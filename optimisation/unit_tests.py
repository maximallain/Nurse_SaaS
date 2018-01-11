import unittest
from solver import *
from nurse import *


class PointTestCase(unittest.TestCase):
    """Tests the address attribute"""

    def test_specified_address(self):
        point = Point(address="Paris")
        point2 = Point(address="Paris", x=48.5, y=2.5)
        point3 = Point(x=48.5, y=2.5)
        self.assertEqual(point.address, "Paris")
        self.assertEqual(point2.address, "Paris")
        self.assertEqual(point3.address, "48.5,2.5")


class RoundTestCase1(unittest.TestCase):
    """Tests the calculate_total_cost method with different number of patients and precise time constraints"""

    def setUp(self):
        self._office = Office(x=0, y=0)
        self._nurse = Nurse(1)
        self._problem = Problem(self._office, [], [self._nurse])
        self._round = Round([], self._problem, self._nurse)

    def test_calculate_total_cost(self):
        self.assertEqual(self._round.total_cost, 0)

    def test_calculate_total_cost_one_patient(self):
        self._patient = Patient(x=1, y=0, duration_of_care=1000)
        self._problem = Problem(self._office, [self._patient], [self._nurse])
        self._problem.costs_matrix = np.zeros((2, 2))
        self._problem.costs_matrix[0, 1] = 1000
        self._problem.costs_matrix[1, 0] = 1000
        self._round = Round([self._patient], self._problem, self._nurse)
        self.assertEqual(self._round.total_cost, 3000)

    def test_calculate_total_cost_two_patients(self):
        self._patients_list = [Patient(x=1, y=0, duration_of_care=1000), Patient(x=2, y=0, duration_of_care=1000)]
        self._problem = Problem(self._office, self._patients_list, [self._nurse])
        self._problem.costs_matrix = np.zeros((3, 3))
        self._problem.costs_matrix[0][1] = 1000
        self._problem.costs_matrix[1][0] = 1000
        self._problem.costs_matrix[0][2] = 2000
        self._problem.costs_matrix[2][0] = 2000
        self._problem.costs_matrix[1][2] = 1000
        self._problem.costs_matrix[2][1] = 1000
        self._round = Round(self._patients_list, self._problem, self._nurse)
        self.assertEqual(self._round.total_cost, 6000)

    def test_calculate_total_cost_five_patients(self):
        self._patients_list = [Patient(x=1, y=0, duration_of_care=1000), Patient(x=2, y=0, duration_of_care=1000),
                               Patient(x=3, y=0, duration_of_care=1000), Patient(x=4, y=0, duration_of_care=1000)]
        self._problem = Problem(self._office, self._patients_list, [self._nurse])
        self._problem.costs_matrix = np.zeros((5, 5))
        self._problem.costs_matrix[0][1] = 1000
        self._problem.costs_matrix[1][0] = 1000
        self._problem.costs_matrix[0][2] = 2000
        self._problem.costs_matrix[2][0] = 2000
        self._problem.costs_matrix[0][3] = 3000
        self._problem.costs_matrix[3][0] = 3000
        self._problem.costs_matrix[0][4] = 4000
        self._problem.costs_matrix[4][0] = 4000
        self._problem.costs_matrix[1][2] = 1000
        self._problem.costs_matrix[2][1] = 1000
        self._problem.costs_matrix[1][3] = 2000
        self._problem.costs_matrix[3][1] = 2000
        self._problem.costs_matrix[1][4] = 3000
        self._problem.costs_matrix[4][1] = 3000
        self._problem.costs_matrix[2][3] = 1000
        self._problem.costs_matrix[3][2] = 1000
        self._problem.costs_matrix[2][4] = 2000
        self._problem.costs_matrix[4][2] = 2000
        self._problem.costs_matrix[3][4] = 1000
        self._problem.costs_matrix[4][3] = 1000
        self._round = Round(self._patients_list, self._problem, self._nurse)
        self.assertEqual(self._round.total_cost, 12000)

    def test_calculate_total_cost_two_patients_with_precise_time_constraint(self):
        self._patients_list = [Patient(x=1, y=0, duration_of_care=1000),
                               Patient(x=2, y=0, duration_of_care=1000, must_be_visited_exactly_at=10000)]
        self._problem = Problem(self._office, self._patients_list, [self._nurse])
        self._problem.costs_matrix = np.zeros((3, 3))
        self._problem.costs_matrix[0][1] = 1000
        self._problem.costs_matrix[1][0] = 1000
        self._problem.costs_matrix[0][2] = 2000
        self._problem.costs_matrix[2][0] = 2000
        self._problem.costs_matrix[1][2] = 1000
        self._problem.costs_matrix[2][1] = 1000
        self._round = Round(self._patients_list, self._problem, self._nurse)
        self.assertEqual(self._round.total_cost, 13000)

    def test_calculate_total_cost_five_patients_with_precise_time_constraint(self):
        self._patients_list = [Patient(x=1, y=0, duration_of_care=1000), Patient(x=2, y=0, duration_of_care=1000,
                                                                                 must_be_visited_exactly_at=5000),
                               Patient(x=3, y=0, duration_of_care=1000), Patient(x=4, y=0, duration_of_care=1000)]
        self._problem = Problem(self._office, self._patients_list, [self._nurse])
        self._problem.costs_matrix = np.zeros((5, 5))
        self._problem.costs_matrix[0][1] = 1000
        self._problem.costs_matrix[1][0] = 1000
        self._problem.costs_matrix[0][2] = 2000
        self._problem.costs_matrix[2][0] = 2000
        self._problem.costs_matrix[0][3] = 3000
        self._problem.costs_matrix[3][0] = 3000
        self._problem.costs_matrix[0][4] = 4000
        self._problem.costs_matrix[4][0] = 4000
        self._problem.costs_matrix[1][2] = 1000
        self._problem.costs_matrix[2][1] = 1000
        self._problem.costs_matrix[1][3] = 2000
        self._problem.costs_matrix[3][1] = 2000
        self._problem.costs_matrix[1][4] = 3000
        self._problem.costs_matrix[4][1] = 3000
        self._problem.costs_matrix[2][3] = 1000
        self._problem.costs_matrix[3][2] = 1000
        self._problem.costs_matrix[2][4] = 2000
        self._problem.costs_matrix[4][2] = 2000
        self._problem.costs_matrix[3][4] = 1000
        self._problem.costs_matrix[4][3] = 1000
        self._round = Round(self._patients_list, self._problem, self._nurse)
        self.assertEqual(self._round.total_cost, 14000)


class RoundTestCase2(unittest.TestCase):
    """Tests the calculate_total_savings method with empty patients_list"""

    def setUp(self):
        self._office = Office(x=0, y=0)
        self._nurse = Nurse(1)
        self._problem = Problem(self._office, [], [self._nurse])
        self._round = Round([], self._problem, self._nurse)

    def test_calculate_total_savings_empty_list(self):
        self.assertEqual(self._round.total_savings, 0)

    def test_calculate_total_savings_one_patient(self):
        self._patient = Patient(x=1, y=0, duration_of_care=1000)
        self._problem = Problem(self._office, [self._patient], [self._nurse])
        self._problem.costs_matrix = np.zeros((2, 2))
        self._problem.costs_matrix[0, 1] = 1000
        self._problem.costs_matrix[1, 0] = 1000
        self._round = Round([self._patient], self._problem, self._nurse)
        self.assertEqual(self._round.total_savings, 0)

    def test_calculate_total_savings_two_patients(self):
        self._patients_list = [Patient(x=1, y=0, duration_of_care=1000), Patient(x=2, y=0, duration_of_care=1000)]
        self._problem = Problem(self._office, self._patients_list, [self._nurse])
        self._problem.costs_matrix = np.zeros((3, 3))
        self._problem.costs_matrix[0][1] = 1000
        self._problem.costs_matrix[1][0] = 1000
        self._problem.costs_matrix[0][2] = 2000
        self._problem.costs_matrix[2][0] = 2000
        self._problem.costs_matrix[1][2] = 1000
        self._problem.costs_matrix[2][1] = 1000
        self._round = Round(self._patients_list, self._problem, self._nurse)
        self.assertEqual(self._round.total_savings, 2000)

    def test_calculate_total_savings_five_patients(self):
        self._patients_list = [Patient(x=1, y=0, duration_of_care=1000), Patient(x=2, y=0, duration_of_care=1000),
                               Patient(x=3, y=0, duration_of_care=1000), Patient(x=4, y=0, duration_of_care=1000)]
        self._problem = Problem(self._office, self._patients_list, [self._nurse])
        self._problem.costs_matrix = np.zeros((5, 5))
        self._problem.costs_matrix[0][1] = 1000
        self._problem.costs_matrix[1][0] = 1000
        self._problem.costs_matrix[0][2] = 2000
        self._problem.costs_matrix[2][0] = 2000
        self._problem.costs_matrix[0][3] = 3000
        self._problem.costs_matrix[3][0] = 3000
        self._problem.costs_matrix[0][4] = 4000
        self._problem.costs_matrix[4][0] = 4000
        self._problem.costs_matrix[1][2] = 1000
        self._problem.costs_matrix[2][1] = 1000
        self._problem.costs_matrix[1][3] = 2000
        self._problem.costs_matrix[3][1] = 2000
        self._problem.costs_matrix[1][4] = 3000
        self._problem.costs_matrix[4][1] = 3000
        self._problem.costs_matrix[2][3] = 1000
        self._problem.costs_matrix[3][2] = 1000
        self._problem.costs_matrix[2][4] = 2000
        self._problem.costs_matrix[4][2] = 2000
        self._problem.costs_matrix[3][4] = 1000
        self._problem.costs_matrix[4][3] = 1000
        self._round = Round(self._patients_list, self._problem, self._nurse)
        self.assertEqual(self._round.total_savings, 12000)

    def test_calculate_total_savings_two_patients_with_precise_time_constraint(self):
        self._patients_list = [Patient(x=1, y=0, duration_of_care=1000),
                               Patient(x=2, y=0, duration_of_care=1000, must_be_visited_exactly_at=10000)]
        self._problem = Problem(self._office, self._patients_list, [self._nurse])
        self._problem.costs_matrix = np.zeros((3, 3))
        self._problem.costs_matrix[0][1] = 1000
        self._problem.costs_matrix[1][0] = 1000
        self._problem.costs_matrix[0][2] = 2000
        self._problem.costs_matrix[2][0] = 2000
        self._problem.costs_matrix[1][2] = 1000
        self._problem.costs_matrix[2][1] = 1000
        self._round = Round(self._patients_list, self._problem, self._nurse)
        self.assertEqual(self._round.total_savings, 0)

    def test_calculate_total_savings_five_patients_with_precise_time_constraint(self):
        self._patients_list = [Patient(x=1, y=0, duration_of_care=1000), Patient(x=2, y=0, duration_of_care=1000,
                                                                                 must_be_visited_exactly_at=5000),
                               Patient(x=3, y=0, duration_of_care=1000), Patient(x=4, y=0, duration_of_care=1000)]
        self._problem = Problem(self._office, self._patients_list, [self._nurse])
        self._problem.costs_matrix = np.zeros((5, 5))
        self._problem.costs_matrix[0][1] = 1000
        self._problem.costs_matrix[1][0] = 1000
        self._problem.costs_matrix[0][2] = 2000
        self._problem.costs_matrix[2][0] = 2000
        self._problem.costs_matrix[0][3] = 3000
        self._problem.costs_matrix[3][0] = 3000
        self._problem.costs_matrix[0][4] = 4000
        self._problem.costs_matrix[4][0] = 4000
        self._problem.costs_matrix[1][2] = 1000
        self._problem.costs_matrix[2][1] = 1000
        self._problem.costs_matrix[1][3] = 2000
        self._problem.costs_matrix[3][1] = 2000
        self._problem.costs_matrix[1][4] = 3000
        self._problem.costs_matrix[4][1] = 3000
        self._problem.costs_matrix[2][3] = 1000
        self._problem.costs_matrix[3][2] = 1000
        self._problem.costs_matrix[2][4] = 2000
        self._problem.costs_matrix[4][2] = 2000
        self._problem.costs_matrix[3][4] = 1000
        self._problem.costs_matrix[4][3] = 1000
        self._round = Round(self._patients_list, self._problem, self._nurse)
        self.assertEqual(self._round.total_savings, 10000)


class RoundTestCase3(unittest.TestCase):
    """Tests can_merge_left and can_merge_right"""

    def setUp(self):
        self._p = []
        for i in range(10):
            self._p.append(Patient())
        self._n = [Nurse(1), Nurse(2)]
        self._problem = Problem(Office(), self._p, self._n)
        self._problem.costs_matrix = np.zeros((11, 11))

    def test_can_merge_left(self):
        self.assertTrue(Round(patients_list=[self._p[1], self._p[2]], problem=self._problem, nurse=self._n[0])
            .can_merge_left(
            Round(patients_list=[self._p[3], self._p[4]], problem=self._problem, nurse=self._n[1])))
        self.assertTrue(Round(patients_list=[self._p[1], self._p[2]], problem=self._problem, nurse=self._n[0])
            .can_merge_left(
            Round(patients_list=[self._p[3], self._p[1]], problem=self._problem, nurse=self._n[1])))
        self.assertFalse(Round(patients_list=[self._p[1], self._p[2]], problem=self._problem, nurse=self._n[0])
            .can_merge_left(
            Round(patients_list=[self._p[3], self._p[4]], problem=self._problem, nurse=self._n[1]),
            force_common_patient=True))
        self.assertTrue(Round(patients_list=[self._p[1], self._p[2]], problem=self._problem, nurse=self._n[0])
            .can_merge_left(
            Round(patients_list=[self._p[3], self._p[1]], problem=self._problem, nurse=self._n[1]),
            force_common_patient=True))
        self.assertFalse(
            Round(patients_list=[self._p[1], self._p[2], self._p[4]], problem=self._problem, nurse=self._n[0])
            .can_merge_left(Round(patients_list=[self._p[3], self._p[4]], problem=self._problem, nurse=self._n[1])))

    def test_can_merge_right(self):
        self.assertTrue(Round(patients_list=[self._p[3], self._p[4]], problem=self._problem, nurse=self._n[1])
            .can_merge_right(
            Round(patients_list=[self._p[1], self._p[2]], problem=self._problem, nurse=self._n[0])))
        self.assertTrue(Round(patients_list=[self._p[3], self._p[1]], problem=self._problem, nurse=self._n[1])
            .can_merge_right(
            Round(patients_list=[self._p[1], self._p[2]], problem=self._problem, nurse=self._n[0])))
        self.assertFalse(Round(patients_list=[self._p[3], self._p[4]], problem=self._problem, nurse=self._n[1])
            .can_merge_right(
            Round(patients_list=[self._p[1], self._p[2]], problem=self._problem, nurse=self._n[0]),
            force_common_patient=True))
        self.assertTrue(Round(patients_list=[self._p[3], self._p[1]], problem=self._problem, nurse=self._n[1])
            .can_merge_right(
            Round(patients_list=[self._p[1], self._p[2]], problem=self._problem, nurse=self._n[0]),
            force_common_patient=True))
        self.assertFalse(
            Round(patients_list=[self._p[3], self._p[4]], problem=self._problem, nurse=self._n[1])
            .can_merge_right(
                Round(patients_list=[self._p[1], self._p[2], self._p[4]], problem=self._problem, nurse=self._n[0])))


class RoundTestCase4(unittest.TestCase):
    """Tests merge_left and merge_right"""

    def setUp(self):
        self._p = []
        for i in range(10):
            self._p.append(Patient())
        self._n = [Nurse(1), Nurse(2)]
        self._problem = Problem(Office(), self._p, self._n)
        self._problem.costs_matrix = np.zeros((11, 11))
        self._problem.costs_matrix[0][1] = 1000
        self._problem.costs_matrix[0][2] = 1000
        self._problem.costs_matrix[0][3] = 1000
        self._problem.costs_matrix[0][4] = 1000
        self._problem.costs_matrix[0][5] = 1000
        self._problem.costs_matrix[0][6] = 1000
        self._problem.costs_matrix[0][7] = 1000
        self._problem.costs_matrix[0][8] = 1000
        self._problem.costs_matrix[0][9] = 1000
        self._problem.costs_matrix[0][10] = 1000
        self._problem.costs_matrix[1][0] = 1000
        self._problem.costs_matrix[2][0] = 1000
        self._problem.costs_matrix[3][0] = 1000
        self._problem.costs_matrix[4][0] = 1000
        self._problem.costs_matrix[5][0] = 1000
        self._problem.costs_matrix[6][0] = 1000
        self._problem.costs_matrix[7][0] = 1000
        self._problem.costs_matrix[8][0] = 1000
        self._problem.costs_matrix[9][0] = 1000
        self._problem.costs_matrix[10][0] = 1000
        self._problem.costs_matrix[1][2] = 1000
        self._problem.costs_matrix[2][1] = 1000
        self._problem.costs_matrix[5][6] = 1000
        self._problem.costs_matrix[6][5] = 1000

    def test_merge_right_no_common(self):
        round1, round2 = Round([p for p in self._p[:5]], self._problem, self._n[0]), Round([p for p in self._p[5:]],
                                                                                           self._problem, self._n[1])
        round1.merge_right(round2)
        self.assertEqual(round1.patients_list, self._p)
        self.assertEqual(round1.total_cost, 4000)
        self.assertEqual(round1.total_savings, 16000)

    def test_merge_right_with_common(self):
        round1, round2 = Round([p for p in self._p[:5]], self._problem, self._n[0]), Round([p for p in self._p[4:]],
                                                                                           self._problem, self._n[1])
        round1.merge_right(round2)
        self.assertEqual(round1.patients_list, self._p)
        self.assertEqual(round1.total_cost, 4000)
        self.assertEqual(round1.total_savings, 16000)

    def test_merge_left_no_common(self):
        round1, round2 = Round([p for p in self._p[:5]], self._problem, self._n[0]), Round([p for p in self._p[5:]],
                                                                                           self._problem, self._n[1])
        round2.merge_left(round1)
        self.assertEqual(round2.patients_list, self._p)
        self.assertEqual(round2.total_cost, 4000)
        self.assertEqual(round2.total_savings, 16000)

    def test_merge_left_with_common(self):
        round1, round2 = Round([p for p in self._p[:5]], self._problem, self._n[0]), Round([p for p in self._p[4:]],
                                                                                           self._problem, self._n[1])
        round2.merge_left(round1)
        self.assertEqual(round2.patients_list, self._p)
        self.assertEqual(round2.total_cost, 4000)
        self.assertEqual(round2.total_savings, 16000)


class RoundTestCase5(unittest.TestCase):
    """Tests time_when_patient_visited method"""

    def setUp(self):
        self._p = [Patient(x=1, y=0, duration_of_care=1000),
                   Patient(x=2, y=0, duration_of_care=2000, must_be_visited_exactly_at=5000),
                   Patient(x=3, y=0, duration_of_care=3000)]
        self._n = [Nurse(1)]
        self._problem = Problem(Office(), self._p, self._n)
        self._problem.costs_matrix = np.zeros((4, 4))
        self._problem.costs_matrix[0][1] = 1000
        self._problem.costs_matrix[0][2] = 2000
        self._problem.costs_matrix[0][3] = 3000
        self._problem.costs_matrix[1][0] = 1000
        self._problem.costs_matrix[2][0] = 2000
        self._problem.costs_matrix[3][0] = 3000
        self._problem.costs_matrix[1][2] = 1000
        self._problem.costs_matrix[2][1] = 1000
        self._problem.costs_matrix[1][3] = 2000
        self._problem.costs_matrix[3][1] = 2000
        self._problem.costs_matrix[2][3] = 1000
        self._problem.costs_matrix[3][2] = 1000

    def test_time(self):
        round1 = Round(self._p[:], self._problem, self._n[0])
        round2 = Round([self._p[(i + 1) % 3] for i in range(3)], self._problem, self._n[0])
        self.assertEqual(round1.time_when_patient_visited(self._p[0]), 1000)
        self.assertEqual(round1.time_when_patient_visited(self._p[1]), 5000)
        self.assertEqual(round1.time_when_patient_visited(self._p[2]), 8000)
        self.assertEqual(round2.time_when_patient_visited(self._p[0]), 13000)
        self.assertEqual(round2.time_when_patient_visited(self._p[1]), 5000)
        self.assertEqual(round2.time_when_patient_visited(self._p[2]), 8000)


class RoundTestCase6(unittest.TestCase):
    """Tests can_be_assigned_to method"""

    def setUp(self):
        self._p = [Patient(x=1, y=0, duration_of_care=1000),
                   Patient(x=2, y=0, duration_of_care=2000, must_be_visited_exactly_at=5000),
                   Patient(x=3, y=0, duration_of_care=3000)]
        self._n = [Nurse(1, 0, 10000), Nurse(2, 4000, 10000), Nurse(3, 0, 14000), Nurse(4, 0, 20000)]
        self._problem = Problem(Office(), self._p, self._n)
        self._problem.costs_matrix = np.zeros((4, 4))
        self._problem.costs_matrix[0][1] = 1000
        self._problem.costs_matrix[0][2] = 2000
        self._problem.costs_matrix[0][3] = 3000
        self._problem.costs_matrix[1][0] = 1000
        self._problem.costs_matrix[2][0] = 2000
        self._problem.costs_matrix[3][0] = 3000
        self._problem.costs_matrix[1][2] = 1000
        self._problem.costs_matrix[2][1] = 1000
        self._problem.costs_matrix[1][3] = 2000
        self._problem.costs_matrix[3][1] = 2000
        self._problem.costs_matrix[2][3] = 1000
        self._problem.costs_matrix[3][2] = 1000

    def test_can_be_assigned_to(self):
        round1 = Round(self._p[:], self._problem, self._n[3])
        round2 = Round([self._p[(i + 1) % 3] for i in range(3)], self._problem, self._n[3])
        self.assertFalse(round1.can_be_assigned_to(self._n[0]))
        self.assertFalse(round1.can_be_assigned_to(self._n[1]))
        self.assertTrue(round1.can_be_assigned_to(self._n[2]))
        self.assertFalse(round2.can_be_assigned_to(self._n[0]))
        self.assertFalse(round2.can_be_assigned_to(self._n[1]))
        self.assertFalse(round2.can_be_assigned_to(self._n[2]))


class SolutionTestCase(unittest.TestCase):
    """Tests calculate_total_cost and calculate_total_savings methods of class Solution"""

    def setUp(self):
        self._office = Office(x=0, y=0)
        self._n = [Nurse(1), Nurse(2)]
        self._patients_list = [Patient(x=1, y=0, duration_of_care=1000), Patient(x=2, y=0, duration_of_care=1000,
                                                                                 must_be_visited_exactly_at=5000),
                               Patient(x=3, y=0, duration_of_care=1000), Patient(x=4, y=0, duration_of_care=1000)]
        self._problem = Problem(self._office, self._patients_list, self._n)
        self._problem.costs_matrix = np.zeros((5, 5))
        self._problem.costs_matrix[0][1] = 1000
        self._problem.costs_matrix[1][0] = 1000
        self._problem.costs_matrix[0][2] = 2000
        self._problem.costs_matrix[2][0] = 2000
        self._problem.costs_matrix[0][3] = 3000
        self._problem.costs_matrix[3][0] = 3000
        self._problem.costs_matrix[0][4] = 4000
        self._problem.costs_matrix[4][0] = 4000
        self._problem.costs_matrix[1][2] = 1000
        self._problem.costs_matrix[2][1] = 1000
        self._problem.costs_matrix[1][3] = 2000
        self._problem.costs_matrix[3][1] = 2000
        self._problem.costs_matrix[1][4] = 3000
        self._problem.costs_matrix[4][1] = 3000
        self._problem.costs_matrix[2][3] = 1000
        self._problem.costs_matrix[3][2] = 1000
        self._problem.costs_matrix[2][4] = 2000
        self._problem.costs_matrix[4][2] = 2000
        self._problem.costs_matrix[3][4] = 1000
        self._problem.costs_matrix[4][3] = 1000
        rounds_list = [Round(self._patients_list[:2], self._problem, self._n[0]),
                       Round(self._patients_list[2:], self._problem, self._n[1])]
        self._solution = Solution(rounds_list=rounds_list)

    def test_total_cost(self):
        self.assertEqual(self._solution.total_cost, 18000)

    def test_total_savings(self):
        self.assertEqual(self._solution.total_savings, 6000)


class ProblemTestCase1(unittest.TestCase):
    """Tests generate_random_patients method with amount=0"""

    def setUp(self):
        self._problem = Problem(Office(), nurses_list=[Nurse(1)])
        self._problem.generate_random_patients(amount=0)

    def test_generate_random_patients0(self):
        self.assertEqual(0, len(self._problem.patients_list))

    def test_generate_random_patients10(self):
        self._problem = Problem(Office(), nurses_list=[Nurse(1)])
        self._problem.generate_random_patients(amount=10, x=(1, 10), y=(2, 5), duration_of_care=(1000, 10000))
        self.assertEqual(10, len(self._problem.patients_list))
        for patient in self._problem.patients_list:
            coordinates = patient.address.split(",")
            self.assertTrue(1 <= float(coordinates[0]) < 10 and 2 < float(coordinates[1]) < 5)
            self.assertTrue(1000 <= patient.duration_of_care <= 10000)


class ProblemTestCase2(unittest.TestCase):
    """Tests query_api method"""
    def setUp(self):
        self._problem = Problem(Office(address="officeaddress"), [Patient(address="patient" + str(i))
                                                                  for i in range(1, 6)], [Nurse(1)])
        self._url1 = self._problem.query_api(0, 0, 0, 0)
        self._url2 = self._problem.query_api(0, 3, 0, 0)
        self._url3 = self._problem.query_api(0, 0, 0, 3)
        self._url4 = self._problem.query_api(1, 3, 0, 0)
        self._url5 = self._problem.query_api(0, 0, 1, 3)
        self._url6 = self._problem.query_api(0, 6, 0, 6)
        self._url7 = self._problem.query_api(0, 10, 0, 10)
        self._url8 = self._problem.query_api(-1, -2, -3, -4)

    def test_query_api(self):
        self.assertEqual("https://maps.googleapis.com/maps/api/distancematrix/json?origins=&destinations=&key=" + KEY,
                         self._url1)
        self.assertEqual("https://maps.googleapis.com/maps/api/distancematrix/json?origins=officeaddress"
                         "|patient1|patient2&destinations=&key=" + KEY, self._url2)
        self.assertEqual("https://maps.googleapis.com/maps/api/distancematrix/json?origins=&destinations="
                         "officeaddress|patient1|patient2&key=" + KEY, self._url3)
        self.assertEqual("https://maps.googleapis.com/maps/api/distancematrix/json?origins="
                         "patient1|patient2|patient3&destinations=&key=" + KEY, self._url4)
        self.assertEqual("https://maps.googleapis.com/maps/api/distancematrix/json?origins=&destinations="
                         "patient1|patient2|patient3&key=" + KEY, self._url5)
        self.assertEqual("https://maps.googleapis.com/maps/api/distancematrix/json?origins="
                         "officeaddress|patient1|patient2|patient3|patient4|patient5&destinations="
                         "officeaddress|patient1|patient2|patient3|patient4|patient5&key=" + KEY,
                         self._url6)
        self.assertEqual("https://maps.googleapis.com/maps/api/distancematrix/json?origins="
                         "officeaddress|patient1|patient2|patient3|patient4|patient5&destinations="
                         "officeaddress|patient1|patient2|patient3|patient4|patient5&key=" + KEY,
                         self._url7)
        self.assertEqual("https://maps.googleapis.com/maps/api/distancematrix/json?origins=&destinations=&key=" + KEY,
                         self._url8)


class ProblemTestCase3(unittest.TestCase):
    """Tests generate_rectangles method with empty list of patients"""
    def setUp(self):
        self._problem = Problem(Office(), [], [Nurse(1)])

    def test_generate_rectangles0(self):
        self.assertEqual(self._problem.generate_rectangles(), [])

    def test_generate_rectangles1(self):
        self._problem = Problem(Office(), [Patient()], [Nurse(1)])
        self.assertEqual(self._problem.generate_rectangles(), [(0, 2, 0, 2)])

    def test_generate_rectangles5(self):
        self._problem = Problem(Office(), [Patient() for i in range(5)], [Nurse(1)])
        self.assertEqual(self._problem.generate_rectangles(), [(0, 6, 0, 6)])

    def test_generate_rectangles9(self):
        self._problem = Problem(Office(), [Patient() for i in range(9)], [Nurse(1)])
        self.assertEqual(self._problem.generate_rectangles(), [(0, 10, 0, 10)])

    def test_generate_rectangles10(self):
        self._problem = Problem(Office(), [Patient() for i in range(10)], [Nurse(1)])
        self.assertEqual(self._problem.generate_rectangles(), [(0, 9, 0, 11), (9, 2, 0, 11)])

    def test_generate_rectangles22(self):
        self._problem = Problem(Office(), [Patient() for i in range(22)], [Nurse(1)])
        self.assertEqual(self._problem.generate_rectangles(), [(0, 4, 0, 23), (4, 4, 0, 23), (8, 4, 0, 23),
                                                               (12, 4, 0, 23), (16, 4, 0, 23), (20, 3, 0, 23)])

    def test_generate_rectangles50(self):
        self._problem = Problem(Office(), [Patient() for i in range(50)], [Nurse(1)])
        with self.assertRaises(ValueError):
            self._problem.generate_rectangles()

    def test_generate_rectangles49(self):
        self._problem = Problem(Office(), [Patient() for i in range(49)], [Nurse(1)])
        self._problem.generate_rectangles()


class ProblemTestCase4(unittest.TestCase):
    """Tests calculate_cost_matrix"""
    def setUp(self):
        self._problem = Problem(Office(address="Paris"), [Patient(address="Marseille")], [Nurse(1)])

    def test_calculate_cost_matrix(self):
        self._problem.calculate_cost_matrix()
        self.assertEqual(0, self._problem.costs_matrix[0][0])
        self.assertTrue(self._problem.costs_matrix[0][1] > 20000)  # not possible to know exactly the value since
        # googlemaps API takes the state of traffic in account for example
        self.assertTrue(self._problem.costs_matrix[1][0] > 20000)
        self.assertEqual(0, self._problem.costs_matrix[1][1])

    def test_calculate_cost_matrix2(self):
        self._problem = Problem(Office(address="Paris"), [Patient(address="Marseille") for i in range(10)], [Nurse(1)])
        self._problem.calculate_cost_matrix()
        for i in range(self._problem.number_of_patients() + 1):
            for j in range(self._problem.number_of_patients() + 1):
                if (i == 0 and j != 0) or (j == 0 and i != 0):
                    self.assertTrue(
                        self._problem.costs_matrix[i][j] > 20000)  # not possible to know exactly the value since
                    # googlemaps API takes the state of traffic in account for example
                else:
                    self.assertEqual(0, self._problem.costs_matrix[i][j])

    def test_calculate_cost_matrix3(self):
        self._problem = Problem(Office(address="azerty"), [Patient(address="Marseille") for i in range(10)], [Nurse(1)])
        with self.assertRaises(AttributeError):
            self._problem.calculate_cost_matrix()


class SolverTestCase1(unittest.TestCase):
    """Tests calculate_savings_matrix"""
    def setUp(self):
        self._problem = Problem(Office(), [], [Nurse(1)])
        self._problem.costs_matrix = np.zeros((1, 1))
        self._solver = Solver(self._problem)

    def test_calculate_savings_matrix(self):
        self.assertEqual(self._solver.calculate_savings_matrix().shape, (0, 0))

    def test_calculate_savings_matrix2(self):
        self._problem = Problem(Office(), [Patient()], [Nurse(1)])
        self._problem.costs_matrix = np.zeros((2, 2))
        self._problem.costs_matrix[0, 1] = 1000
        self._problem.costs_matrix[1, 0] = 1000
        self._solver = Solver(self._problem)
        savings_matrix = self._solver.calculate_savings_matrix()
        self.assertEqual(savings_matrix.shape, (1, 1))
        self.assertEqual(savings_matrix[0, 0], 0)

    def test_calculate_savings_matrix3(self):
        self._problem = Problem(Office(), [Patient(), Patient()], [Nurse(1)])
        self._problem.costs_matrix = np.zeros((3, 3))
        self._problem.costs_matrix[0, 1] = 1000
        self._problem.costs_matrix[1, 0] = 1000
        self._problem.costs_matrix[0, 2] = 2000
        self._problem.costs_matrix[2, 0] = 2000
        self._problem.costs_matrix[1, 2] = 1000
        self._problem.costs_matrix[2, 1] = 1000
        self._solver = Solver(self._problem)
        savings_matrix = self._solver.calculate_savings_matrix()
        self.assertEqual(savings_matrix.shape, (2, 2))
        self.assertEqual(savings_matrix[0, 0], 0)
        self.assertEqual(savings_matrix[0, 1], 2000)
        self.assertEqual(savings_matrix[1, 0], 2000)
        self.assertEqual(savings_matrix[1, 1], 0)


class SolverTestCase2(unittest.TestCase):
    """Tests clarke_and_wright_init"""
    def setUp(self):
        self._problem = Problem(Office(), [Patient(), Patient(), Patient()], [Nurse(1)])
        self._problem.costs_matrix = np.zeros((4, 4))
        self._problem.costs_matrix[0, 1] = 1000
        self._problem.costs_matrix[1, 0] = 1000
        self._problem.costs_matrix[0, 2] = 2000
        self._problem.costs_matrix[2, 0] = 2000
        self._problem.costs_matrix[0, 3] = 3000
        self._problem.costs_matrix[3, 0] = 3000
        self._problem.costs_matrix[1, 2] = 1000
        self._problem.costs_matrix[2, 1] = 1000
        self._problem.costs_matrix[1, 3] = 2000
        self._problem.costs_matrix[3, 1] = 2000
        self._problem.costs_matrix[2, 3] = 1000
        self._problem.costs_matrix[3, 2] = 1000
        self._solver = Solver(self._problem)

    def test_clarke_and_wright_init(self):
        self._solver.clarke_and_wright_init()
        self.assertEqual(self._solver._sorted_savings, [0, 0, 0, 2000, 2000, 2000, 2000, 4000, 4000])


class SolverTestCase3(unittest.TestCase):
    """Tests get_patient_pair_from_arg"""
    def setUp(self):
        self._problem = Problem(Office(), [Patient(), Patient(), Patient()], [Nurse(1)])
        self._solver = Solver(self._problem)

    def test_get_patients_pair_from_arg(self):
        patient_a0, patient_b0 = self._solver.get_patients_pair_from_arg(0)
        patient_a1, patient_b1 = self._solver.get_patients_pair_from_arg(1)
        patient_a2, patient_b2 = self._solver.get_patients_pair_from_arg(2)
        patient_a6, patient_b6 = self._solver.get_patients_pair_from_arg(6)
        self.assertTrue(patient_a0 is patient_b0 is self._problem.patients_list[0])
        self.assertTrue(patient_a1 is self._problem.patients_list[0] and patient_b1 is self._problem.patients_list[1])
        self.assertTrue(patient_a2 is self._problem.patients_list[0] and patient_b2 is self._problem.patients_list[2])
        self.assertTrue(patient_a6 is self._problem.patients_list[2] and patient_b6 is self._problem.patients_list[0])


class SolverTestCase4(unittest.TestCase):
    """Tests search_rounds_for_patient static method"""
    def setUp(self):
        self._patient_a, self._patient_b, self._patient_c, self._patient_d, self._patient_e = \
            Patient(), Patient(), Patient(), Patient(), Patient()
        self._problem = Problem(Office(), [self._patient_a, self._patient_b, self._patient_c, self._patient_d,
                                           self._patient_e], [Nurse(1), Nurse(2)])
        self._problem.costs_matrix = np.zeros((6, 6))
        self._round1 = Round([self._patient_a, self._patient_b, self._patient_c], self._problem,
                             self._problem.nurses_list[0])
        self._round2 = Round([self._patient_d, self._patient_e], self._problem, self._problem.nurses_list[1])
        self._rounds_list = [self._round1, self._round2]

    def test_search_rounds_for_patient(self):
        self.assertIs(self._round1, Solver.search_rounds_for_patient(self._patient_a, self._rounds_list, True, True,
                                                                     True))
        self.assertIs(self._round1, Solver.search_rounds_for_patient(self._patient_a, self._rounds_list, True, False,
                                                                     False))
        self.assertIs(self._round1, Solver.search_rounds_for_patient(self._patient_a, self._rounds_list, True, True,
                                                                     False))
        self.assertIs(None, Solver.search_rounds_for_patient(self._patient_a, self._rounds_list, False, True,
                                                                     True))
        self.assertIs(self._round1, Solver.search_rounds_for_patient(self._patient_b, self._rounds_list, True, True,
                                                                     True))
        self.assertIs(self._round1, Solver.search_rounds_for_patient(self._patient_b, self._rounds_list, False, True,
                                                                     False))
        self.assertIs(None, Solver.search_rounds_for_patient(self._patient_b, self._rounds_list, True, False,
                                                                     False))


class SolverTestCase5(unittest.TestCase):
    """Tests add_round_if_possible static method"""
    def setUp(self):
        self._office = Office(x=0, y=0)
        self._n = [Nurse(1, start_time=0, availability=10000), Nurse(2, start_time=0, availability=10000),
                   Nurse(3, start_time=0, availability=10000)]
        self._patients_list = [Patient(x=1, y=0, duration_of_care=1000), Patient(x=2, y=0, duration_of_care=1000,
                                                                                 must_be_visited_exactly_at=5000),
                               Patient(x=3, y=0, duration_of_care=1000), Patient(x=4, y=0, duration_of_care=1000),
                               Patient(x=5, y=0, duration_of_care=1000), Patient(x=6, y=0, duration_of_care=1000)]
        self._problem = Problem(self._office, self._patients_list, self._n)
        self._problem.costs_matrix = np.zeros((7, 7))
        self._problem.costs_matrix[0][1] = 1000
        self._problem.costs_matrix[1][0] = 1000
        self._problem.costs_matrix[0][2] = 2000
        self._problem.costs_matrix[2][0] = 2000
        self._problem.costs_matrix[0][3] = 3000
        self._problem.costs_matrix[3][0] = 3000
        self._problem.costs_matrix[0][4] = 4000
        self._problem.costs_matrix[4][0] = 4000
        self._problem.costs_matrix[0][5] = 5000
        self._problem.costs_matrix[5][0] = 5000
        self._problem.costs_matrix[0][6] = 6000
        self._problem.costs_matrix[6][0] = 6000
        self._problem.costs_matrix[1][2] = 1000
        self._problem.costs_matrix[2][1] = 1000
        self._problem.costs_matrix[1][3] = 2000
        self._problem.costs_matrix[3][1] = 2000
        self._problem.costs_matrix[1][4] = 3000
        self._problem.costs_matrix[4][1] = 3000
        self._problem.costs_matrix[1][5] = 4000
        self._problem.costs_matrix[5][1] = 4000
        self._problem.costs_matrix[1][6] = 5000
        self._problem.costs_matrix[6][1] = 5000
        self._problem.costs_matrix[2][3] = 1000
        self._problem.costs_matrix[3][2] = 1000
        self._problem.costs_matrix[2][4] = 2000
        self._problem.costs_matrix[4][2] = 2000
        self._problem.costs_matrix[2][5] = 3000
        self._problem.costs_matrix[5][2] = 3000
        self._problem.costs_matrix[2][6] = 4000
        self._problem.costs_matrix[6][2] = 4000
        self._problem.costs_matrix[3][4] = 1000
        self._problem.costs_matrix[4][3] = 1000
        self._problem.costs_matrix[3][5] = 2000
        self._problem.costs_matrix[5][3] = 2000
        self._problem.costs_matrix[3][6] = 3000
        self._problem.costs_matrix[6][3] = 3000
        self._problem.costs_matrix[4][5] = 1000
        self._problem.costs_matrix[5][4] = 1000
        self._problem.costs_matrix[4][6] = 2000
        self._problem.costs_matrix[6][4] = 2000
        self._problem.costs_matrix[5][6] = 1000
        self._problem.costs_matrix[6][5] = 1000

    def test_add_round_if_possible(self):
        self._rounds_list = [Round([self._patients_list[0], self._patients_list[1]], self._problem, self._n[0]),
                             Round([self._patients_list[2], self._patients_list[3]], self._problem, self._n[1])]
        new_round = Round([self._patients_list[4], self._patients_list[5]], self._problem, self._n[2])
        Solver.add_round_if_possible(new_round, self._rounds_list, self._problem)
        self.assertNotIn(new_round, self._rounds_list)

    def test_add_round_if_possible2(self):
        self._n.append(Nurse(4, start_time=0, availability=20000))
        self._rounds_list = [Round([self._patients_list[0], self._patients_list[1]], self._problem, self._n[0]),
                             Round([self._patients_list[2], self._patients_list[3]], self._problem, self._n[1])]
        new_round = Round([self._patients_list[4], self._patients_list[5]], self._problem, self._n[2])
        Solver.add_round_if_possible(new_round, self._rounds_list, self._problem)
        self.assertIn(new_round, self._rounds_list)
        self.assertIs(new_round.nurse, self._n[3])


class SolverTestCase6(unittest.TestCase):
    """Tests add_merged_round_if_possible static method"""
    def setUp(self):
        self._office = Office(x=0, y=0)
        self._n = [Nurse(1, start_time=0, availability=10000), Nurse(2, start_time=0, availability=11000),
                   Nurse(3, start_time=0, availability=10000), Nurse(4, start_time=0, availability=20000)]
        self._patients_list = [Patient(x=1, y=0, duration_of_care=1000), Patient(x=2, y=0, duration_of_care=1000,
                                                                                 must_be_visited_exactly_at=5000),
                               Patient(x=3, y=0, duration_of_care=1000), Patient(x=4, y=0, duration_of_care=1000),
                               Patient(x=5, y=0, duration_of_care=1000), Patient(x=6, y=0, duration_of_care=1000)]
        self._problem = Problem(self._office, self._patients_list, self._n)
        self._problem.costs_matrix = np.zeros((7, 7))
        self._problem.costs_matrix[0][1] = 1000
        self._problem.costs_matrix[1][0] = 1000
        self._problem.costs_matrix[0][2] = 2000
        self._problem.costs_matrix[2][0] = 2000
        self._problem.costs_matrix[0][3] = 3000
        self._problem.costs_matrix[3][0] = 3000
        self._problem.costs_matrix[0][4] = 4000
        self._problem.costs_matrix[4][0] = 4000
        self._problem.costs_matrix[0][5] = 5000
        self._problem.costs_matrix[5][0] = 5000
        self._problem.costs_matrix[0][6] = 6000
        self._problem.costs_matrix[6][0] = 6000
        self._problem.costs_matrix[1][2] = 1000
        self._problem.costs_matrix[2][1] = 1000
        self._problem.costs_matrix[1][3] = 2000
        self._problem.costs_matrix[3][1] = 2000
        self._problem.costs_matrix[1][4] = 3000
        self._problem.costs_matrix[4][1] = 3000
        self._problem.costs_matrix[1][5] = 4000
        self._problem.costs_matrix[5][1] = 4000
        self._problem.costs_matrix[1][6] = 5000
        self._problem.costs_matrix[6][1] = 5000
        self._problem.costs_matrix[2][3] = 1000
        self._problem.costs_matrix[3][2] = 1000
        self._problem.costs_matrix[2][4] = 2000
        self._problem.costs_matrix[4][2] = 2000
        self._problem.costs_matrix[2][5] = 3000
        self._problem.costs_matrix[5][2] = 3000
        self._problem.costs_matrix[2][6] = 4000
        self._problem.costs_matrix[6][2] = 4000
        self._problem.costs_matrix[3][4] = 1000
        self._problem.costs_matrix[4][3] = 1000
        self._problem.costs_matrix[3][5] = 2000
        self._problem.costs_matrix[5][3] = 2000
        self._problem.costs_matrix[3][6] = 3000
        self._problem.costs_matrix[6][3] = 3000
        self._problem.costs_matrix[4][5] = 1000
        self._problem.costs_matrix[5][4] = 1000
        self._problem.costs_matrix[4][6] = 2000
        self._problem.costs_matrix[6][4] = 2000
        self._problem.costs_matrix[5][6] = 1000
        self._problem.costs_matrix[6][5] = 1000

    def test_add_merged_round_if_possible(self):
        self._rounds_list = [Round([self._patients_list[0], self._patients_list[1]], self._problem, self._n[0]),
                             Round([self._patients_list[2], self._patients_list[3]], self._problem, self._n[3])]
        merged_round = Round([self._patients_list[2], self._patients_list[3], self._patients_list[4]],
                             self._problem, self._n[2])
        Solver.add_merged_round_if_possible(merged_round, self._rounds_list[1], self._rounds_list, self._problem)
        self.assertIn(merged_round, self._rounds_list)
        self.assertIs(merged_round.nurse, self._n[3])
        self.assertEqual(2, len(self._rounds_list))

    def test_add_merged_round_if_possible2(self):
        self._rounds_list = [Round([self._patients_list[0], self._patients_list[1]], self._problem, self._n[0]),
                             Round([self._patients_list[2], self._patients_list[3]], self._problem, self._n[1])]
        merged_round = Round([self._patients_list[2], self._patients_list[3], self._patients_list[4]],
                             self._problem, self._n[2])
        Solver.add_merged_round_if_possible(merged_round, self._rounds_list[1], self._rounds_list, self._problem)
        self.assertIn(merged_round, self._rounds_list)
        self.assertIs(merged_round.nurse, self._n[3])
        self.assertEqual(2, len(self._rounds_list))

    def test_add_merged_round_if_possible3(self):
        self._n.pop(-1)
        self._rounds_list = [Round([self._patients_list[0], self._patients_list[1]], self._problem, self._n[0]),
                             Round([self._patients_list[2], self._patients_list[3]], self._problem, self._n[1])]
        merged_round = Round([self._patients_list[2], self._patients_list[3], self._patients_list[4]],
                             self._problem, self._n[2])
        Solver.add_merged_round_if_possible(merged_round, self._rounds_list[1], self._rounds_list, self._problem)
        self.assertNotIn(merged_round, self._rounds_list)
        self.assertEqual(2, len(self._rounds_list))


class SolverTestCase7(unittest.TestCase):
    """Tests merge_rounds_if_possible static method"""
    def setUp(self):
        self._office = Office(x=0, y=0)
        self._n = [Nurse(1, start_time=0, availability=10000), Nurse(2, start_time=0, availability=11000),
                   Nurse(3, start_time=0, availability=10000), Nurse(4, start_time=0, availability=20000)]
        self._patients_list = [Patient(x=1, y=0, duration_of_care=1000), Patient(x=2, y=0, duration_of_care=1000,
                                                                                 must_be_visited_exactly_at=5000),
                               Patient(x=3, y=0, duration_of_care=1000), Patient(x=4, y=0, duration_of_care=1000),
                               Patient(x=5, y=0, duration_of_care=1000), Patient(x=6, y=0, duration_of_care=1000)]
        self._problem = Problem(self._office, self._patients_list, self._n)
        self._problem.costs_matrix = np.zeros((7, 7))
        self._problem.costs_matrix[0][1] = 1000
        self._problem.costs_matrix[1][0] = 1000
        self._problem.costs_matrix[0][2] = 2000
        self._problem.costs_matrix[2][0] = 2000
        self._problem.costs_matrix[0][3] = 3000
        self._problem.costs_matrix[3][0] = 3000
        self._problem.costs_matrix[0][4] = 4000
        self._problem.costs_matrix[4][0] = 4000
        self._problem.costs_matrix[0][5] = 5000
        self._problem.costs_matrix[5][0] = 5000
        self._problem.costs_matrix[0][6] = 6000
        self._problem.costs_matrix[6][0] = 6000
        self._problem.costs_matrix[1][2] = 1000
        self._problem.costs_matrix[2][1] = 1000
        self._problem.costs_matrix[1][3] = 2000
        self._problem.costs_matrix[3][1] = 2000
        self._problem.costs_matrix[1][4] = 3000
        self._problem.costs_matrix[4][1] = 3000
        self._problem.costs_matrix[1][5] = 4000
        self._problem.costs_matrix[5][1] = 4000
        self._problem.costs_matrix[1][6] = 5000
        self._problem.costs_matrix[6][1] = 5000
        self._problem.costs_matrix[2][3] = 1000
        self._problem.costs_matrix[3][2] = 1000
        self._problem.costs_matrix[2][4] = 2000
        self._problem.costs_matrix[4][2] = 2000
        self._problem.costs_matrix[2][5] = 3000
        self._problem.costs_matrix[5][2] = 3000
        self._problem.costs_matrix[2][6] = 4000
        self._problem.costs_matrix[6][2] = 4000
        self._problem.costs_matrix[3][4] = 1000
        self._problem.costs_matrix[4][3] = 1000
        self._problem.costs_matrix[3][5] = 2000
        self._problem.costs_matrix[5][3] = 2000
        self._problem.costs_matrix[3][6] = 3000
        self._problem.costs_matrix[6][3] = 3000
        self._problem.costs_matrix[4][5] = 1000
        self._problem.costs_matrix[5][4] = 1000
        self._problem.costs_matrix[4][6] = 2000
        self._problem.costs_matrix[6][4] = 2000
        self._problem.costs_matrix[5][6] = 1000
        self._problem.costs_matrix[6][5] = 1000

    def test_merge_rounds_if_possible(self):
        self._rounds_list = [Round([self._patients_list[0], self._patients_list[1]], self._problem, self._n[0]),
                             Round([self._patients_list[2], self._patients_list[3]], self._problem, self._n[3])]
        Solver.merge_rounds_if_possible(self._rounds_list[0], self._rounds_list[1], self._rounds_list, self._problem)
        self.assertEqual(1, len(self._rounds_list))
        self.assertIs(self._rounds_list[0].nurse, self._n[-1])

    def test_merge_rounds_if_possible2(self):
        self._rounds_list = [Round([self._patients_list[0], self._patients_list[1]], self._problem, self._n[0]),
                             Round([self._patients_list[2], self._patients_list[3]], self._problem, self._n[1])]
        Solver.merge_rounds_if_possible(self._rounds_list[0], self._rounds_list[1], self._rounds_list, self._problem)
        self.assertEqual(1, len(self._rounds_list))
        self.assertIs(self._rounds_list[0].nurse, self._n[-1])

    def test_merge_rounds_if_possible3(self):
        self._n.pop(-1)
        self._rounds_list = [Round([self._patients_list[0], self._patients_list[1]], self._problem, self._n[0]),
                             Round([self._patients_list[2], self._patients_list[3]], self._problem, self._n[1])]
        Solver.merge_rounds_if_possible(self._rounds_list[0], self._rounds_list[1], self._rounds_list, self._problem)
        self.assertEqual(2, len(self._rounds_list))


class SolverTestCase8(unittest.TestCase):
    """Tests parallel_build_rounds method"""
    def setUp(self):
        self._office = Office(x=0, y=0)
        self._n = [Nurse(1, start_time=0, availability=10000), Nurse(2, start_time=0, availability=11000),
                   Nurse(3, start_time=0, availability=10000), Nurse(4, start_time=0, availability=40000)]
        self._patients_list = [Patient(x=1, y=0, duration_of_care=1000), Patient(x=2, y=0, duration_of_care=1000,
                                                                                 must_be_visited_exactly_at=5000),
                               Patient(x=3, y=0, duration_of_care=1000), Patient(x=4, y=0, duration_of_care=1000),
                               Patient(x=5, y=0, duration_of_care=1000), Patient(x=6, y=0, duration_of_care=1000)]
        self._problem = Problem(self._office, self._patients_list, self._n)
        self._problem.costs_matrix = np.zeros((7, 7))
        self._problem.costs_matrix[0][1] = 1000
        self._problem.costs_matrix[1][0] = 1000
        self._problem.costs_matrix[0][2] = 2000
        self._problem.costs_matrix[2][0] = 2000
        self._problem.costs_matrix[0][3] = 3000
        self._problem.costs_matrix[3][0] = 3000
        self._problem.costs_matrix[0][4] = 4000
        self._problem.costs_matrix[4][0] = 4000
        self._problem.costs_matrix[0][5] = 5000
        self._problem.costs_matrix[5][0] = 5000
        self._problem.costs_matrix[0][6] = 6000
        self._problem.costs_matrix[6][0] = 6000
        self._problem.costs_matrix[1][2] = 1000
        self._problem.costs_matrix[2][1] = 1000
        self._problem.costs_matrix[1][3] = 2000
        self._problem.costs_matrix[3][1] = 2000
        self._problem.costs_matrix[1][4] = 3000
        self._problem.costs_matrix[4][1] = 3000
        self._problem.costs_matrix[1][5] = 4000
        self._problem.costs_matrix[5][1] = 4000
        self._problem.costs_matrix[1][6] = 5000
        self._problem.costs_matrix[6][1] = 5000
        self._problem.costs_matrix[2][3] = 1000
        self._problem.costs_matrix[3][2] = 1000
        self._problem.costs_matrix[2][4] = 2000
        self._problem.costs_matrix[4][2] = 2000
        self._problem.costs_matrix[2][5] = 3000
        self._problem.costs_matrix[5][2] = 3000
        self._problem.costs_matrix[2][6] = 4000
        self._problem.costs_matrix[6][2] = 4000
        self._problem.costs_matrix[3][4] = 1000
        self._problem.costs_matrix[4][3] = 1000
        self._problem.costs_matrix[3][5] = 2000
        self._problem.costs_matrix[5][3] = 2000
        self._problem.costs_matrix[3][6] = 3000
        self._problem.costs_matrix[6][3] = 3000
        self._problem.costs_matrix[4][5] = 1000
        self._problem.costs_matrix[5][4] = 1000
        self._problem.costs_matrix[4][6] = 2000
        self._problem.costs_matrix[6][4] = 2000
        self._problem.costs_matrix[5][6] = 1000
        self._problem.costs_matrix[6][5] = 1000
        self._solver = Solver(self._problem)

    def test_parallel_build_rounds(self):
        self._solver.clarke_and_wright_init()
        rounds_list = self._solver.parallel_build_rounds()
        self.assertEqual(len(rounds_list), 1)
        self.assertIs(rounds_list[0].nurse, self._n[-1])

    def test_parallel_build_rounds2(self):
        self._problem.nurses_list[-1] = Nurse(4, start_time=0, availability=15000)
        self._solver.clarke_and_wright_init()
        rounds_list = self._solver.parallel_build_rounds()
        self.assertEqual(len(rounds_list), 2)


class SolverTestCase9(unittest.TestCase):
    """Tests add_single_patient_rounds method"""
    def setUp(self):
        self._office = Office(x=0, y=0)
        self._n = [Nurse(1, start_time=0, availability=10000), Nurse(2, start_time=0, availability=11000),
                   Nurse(3, start_time=0, availability=10000), Nurse(4, start_time=0, availability=40000)]
        self._patients_list = [Patient(x=1, y=0, duration_of_care=1000), Patient(x=2, y=0, duration_of_care=1000,
                                                                                 must_be_visited_exactly_at=5000),
                               Patient(x=3, y=0, duration_of_care=1000), Patient(x=4, y=0, duration_of_care=1000),
                               Patient(x=5, y=0, duration_of_care=1000), Patient(x=6, y=0, duration_of_care=1000)]
        self._problem = Problem(self._office, self._patients_list, self._n)
        self._problem.costs_matrix = np.zeros((7, 7))
        self._problem.costs_matrix[0][1] = 1000
        self._problem.costs_matrix[1][0] = 1000
        self._problem.costs_matrix[0][2] = 2000
        self._problem.costs_matrix[2][0] = 2000
        self._problem.costs_matrix[0][3] = 3000
        self._problem.costs_matrix[3][0] = 3000
        self._problem.costs_matrix[0][4] = 4000
        self._problem.costs_matrix[4][0] = 4000
        self._problem.costs_matrix[0][5] = 5000
        self._problem.costs_matrix[5][0] = 5000
        self._problem.costs_matrix[0][6] = 6000
        self._problem.costs_matrix[6][0] = 6000
        self._problem.costs_matrix[1][2] = 1000
        self._problem.costs_matrix[2][1] = 1000
        self._problem.costs_matrix[1][3] = 2000
        self._problem.costs_matrix[3][1] = 2000
        self._problem.costs_matrix[1][4] = 3000
        self._problem.costs_matrix[4][1] = 3000
        self._problem.costs_matrix[1][5] = 4000
        self._problem.costs_matrix[5][1] = 4000
        self._problem.costs_matrix[1][6] = 5000
        self._problem.costs_matrix[6][1] = 5000
        self._problem.costs_matrix[2][3] = 1000
        self._problem.costs_matrix[3][2] = 1000
        self._problem.costs_matrix[2][4] = 2000
        self._problem.costs_matrix[4][2] = 2000
        self._problem.costs_matrix[2][5] = 3000
        self._problem.costs_matrix[5][2] = 3000
        self._problem.costs_matrix[2][6] = 4000
        self._problem.costs_matrix[6][2] = 4000
        self._problem.costs_matrix[3][4] = 1000
        self._problem.costs_matrix[4][3] = 1000
        self._problem.costs_matrix[3][5] = 2000
        self._problem.costs_matrix[5][3] = 2000
        self._problem.costs_matrix[3][6] = 3000
        self._problem.costs_matrix[6][3] = 3000
        self._problem.costs_matrix[4][5] = 1000
        self._problem.costs_matrix[5][4] = 1000
        self._problem.costs_matrix[4][6] = 2000
        self._problem.costs_matrix[6][4] = 2000
        self._problem.costs_matrix[5][6] = 1000
        self._problem.costs_matrix[6][5] = 1000
        self._solver = Solver(self._problem)
        self._rounds_list = [Round(self._patients_list[:-1], self._problem, self._n[-1])]

    def test_add_single_patient_rounds(self):
        self._solver.add_single_patient_rounds(self._rounds_list)
        self.assertEqual(1, len(self._rounds_list))

    def test_add_single_patient_rounds2(self):
        self._problem.nurses_list[0] = Nurse(1, start_time=0, availability=20000)
        self._solver.add_single_patient_rounds(self._rounds_list)
        self.assertEqual(2, len(self._rounds_list))
        self.assertIs(self._rounds_list[-1].nurse, self._n[0])


if __name__ == '__main__':
    unittest.main()
