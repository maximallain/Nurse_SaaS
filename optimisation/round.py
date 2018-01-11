from point import *


class Round:
    """
    Class used to represent a round for a nurse (starting from and ending at the office, with a list of visited patients
    """

    def __init__(self, patients_list=None, problem=None, nurse=None):
        """
        Instanciates a Round object
        :param patients_list: the list of patients to visit during this round
        :param problem: the associated problem
        :param nurse: the nurse that performs this round
        """
        if patients_list is None:
            self._patients_list = list()
        else:
            self._patients_list = patients_list
        if problem is None:
            self._office = Office()
        else:
            self._office = problem.office
        self._nurse = nurse
        self._problem = problem
        self._total_savings = 0.
        self._total_cost = 0.
        if problem is not None and self._patients_list is not None and len(self._patients_list) > 0 \
                and nurse is not None:
            self.update()

    def __str__(self):
        """
        Converts this Round object to a string
        :return: a string representing this round
        """
        result = "Printing round properties :\n"
        result += "Office :\n"
        result += str(self._office) + "\n"
        result += str(self._nurse) + "\n"
        result += "Patients list : ({} patient(s))".format(len(self._patients_list)) + "\n"
        for i in range(len(self._patients_list)):
            patient = self._patients_list[i]
            if i == 0:
                last_point = self._office
            else:
                last_point = self._patients_list[i-1]
            result += "cost of trip : {}".format(self._problem.cost(last_point, patient)) + "\n"
            result += str(patient) + ", visited at {}".format(self.time_when_patient_visited(patient)) \
                + "\n"
        result += "cost of trip : {}".format(self._problem.cost(self._patients_list[-1], self._office)) + "\n"
        result += "Round properties :" + "\n"
        result += "Total cost = {}, total savings = {}".format(self._total_cost, self._total_savings) + "\n"
        return result

    def _get_office(self):
        return self._office

    def _set_office(self, office):
        self._office = office
        self.calculate_total_savings()
        self.calculate_total_cost()

    def _get_patients_list(self):
        return self._patients_list

    def _set_patients_list(self, patients_list):
        self._patients_list = patients_list
        self.calculate_total_savings()
        self.calculate_total_cost()

    def _get_problem(self):
        return self._problem

    def _get_total_savings(self):
        return self._total_savings

    def _get_total_cost(self):
        return self._total_cost

    def _get_nurse(self):
        return self._nurse

    def _set_nurse(self, nurse):
        self._nurse = nurse

    office = property(_get_office, _set_office)
    patients_list = property(_get_patients_list, _set_patients_list)
    total_savings = property(_get_total_savings)
    total_cost = property(_get_total_cost)
    problem = property(_get_problem)
    nurse = property(_get_nurse, _set_nurse)

    def print_patients_list(self):
        """Prints this round's patients list to the console"""
        print("Patients list : ({} patient(s))".format(len(self._patients_list)))
        for patient in self._patients_list:
            print(patient)

    def print_office(self):
        """Prints this round's office to the console"""
        print(self._office)

    def print_nurse(self):
        print(self._nurse)

    def print_round(self):
        """Prints this round to the console"""
        print("Printing round properties :")
        print("Office :")
        self.print_office()
        self.print_nurse()
        self.print_patients_list()
        print("Round properties :")
        print("Total cost = {}, total savings = {}"
              .format(self._total_cost, self._total_savings))

    def calculate_total_cost(self):
        """Updates the _total_cost attribute of this round"""
        if self.patients_list == list():
            self._total_cost = 0
        else:
            if self.patients_list[0].must_be_visited_exactly_at == -1:
                t = self._problem.cost(self._office, self._patients_list[0]) + self._patients_list[0].duration_of_care
            else:
                t = self.patients_list[0].must_be_visited_exactly_at + self._patients_list[0].duration_of_care
            for i in range(len(self._patients_list) - 1):
                if self.patients_list[i+1].must_be_visited_exactly_at == -1:
                    t += self._problem.cost(self._patients_list[i], self._patients_list[i + 1]) \
                         + self._patients_list[i + 1].duration_of_care
                else:
                    t = self.patients_list[i+1].must_be_visited_exactly_at + self._patients_list[i+1].duration_of_care
            t += self._problem.cost(self._patients_list[-1], self._office)
            self._total_cost = t

    def calculate_total_savings(self):
        """Updates the _total_savings attribute of this round"""
        naive_total = self._nurse.start_time
        for patient in self._patients_list:
            if patient.must_be_visited_exactly_at == -1:
                naive_total = naive_total + self._problem.cost(self._office, patient) + patient.duration_of_care \
                              + self._problem.cost(patient, self._office)
            else:
                naive_total = patient.must_be_visited_exactly_at + patient.duration_of_care \
                              + self._problem.cost(patient, self._office)
        naive_total -= self._nurse.start_time
        self._total_savings = naive_total - self._total_cost

    def update(self):
        """Updates the _total_savings and _total_cost attributes of this round"""
        self.calculate_total_cost()
        self.calculate_total_savings()

    def can_merge_left(self, other_round, force_common_patient=False):
        """
        Returns True if other_round can be merged to the left of the current round, False otherwise.
        If force_common_patient is True then this method returns False if the two rounds don't have a common
        patient at their border.
        !!! This method doesn't care about time and availability constraints
        :param other_round: the other round that we want to merge with self
        :param force_common_patient: if set to True, forces both rounds to have a common patient at their borders
        :return: True if other_round can be merged to the left of the current round, False otherwise
        """
        if force_common_patient and self.patients_list[0] != other_round.patients_list[-1]:
            return False
        for k in range(len(self.patients_list)):
            if k == 0:
                if self.patients_list[k] in other_round.patients_list[:(len(other_round.patients_list) - 1)]:
                    return False
            else:
                if self.patients_list[k] in other_round.patients_list:
                    return False
        return True

    def can_merge_right(self, other_round, force_common_patient=False):
        """
        Returns True if other_round can be merged to the right of the current round, False otherwise.
        If force_common_patient is True then this method returns False if the two rounds don't have a common
        patient at their border.
        !!! This method doesn't care about time and availability constraints
        :param other_round: the other round that we want to merge with self
        :param force_common_patient: if set to True, forces both rounds to have a common patient at their borders
        :return: True if other_round can be merged to the right of the current round, False otherwise
        """
        if force_common_patient and self.patients_list[-1] != other_round.patients_list[0]:
            return False
        for k in range(len(self.patients_list)):
            if k == (len(self.patients_list) - 1):
                if self.patients_list[k] in other_round.patients_list[1:]:
                    return False
            else:
                if self.patients_list[k] in other_round.patients_list:
                    return False
        return True

    def merge_left(self, other_round):
        """
        Merges other_round to the left of this round
        :param other_round: the other round that we want to merge with self
        """
        pl = other_round.patients_list[:]
        if len(self._patients_list) != 0:
            if pl != [] and pl[-1] == self._patients_list[0]:
                pl = pl + self._patients_list[1:]
            else:
                pl = pl + self._patients_list
        self._patients_list = pl
        if self.nurse is not None:
            self.update()

    def merge_right(self, other_round):
        """
        Merges other_round to the right of this round
        :param other_round: the other round that we want to merge with self
        """
        pl = self._patients_list[:]
        if len(other_round.patients_list) != 0:
            if pl != [] and pl[-1] == other_round.patients_list[0]:
                pl = pl + other_round.patients_list[1:]
            else:
                pl = pl + other_round.patients_list
        self._patients_list = pl
        if self.nurse is not None:
            self.update()

    def time_when_patient_visited(self, patient_to_visit):
        """
        Computes the time when patient_to_visit (that should be in this round) is visited.
        :param patient_to_visit: the patient
        :return: the time (in seconds from midnight) when the patient is visited
        """
        time = self._nurse.start_time
        if patient_to_visit in self._patients_list:
            time += self._problem.cost(self._problem.office, self._patients_list[0])
            for i in range(len(self._patients_list)):
                patient = self._patients_list[i]
                next_patient = None
                if i < len(self._patients_list) - 1:
                    next_patient = self._patients_list[i+1]
                if patient.must_be_visited_exactly_at != -1:
                    time = patient.must_be_visited_exactly_at
                if patient is patient_to_visit:
                    return time
                time += patient.duration_of_care + self._problem.cost(patient, next_patient)
        return -1

    def can_be_assigned_to(self, nurse):
        """
        Checks if a round can be assigned to a nurse without violating the precise visit time and availability
        constraints
        :param nurse: the nurse we want to assign the round to
        :return: True iff this round can be assigned to a nurse without violating the precise visit time constraints
        """
        time = nurse.start_time + self._problem.cost(self.office, self.patients_list[0])
        for i in range(len(self._patients_list)-1):
            patient = self._patients_list[i]
            next_patient = self._patients_list[i+1]
            if patient.must_be_visited_exactly_at != -1 and patient.must_be_visited_exactly_at < time:
                return False
            if patient.must_be_visited_exactly_at != -1:
                time = patient.must_be_visited_exactly_at
            time += patient.duration_of_care + self._problem.cost(patient, next_patient)
        if self._patients_list[-1].must_be_visited_exactly_at != -1 \
                and self._patients_list[-1].must_be_visited_exactly_at < time:
            return False
        time += self._patients_list[-1].duration_of_care + self._problem.cost(self._patients_list[-1],
                                                                              self._problem.office)
        return time <= nurse.start_time + nurse.availability
