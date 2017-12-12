import numpy as np
import sys
import requests as req
import time as tim
import copy

apiCall = 0
key = "AIzaSyAqOBngyzDj3dlnNc7qL-v5RW-uNEB1d9g"


def time(point_a, point_b, problem=None):
    # Returns the duration of the trip from point_a to point_b using a given drone
    if problem is None:
        global apiCall
        print("api call number ", apiCall)
        apiCall += 1
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(point_a.x) + "," + str(
            point_a.y) + "&destinations=" + str(point_b.x) + "," + str(point_b.y) + "&key=" + key
        # print(point_a, point_b)
        return req.get(url).json().get("rows")[0].get("elements")[0].get("duration").get("value")
    else:
        return problem.time(point_a, point_b)


class Nurse:
    def __init__(self, availability=0):
        self.availability = availability  # duration of availability


# This class represents a point on the map (can be either a patient or a depot)
class Point:
    def __init__(self, identifier="", x=0., y=0.):
        self.identifier = identifier  # string
        self.x = x  # float. x coordinate
        self.y = y  # float. y coordinate

    def time(self, other_point, problem):
        # Returns the cost to go from this point to other_point given a drone and given some wind
        return time(self, other_point, problem)

    def __str__(self):
        # overwrites what should be displayed when calling print(some_point)
        return "identifier : {}, (x,y) : ({}, {})".format(self.identifier, self.x, self.y)

    def __repr__(self):
        # returns a printable representation of the object
        return "Point object with identifier : {}".format(self.identifier)


# The class patient inherits from Point. It adds an attribute : 'demand' which represents the patient's demand
class Patient(Point):
    def __init__(self, duration_of_care, identifier="Patient", x=0., y=0.):
        Point.__init__(self, identifier, x, y)
        self.duration_of_care = duration_of_care

    def __str__(self):
        return "identifier : {}, (x,y) : ({}, {}), duration of care : {}".format(self.identifier, self.x, self.y,
                                                                                 self.duration_of_care)


# The class Depot inherits from Point too.
class Office(Point):
    def __init__(self, identifier="Office", x=0., y=0.):
        Point.__init__(self, identifier, x, y)


class Round:
    def __init__(self, patients_list=None, problem=None):
        if patients_list is None:
            self._patients_list = list()
        else:
            self._patients_list = patients_list
        if problem is None:
            self._office = Office()
        else:
            self._office = problem.office
        self._problem = problem
        self._total_savings = 0.  # float. total savings of this delivery compared to the naive approach
        self._total_time = 0.
        self.update()

    def __str__(self):
        self.print_round()
        return ""

    # getters and setters
    def _get_office(self):
        return self._office

    def _set_office(self, office):
        self._office = office
        # when setting a new depot, all the attributes of this class that are impacted are updated
        self.calculate_total_savings()  # the total demand is not affected by the depot
        self.calculate_total_time()

    def _get_patients_list(self):
        return self._patients_list

    def _set_patients_list(self, patients_list):
        self._patients_list = patients_list
        # when setting a new patients list, all the attributes of this class that are impacted are updated
        self.calculate_total_savings()
        self.calculate_total_time()

    def _get_problem(self):
        return self._problem

    def _get_total_savings(self):
        return self._total_savings

    def _get_total_time(self):
        return self._total_time

    office = property(_get_office, _set_office)
    patients_list = property(_get_patients_list, _set_patients_list)
    total_savings = property(_get_total_savings)
    total_time = property(_get_total_time)
    problem = property(_get_problem)

    # methods
    def print_patients_list(self):
        print("Patients list : ({} patient(s))".format(len(self._patients_list)))
        for patient in self._patients_list:
            print(patient)

    def print_office(self):
        print(self._office)

    def print_round(self):
        print("Printing round properties :")
        print("Office :")
        self.print_office()
        self.print_patients_list()
        print("Round properties :")
        print("Total time = {}, total savings = {}"
              .format(self._total_time, self._total_savings))

    def calculate_total_savings(self):
        # this method updates the _total_savings attribute
        naive_total = 0
        for patient in self._patients_list:  # calculates the cost of the naive method
            naive_total = naive_total + time(self._office, patient, self._problem) + patient.duration_of_care \
                          + time(patient, self._office, self._problem)
        self._total_savings = naive_total - self._total_time

    def calculate_total_time(self):
        # this method updates the _total_time attribute
        if self.patients_list == list():
            self._total_time = 0
        else:
            t = time(self.office, self.patients_list[0], self._problem) + self.patients_list[0].duration_of_care
            for i in range(len(self.patients_list) - 1):
                t += time(self.patients_list[i], self.patients_list[i + 1], self._problem) \
                     + self.patients_list[i+1].duration_of_care
            t += time(self.patients_list[-1], self.office, self._problem)
            self._total_time = t

    def update(self):
        self.calculate_total_savings()
        self.calculate_total_time()

    def check_same_office(self, other_delivery):
        # this method returns True if this delivery has the same depot as other_delivery and False otherwise
        return self._office == other_delivery.office

    def check_time_left(self, other_round, rounds_list):
        # this method returns True if other_delivery can be merges to the left of thr current delivery
        # without exceeding the drone's battery.
        rounds_list_2 = [round for round in rounds_list]
        if self in rounds_list and other_round in rounds_list:
            i, j = rounds_list.index(self), rounds_list.index(other_round)
            rounds_list_2.pop(min(i, j))
            rounds_list_2.pop(max(i, j) - 1)
        elif self in rounds_list:
            rounds_list_2.pop(rounds_list.index(self))
        elif other_round in rounds_list:
            rounds_list_2.pop(rounds_list.index(other_round))
        self_2 = Round(patients_list=[patient for patient in self._patients_list], problem=self._problem)
        other_round_2 = Round(patients_list=[patient for patient in other_round._patients_list], problem=other_round._problem)
        self_2.merge_left(other_round_2)
        rounds_list_2.append(self_2)
        return self._problem.is_enough_availability_for_rounds_list(rounds_list_2)

    def check_time_right(self, other_round, rounds_list):
        # this method returns True if other_delivery can be merges to the right of thr current delivery
        # without exceeding the drone's battery.
        rounds_list_2 = [round for round in rounds_list]
        if self in rounds_list and other_round in rounds_list:
            i, j = rounds_list.index(self), rounds_list.index(other_round)
            rounds_list_2.pop(min(i, j))
            rounds_list_2.pop(max(i, j) - 1)
        elif self in rounds_list:
            rounds_list_2.pop(rounds_list.index(self))
        elif other_round in rounds_list:
            rounds_list_2.pop(rounds_list.index(other_round))
        self_2 = Round(patients_list=[patient for patient in self._patients_list], problem=self._problem)
        other_round_2 = Round(patients_list=[patient for patient in other_round._patients_list],
                              problem=other_round._problem)
        self_2.merge_right(other_round_2)
        rounds_list_2.append(self_2)
        return self._problem.is_enough_availability_for_rounds_list(rounds_list_2)

    def check_compatibility_left(self, other_delivery, duration_of_precedent_deliveries, rounds_list):
        can_merge = self.check_same_office(other_delivery)
        can_merge = can_merge and self.check_time_left(other_delivery, rounds_list)
        # can_merge = can_merge and self.check_time_limits_left(other_delivery, duration_of_precedent_deliveries)
        return can_merge

    def check_compatibility_right(self, other_delivery, duration_of_precedent_deliveries, rounds_list):
        can_merge = self.check_same_office(other_delivery)
        can_merge = can_merge and self.check_time_right(other_delivery, rounds_list)
        # can_merge = can_merge and self.check_time_limits_right(other_delivery, duration_of_precedent_deliveries)
        return can_merge

    def can_merge_left(self, other_delivery, duration_of_precedent_deliveries, rounds_list, force_common_patient=False):
        # this method returns True if other_delivery can be merged to the left of the current delivery.
        # returns False otherwise.
        # if force_common_patient is True then this method returns False if the two deliveries don't have a common
        # patient at their border.
        if not self.check_compatibility_left(other_delivery, duration_of_precedent_deliveries, rounds_list):
            return False  # checks the drone, the wind and the demand
        if force_common_patient and self.patients_list[0] != other_delivery.patients_list[-1]:
            return False
        for k in range(len(self.patients_list)):
            if k == 0:
                if self.patients_list[k] in other_delivery.patients_list[:(len(other_delivery.patients_list) - 1)]:
                    return False
            else:
                if self.patients_list[k] in other_delivery.patients_list:
                    return False  # the other patients of "self" may not be anywhere in "other_delivery".
        return True

    def can_merge_right(self, other_delivery, duration_of_precedent_deliveries, rounds_list, force_common_patient=False):
        # this method returns True if other_delivery can be merged to the right of the current delivery.
        # returns False otherwise.
        # if force_common_patient is True then this method returns False if the two deliveries don't have a common
        # patient at their border.
        if not self.check_compatibility_right(other_delivery, duration_of_precedent_deliveries, rounds_list):
            return False
        if force_common_patient and self.patients_list[-1] != other_delivery.patients_list[0]:
            return False
        for k in range(len(self.patients_list)):
            if k == (len(self.patients_list) - 1):
                if self.patients_list[k] in other_delivery.patients_list[1:]:
                    return False
            else:
                if self.patients_list[k] in other_delivery.patients_list:
                    return False
        return True

    def can_merge(self, other_delivery, duration_of_precedent_deliveries, rounds_list, force_common_patient=False):
        left = self.can_merge_left(other_delivery, duration_of_precedent_deliveries, rounds_list, force_common_patient)
        right = self.can_merge_right(other_delivery, duration_of_precedent_deliveries, rounds_list, force_common_patient)
        return left, right

    def merge_left(self, other_delivery, update=True):
        # this methods modifies the current patients list so that the new list is the combination of the one of the
        # other_delivery + the current patients list.
        # if update is True then a full update is performed after the modification of the list. Otherwise only the
        # total demand is updated.
        pl = other_delivery._patients_list[:]
        if self._patients_list != []:
            if pl != [] and pl[-1] == self._patients_list[0]:
                pl = pl + self._patients_list[
                        1:]  # if there is a common patient, it isn't put twice in the new patients list
            else:
                pl = pl + self._patients_list
        self._patients_list = pl
        if not update:
            self.calculate_total_time()
        else:
            self.update()

    def merge_right(self, other_delivery, update=True):
        # the same as before, but on the other side
        l = self._patients_list[:]
        if other_delivery._patients_list != []:
            if l != [] and l[-1] == other_delivery._patients_list[0]:
                l = l + other_delivery._patients_list[1:]
            else:
                l = l + other_delivery._patients_list
        self._patients_list = l
        if not update:
            self.calculate_total_time()
        else:
            self.update()


# A solution is a combination of deliveries (in the form of a list of deliveries).
# This class also stores the cost and savings matrices of the problem it solves.
# The total cost and total savings of the solution are stored as well.
class Solution:
    def __init__(self, name="Unnamed Solution", rounds_list=None):
        if rounds_list is None:
            self._rounds_list = list()
        else:
            self._rounds_list = rounds_list
        self.name = name  # string. Useful for identification and post-processing
        self.time_matrix = None  # numpy two dimensional array. Cost matrix (for the given drone and wind)
        self.savings_matrix = None  # numpy two dimensional array. savings matrix (for the given drone and wind)
        self._total_savings = None  # float. total savings of the solution
        self._total_time = None  # float. total duration of the solution

    def print(self, detailed=True):
        for round in self._rounds_list:
            round.update()
        print("Solution name : {}".format(self.name))
        print("number of tours = {}, total time = {}, total savings = {}"
              .format(len(self._rounds_list), self._total_time, self._total_savings))
        if detailed:
            for delivery in self._rounds_list:
                print(delivery)

    def __str__(self):
        self.print(detailed=False)
        return ""

    def _get_rounds_list(self):
        return self._rounds_list

    def _set_rounds_list(self, deliveries_list):
        self._rounds_list = deliveries_list
        self.calculate_total_time()
        self.calculate_total_savings(True)

    def _get_total_savings(self):
        return self._total_savings

    def _get_total_time(self):
        return self._total_time

    rounds_list = property(_get_rounds_list, _set_rounds_list)
    total_savings = property(_get_total_savings)
    total_time = property(_get_total_time)

    def get_nurses_list(self):
        return [delivery.drone for delivery in self.rounds_list]

    def calculate_total_savings(self, recalculate_for_rounds=False):
        # This method calculates the _total_savings attribute
        if(recalculate_for_rounds):
            for round in self._rounds_list:
                round.calculate_total_savings()
        self._total_savings = sum([d.total_savings for d in self._rounds_list])

    def calculate_total_time(self):
        self._total_time = sum([d.total_time for d in self.rounds_list])


# A problem is a set of patients to deliver from a given depot.
# This class can also store a list of solutions.
class Problem:
    def __init__(self, office=None, patients_list=None, nurses_list=None):
        if office is None:
            self._office = Office()
        else:
            self._office = office
        if patients_list is None:
            self._patients_list = list()
        else:
            self._patients_list = patients_list
        self._number_of_generated_patients = 0  # int. Useful for random problem generation.
        self.solutions_list = list()  # python list of solutions.
        self._costs_matrix = None
        self._nurses_list = nurses_list
        self._availability_of_nurses = sorted([nurse.availability for nurse in self._nurses_list])

    def _get_office(self):
        return self._office

    def _set_office(self, office):
        self._office = office
        self.solutions_list = list()

    def _get_patients_list(self):
        return self._patients_list

    def _set_patients_list(self, patients_list):
        self._patients_list = patients_list
        self.solutions_list = list()

    def _get_number_of_generated_patients(self):
        return self._number_of_generated_patients

    def _get_costs_matrix(self):
        return self._costs_matrix

    def _set_costs_matrix(self, costs_matrix):
        self._costs_matrix = costs_matrix

    def _get_nurses_list(self):
        return self._nurses_list

    def _set_nurses_list(self, nurses_list):
        self._nurses_list = nurses_list

    office = property(_get_office, _set_office)
    patients_list = property(_get_patients_list, _set_patients_list)
    number_of_generated_patients = property(_get_number_of_generated_patients)
    costs_matrix = property(_get_costs_matrix, _set_costs_matrix)
    nurses_list = property(_get_nurses_list, _set_nurses_list)

    def print_patients(self):
        for patient in self._patients_list:
            print(patient)

    def print_office(self):
        print(self._office)

    def number_of_patients(self):
        return len(self._patients_list)

    def print_solutions(self, detailed=False):
        for solution in self.solutions_list:
            print("")
            solution.print(detailed)

    def remove_solution_index(self, index):
        del self.solutions_list[index]

    def remove_solution_named(self, name):
        for i, solution in enumerate(self.solutions_list):
            if solution["Name"] == name:
                del self.solutions_list[i]
                break

    def clear_solutions(self):
        self.solutions_list.clear()

    def generate_random_patients(self, amount=1, x=(48, 49), y=(2, 3), duration_of_care=(600, 1800)):
        # This method adds random patients to the current _patients_list and then updates the _total_demand attribute
        # Every time a new patient is generated, _number_of_generated_patients is increased by 1.
        # When a patient is generated, its identifier is "random patient X" with X=_number_of_generated_patients
        for i in range(amount):
            X = ((x[1] - x[0]) * np.random.rand() + x[0])  # generates X in the wanted interval
            Y = ((y[1] - y[0]) * np.random.rand() + y[0])  # same with Y
            d = np.random.random_integers(duration_of_care[0], duration_of_care[1])
            self._number_of_generated_patients += 1
            c = Patient(d, "", X, Y)
            self._patients_list.append(c)

    def time(self, point_a, point_b):
        if self._costs_matrix is None :
            print("costs matrix None")
            return time(point_a, point_b)
        else:
            a, b = -1, -1
            for i in range(len(self._patients_list)):
                if point_a is self._patients_list[i]:
                    a = i
                if point_b is self._patients_list[i]:
                    b = i
            return self._costs_matrix[a+1][b+1]

    def is_enough_availability_for_rounds_list(self, rounds_list):
        rounds_times = []
        for round in rounds_list:
            round.calculate_total_time()
            rounds_times.append(round.total_time)
        if len(rounds_times) > len(self._nurses_list):
            return False
        rounds_times.sort()
        for i in range(len(rounds_times)):
            if rounds_times[i] > self._availability_of_nurses[i]:
                return False
        return True



def calculate_cost_matrix(problem):
    # This function returns the cost matrix of a problem for a given drone and a given wind.
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="
    patients_locations = str(problem.office.x) + "," + str(problem.office.y)
    for patient in problem.patients_list:
        patients_locations += "|" + str(patient.x) + "," + str(patient.y)
    patients_locations = patients_locations[:-1]
    url += patients_locations + "&destinations=" + patients_locations + "&key=" + key
    print(url)
    json_matrix = req.get(url).json().get("rows")
    mat_dim = problem.number_of_patients() + 1  # the +1 stands for the depot
    cost_matrix = np.zeros((mat_dim, mat_dim))
    """for j in range(1, mat_dim):  # first line : costs from the depot to the client
        print(0,j)
        cost_matrix[0, j] = json_matrix[0].get("elements")[j].get("duration").get("value")
    for i in range(1, mat_dim):  # first column : costs from the clients to the depot
        print(i,0)
        cost_matrix[i, 0] = time(problem.patients_list[i - 1], problem.office)"""
    for i in range(0, mat_dim):  # costs from client i to client j
        for j in range(0, mat_dim):
            cost_matrix[i, j] = json_matrix[i].get("elements")[j].get("duration").get("value")
    problem.costs_matrix = cost_matrix


def calculate_savings_matrix(problem):
    # This function returns the savings matrix of a problem for a given drone and a given wind.
    mat_dim = problem.number_of_patients()
    savings_matrix = np.zeros((mat_dim, mat_dim))
    calculate_cost_matrix(problem)
    cost_matrix = problem.costs_matrix
    for i in range(mat_dim):
        for j in range(mat_dim):
            if i != j:
                savings_matrix[i, j] = cost_matrix[i + 1, 0] + cost_matrix[0, j + 1] - cost_matrix[i + 1, j + 1]
    return savings_matrix


def _clarke_and_wright_init(problem, name="Unnamed solution"):
    # This function is used to initialize the Clarke and Wright algorithm.
    # This function calculates the savings matrix and store it in an instance of class Solution.
    # This solution is appended to the solutions list of the problem.
    # This function returns a tuple (sorted_savings, arg_sorted_savings)
    # with sorted_savings = the sorted savings in a one-dimensional numpy array
    # and arg_sorted_savings = the arguments used to sort the sorted savings
    savings_mat = calculate_savings_matrix(problem)
    sol = Solution()
    sol.savings_matrix = savings_mat
    sol.name = name
    problem.solutions_list.append(sol)
    savings_flat = np.ndarray.flatten(savings_mat)
    arg_sorted_savings = np.argsort(savings_flat)
    sorted_savings = [savings_flat[i] for i in arg_sorted_savings]
    return sorted_savings, arg_sorted_savings


def _get_patients_pair_from_arg(patients_list, arg_k):
    # This function returns a tuple (client_i, client_j) where both client_i and client_j are instance of class Client.
    number_of_patients = len(patients_list)
    patient_i = arg_k // number_of_patients  # departure client
    patient_j = arg_k % number_of_patients  # arrival client
    return patients_list[patient_i], patients_list[patient_j]


def _sequential_merge_if_possible(current_delivery, candidate_delivery, duration_of_precedent_deliveries, rounds_list):
    # This function merges two deliveries if possible in the sequential version of Clarke and Wright (ie the two
    # deliveries MUST have a common client at their borders)
    # It returns True if the two deliveries have been merged and False otherwise.
    can_merge = current_delivery.can_merge(candidate_delivery, duration_of_precedent_deliveries, rounds_list, True)
    if can_merge[0]:
        current_delivery.merge_left(candidate_delivery, False)
    elif can_merge[1]:
        current_delivery.merge_right(candidate_delivery, False)
    current_delivery.update()
    return can_merge[0] or can_merge[1]


def _sequential_build_deliveries(sorted_savings, arg_sorted_savings, problem):
    # This function returns a list of instances of class Delivery calculated with the use of the sequential Clarke
    # and Wright algorithm.
    rounds_list = []
    n = len(sorted_savings)
    visited_patients = []  # list of the clients who are already in a delivery
    goal = len(problem.patients_list)  # the goal is to deliver all the clients
    duration_of_precedent_rounds = 0
    while len(visited_patients) != goal:
        round = Round([], problem=problem)
        i = 1
        while i <= n:
            number_of_delivered_patients = len(visited_patients)
            if round.patients_list == []:  # a new delivery must be started. Two compatible clients must be found
                patient_a, patient_b = _get_patients_pair_from_arg(problem.patients_list, arg_sorted_savings[
                    n - i])  # arg_sorted_savings is sorted in the increasing order of savings, so the research begins at the end
                if patient_a != patient_b and not (patient_a in visited_patients) and not (
                        patient_b in visited_patients) and problem.is_enough_availability_for_rounds_list(rounds_list + [Round([patient_a,patient_b], problem=problem)]) :  # if both clients can form a new delivery
                    round.patients_list.append(patient_a)  # both clients are added to the clients list
                    round.patients_list.append(patient_b)
                    visited_patients.append(patient_a)  # they are marked delivered
                    visited_patients.append(patient_b)
                    i = 1  # the research restarts from the begining (or the end) of the sorted savings list
            else:  # two clients must be found : one that isn't in any delivery yet, and the other one must be in the current one
                patient_a, patient_b = _get_patients_pair_from_arg(problem.patients_list, arg_sorted_savings[n - i])
                candidate_round = Round([patient_a,patient_b], problem=problem)  # this candidate will be merged to the current delivery if possible
                a_delivered, b_delivered = patient_a in visited_patients, patient_b in visited_patients
                if patient_a != patient_b and (not a_delivered or not b_delivered):
                    if _sequential_merge_if_possible(round, candidate_round, duration_of_precedent_rounds, rounds_list):
                        if a_delivered:
                            visited_patients.append(patient_b)
                        else:
                            visited_patients.append(patient_a)
                        i = 1
            if len(visited_patients) == number_of_delivered_patients:
                i += 1
        if round.patients_list == []:
            break  # if the delivery is still empty after the preceding instructions, the algorithm can stop since it won't make new deliveries any more
        round.update()
        rounds_list = rounds_list + [round]  # the new delivery is added to the deliveries list
        duration_of_precedent_rounds += round.total_time
    return rounds_list


def search_deliveries_for_patient(patient, rounds_list, left_border=False, interior=False, right_border=False):
    # This function searches for a specified client in a list of deliveries. The search is performed at the border
    # and/or in the interior of the deliveries according to the value of the parameters.
    # The function returns True and the instance of class Delivery where the client has been found.
    # It returns False and None if the client has not been found in any of the deliveries.
    for round in rounds_list:
        if interior and len(round.patients_list) >= 2:
            if patient in round.patients_list[1:-1]:
                return round
        if left_border and len(round.patients_list) >= 1:
            if patient == round.patients_list[0]:
                return round
        if right_border and len(round.patients_list) >= 1:
            if patient == round.patients_list[-1]:
                return round
    return None


def _parallel_build_deliveries(sorted_savings, arg_sorted_savings, problem):
    # This function returns a list of instances of class Delivery calculated with the use of the parallel Clarke
    # and Wright algorithm.
    # !!! RETURNS A RESULT THAT DOESN'T CONSIDER THE time_limit ARGUMENTS
    rounds_list = []
    n = len(sorted_savings)
    for i in range(1, n + 1):
        patient_a, patient_b = _get_patients_pair_from_arg(problem.patients_list, arg_sorted_savings[n - i])
        patient_a_somewhere = search_deliveries_for_patient(patient_a, rounds_list, True, True,
                                                           True)  # finds if client_a is already in a delivery (anywhere)
        patient_b_somewhere = search_deliveries_for_patient(patient_b, rounds_list, True, True,
                                                           True)  # finds if client_b is already in a delivery (anywhere)
        patient_a_right = search_deliveries_for_patient(patient_a, rounds_list, False, False,
                                                       True)  # finds if client_a is on the right of a delivery
        patient_b_left = search_deliveries_for_patient(patient_b, rounds_list, True, False,
                                                      False)  # finds if client_b is on the left of a delivery
        if patient_a != patient_b and patient_a_somewhere is None and patient_b_somewhere is None :
            new_round = Round([patient_a,patient_b], problem=problem)
            if problem.is_enough_availability_for_rounds_list(rounds_list + [new_round]):  # if both clients aren't in any delivery and if their total demands aren't over the drone capacity, they can be bound
                rounds_list.append(new_round)
        elif patient_a_right is not None and patient_b_somewhere is None:
            merged_round = Round([patient for patient in patient_a_right.patients_list] + [patient_b], problem)
            if problem.is_enough_availability_for_rounds_list([round for round in rounds_list if round is not patient_a_right] + [merged_round]):  # if client_a is on the right of a delivery and client_b is nowhere, client_b can be added to that delivery if the demand is not too high
                rounds_list.remove(patient_a_right)
                merged_round.update()
                rounds_list.append(merged_round)
        elif patient_b_left is not None and patient_a_somewhere is None:  # the same as the preceding case
            merged_round = Round([patient_a] + [patient for patient in patient_b_left.patients_list], problem)
            if problem.is_enough_availability_for_rounds_list([round for round in rounds_list if round is not patient_b_left] + [merged_round]):  # if client_a is on the right of a delivery and client_b is nowhere, client_b can be added to that delivery if the demand is not too high
                rounds_list.remove(patient_b_left)
                merged_round.update()
                rounds_list.append(merged_round)
        elif patient_a_right is not None and patient_b_left is not None:  # in this case, both clients are already each in a delivery, but those deliveries can be merged if the total demand is not too high
            if patient_a_right is not patient_b_left and patient_a_right.can_merge_right(patient_b_left, 0, rounds_list):
                rounds_list.remove(patient_a_right)
                rounds_list.remove(patient_b_left)
                round = patient_a_right
                round.merge_right(patient_b_left)
                rounds_list.append(round)
    return rounds_list


def _build_deliveries(version, sorted_savings, arg_sorted_savings, problem):
    if version == 'Sequential':
        return _sequential_build_deliveries(sorted_savings, arg_sorted_savings, problem)
    if version == 'Parallel':
        return _parallel_build_deliveries(sorted_savings, arg_sorted_savings, problem)
    return []


def add_single_patient_rounds(problem, rounds_list):
    # This function modifies the deliveries_list argument by adding deliveries containing a single client.
    patients_list = problem.patients_list
    duration_of_precedent_rounds = sum([d.total_time for d in rounds_list])
    for patient in patients_list:  # checks, for each client, if it is in a delivery
        visited = False
        for d in rounds_list:
            if patient in d.patients_list:
                visited = True
                break
        if not visited :  # if the client is not delivered, a new delivery is created if it is possible
            new_round = Round([patient], problem=problem)
            if problem.is_enough_availability_for_rounds_list(rounds_list + [new_round]):
                print("ADD SINGLE PATIENT")
                rounds_list.append(new_round)
                duration_of_precedent_rounds += time(problem.office, patient, problem) + patient.duration_of_care + time(patient,problem.office, problem)


def clarke_and_wright(problem, version, name=None):
    if version != "Sequential" and version != "Parallel":
        print("Unexpected version : {}".format(version))
        print("Please use 'Sequential' or 'Parallel'")
        return
    if name is None:
        name = version + " Clarke and Wright"
    sorted_savings, arg_sorted_savings = _clarke_and_wright_init(problem, name)
    rounds_list = _build_deliveries(version, sorted_savings, arg_sorted_savings, problem)
    add_single_patient_rounds(problem, rounds_list)
    problem.solutions_list[-1].rounds_list = rounds_list


prob = Problem(Office("Office", 48.5, 2.5), nurses_list=[Nurse(15000), Nurse(10000)])
prob.generate_random_patients(5)
prob2 = copy.deepcopy(prob)
#top = tim.time()
clarke_and_wright(prob, "Parallel")
#print(tim.time() - top)
prob.solutions_list[-1].print()
"""top = tim.time()
clarke_and_wright(prob2, Nurse(30000), "Parallel")
print(tim.time() - top)
prob2.solutions_list[-1].print()"""

