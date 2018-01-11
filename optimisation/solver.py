from problem import *


class Solver:
    """Class used to solve a specific problem with Clarke & Wright algorithm,
    with either sequential or parallel version"""

    def __init__(self, problem):
        """
        Instanciates a Solver object
        :param problem: the problem we want to solve
        """
        self._problem = problem
        self._sorted_savings = None
        self._arg_sorted_savings = None

    def calculate_savings_matrix(self):
        """
        This method calculates the savings_matrix of the problem
        :return: the savings matrix of the problem
        """
        mat_dim = self._problem.number_of_patients()
        savings_matrix = np.zeros((mat_dim, mat_dim))
        cost_matrix = self._problem.costs_matrix
        for i in range(mat_dim):
            for j in range(mat_dim):
                if i != j:
                    savings_matrix[i, j] = cost_matrix[i + 1, 0] + cost_matrix[0, j + 1] - cost_matrix[i + 1, j + 1]
        return savings_matrix

    def clarke_and_wright_init(self):
        """Initializes the Clarke & Wright algorithm, computing cost_matrix and savings_matrix attributes of
        the problem. Sets the attributes _sorted_savings and _arg_sorted_savings of the solver, which will be
        used later"""
        if self._problem.costs_matrix is None:
            self._problem.calculate_cost_matrix()
        savings_matrix = self.calculate_savings_matrix()
        savings_flat = np.ndarray.flatten(savings_matrix)
        arg_sorted_savings = np.argsort(savings_flat)
        sorted_savings = [savings_flat[i] for i in arg_sorted_savings]
        self._sorted_savings = sorted_savings
        self._arg_sorted_savings = arg_sorted_savings

    def get_patients_pair_from_arg(self, arg_k):
        """
        Returns a tuple (patient_i, patient_j) where both patient_i and patient_j are instance of class Patient,
        and where the savings from patient_i to patient_j is at the (arg_k)th position in sorted_savings
        :param arg_k: the position of potential savings we are looking at
        :return: a tuple (patient_i, patient_j) corresponding to the savings at (arg_k)th position
        """
        number_of_patients = len(self._problem.patients_list)
        patient_i = arg_k // number_of_patients
        patient_j = arg_k % number_of_patients
        return self._problem.patients_list[patient_i], self._problem.patients_list[patient_j]

    @staticmethod
    def search_rounds_for_patient(patient, rounds_list, left_border=False, interior=False, right_border=False):
        """
        Searches for a specified patient in a list of rounds. The search is performed at the border
        and/or in the interior of the rounds according to the value of the parameters.
        The method returns the instance of class Round where the patient has been found.
        It returns None if the patient has not been found in any of the rounds at the right place.
        :param patient: the patient we are looking for
        :param rounds_list: the list of rounds we are searching the patient in
        :param left_border: If set to True, the patient can be placed at the left border of rounds
        :param interior: If set to True, the patient can be placed in the interior of rounds
        :param right_border: If set to True, the patient can be placed at the right border of rounds
        :return: The round where the patient has been found if it has, None otherwise
        """
        for rnd in rounds_list:
            if interior and len(rnd.patients_list) >= 2:
                if patient in rnd.patients_list[1:-1]:
                    return rnd
            if left_border and len(rnd.patients_list) >= 1:
                if patient is rnd.patients_list[0]:
                    return rnd
            if right_border and len(rnd.patients_list) >= 1:
                if patient is rnd.patients_list[-1]:
                    return rnd
        return None

    @staticmethod
    def add_round_if_possible(new_round, rounds_list, problem):
        """
        Adds a new round to the rounds list if it is possible
        :param new_round: the new round we want to add. It should contain exactly 2 patients in its patients list
        :param rounds_list: the current rounds list
        :param problem: the associated problem
        """
        busy_nurses = [rnd.nurse for rnd in rounds_list]
        available_nurses = [nurse for nurse in problem.nurses_list if nurse not in busy_nurses]
        for nurse in available_nurses:
            if new_round.can_be_assigned_to(nurse):
                new_round.nurse = nurse
                rounds_list.append(new_round)
                break

    @staticmethod
    def add_merged_round_if_possible(merged_round, old_round, rounds_list, problem):
        """
        Adds merged_round and removes old_round from rounds_list if possible
        :param merged_round: the merged_round (ie: with a new patient)
        :param old_round: the old round (without the new patient)
        :param rounds_list: the current rounds_list
        :param problem: the associated problem
        """
        busy_nurses = [rnd.nurse for rnd in rounds_list]
        available_nurses = [nurse for nurse in problem.nurses_list if nurse not in busy_nurses]
        if merged_round.can_be_assigned_to(old_round.nurse):
            merged_round.nurse = old_round.nurse
            rounds_list.remove(old_round)
            merged_round.update()
            rounds_list.append(merged_round)
        else:
            for nurse in available_nurses:
                if merged_round.can_be_assigned_to(nurse):
                    merged_round.nurse = nurse
                    rounds_list.remove(old_round)
                    merged_round.update()
                    rounds_list.append(merged_round)

    @staticmethod
    def merge_rounds_if_possible(left_round, right_round, rounds_list, problem):
        """
        Merges left_round and right_round if possible
        :param left_round: the left round
        :param right_round: the right round
        :param rounds_list: the current rounds list
        :param problem: the associated problem
        """
        busy_nurses = [rnd.nurse for rnd in rounds_list]
        available_nurses = [nurse for nurse in problem.nurses_list if nurse not in busy_nurses]
        merged_round = Round(left_round.patients_list, problem)
        merged_round.merge_right(right_round)
        if merged_round.can_be_assigned_to(left_round.nurse):
            merged_round.nurse = left_round.nurse
            merged_round.update()
            rounds_list.remove(left_round)
            rounds_list.remove(right_round)
            rounds_list.append(merged_round)
        elif merged_round.can_be_assigned_to(right_round.nurse):
            merged_round.nurse = right_round.nurse
            merged_round.update()
            rounds_list.remove(left_round)
            rounds_list.remove(right_round)
            rounds_list.append(merged_round)
        else:
            for nurse in available_nurses:
                if merged_round.can_be_assigned_to(nurse):
                    merged_round.nurse = nurse
                    merged_round.update()
                    rounds_list.remove(left_round)
                    rounds_list.remove(right_round)
                    rounds_list.append(merged_round)
                    break

    def parallel_build_rounds(self):
        """
        Builds a rounds list using the parallel version of Clarke & Wright algorithm
        :return: the rounds list
        """
        rounds_list = []
        n = len(self._sorted_savings)
        for i in range(1, n + 1):
            patient_a, patient_b = self.get_patients_pair_from_arg(self._arg_sorted_savings[n - i])
            patient_a_somewhere = self.search_rounds_for_patient(patient_a, rounds_list, True, True, True)
            patient_b_somewhere = self.search_rounds_for_patient(patient_b, rounds_list, True, True, True)
            patient_a_right = self.search_rounds_for_patient(patient_a, rounds_list, False, False, True)
            patient_b_left = self.search_rounds_for_patient(patient_b, rounds_list, True, False, False)
            if patient_a != patient_b and patient_a_somewhere is None and patient_b_somewhere is None:
                new_round = Round([patient_a, patient_b], problem=self._problem)
                self.add_round_if_possible(new_round, rounds_list, self._problem)
            elif patient_a_right is not None and patient_b_somewhere is None:
                merged_round = Round([patient for patient in patient_a_right.patients_list] + [patient_b],
                                     self._problem)
                self.add_merged_round_if_possible(merged_round, patient_a_right, rounds_list, self._problem)
            elif patient_b_left is not None and patient_a_somewhere is None:
                merged_round = Round([patient_a] + [patient for patient in patient_b_left.patients_list], self._problem)
                self.add_merged_round_if_possible(merged_round, patient_b_left, rounds_list, self._problem)
            elif patient_a_right is not None and patient_b_left is not None:
                if patient_a_right is not patient_b_left and patient_a_right.can_merge_right(patient_b_left):
                    self.merge_rounds_if_possible(patient_a_right, patient_b_left, rounds_list, self._problem)
        return rounds_list

    def add_single_patient_rounds(self, rounds_list):
        """
        Adds single patient rounds to rounds_list for patients that couldn't be merged in any round
        :param rounds_list: the list of rounds that were built thanks to Clarke & Wright algorithm
        """
        patients_list = self._problem.patients_list
        busy_nurses = [rnd.nurse for rnd in rounds_list]
        available_nurses = [nurse for nurse in self._problem.nurses_list if nurse not in busy_nurses]
        for patient in patients_list:
            visited = False
            for d in rounds_list:
                if patient in d.patients_list:
                    visited = True
                    break
            if not visited:
                new_round = Round([patient], problem=self._problem)
                for nurse in available_nurses:
                    if new_round.can_be_assigned_to(nurse):
                        new_round.nurse = nurse
                        rounds_list.append(new_round)
                        available_nurses.remove(nurse)
                        busy_nurses.append(nurse)
                        break

    def compute_clarke_and_wright(self, name=None):
        """
        Computes a complete solution to the problem using the specified version of Clarke & Wright algorithm
        :param name: the given name of the solution (if not specified, it is: version + ' Clarke & Wright'
        :return:
        """
        if name is None:
            name = "Parallel Clarke & Wright"
        self.clarke_and_wright_init()
        rounds_list = self.parallel_build_rounds()
        self.add_single_patient_rounds(rounds_list)
        self._problem.solutions_list.append(Solution(name, rounds_list))
