import unittest
from algo import *


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
    """Tests the calculate_total_cost method with empty patients_list"""

    def setUp(self):
        self._office = Office(x=0, y=0)
        self._nurse = Nurse(1)
        self._problem = Problem(self._office, [], [self._nurse])
        self._round = Round([], self._problem, self._nurse)

    def test_empty_list(self):
        self.assertEqual(self._round.total_cost, 0)


class RoundTestCase2(unittest.TestCase):
    """Tests the calculate_total_cost method with 1 patient"""

    def setUp(self):
        self._office = Office(x=0, y=0)
        self._nurse = Nurse(1)
        self._patient = Patient(x=1, y=0, duration_of_care=1000)
        self._problem = Problem(self._office, [self._patient], [self._nurse])
        self._problem.costs_matrix = np.zeros((2, 2))
        self._problem.costs_matrix[0, 1] = 1000
        self._problem.costs_matrix[1, 0] = 1000
        self._round = Round([self._patient], self._problem, self._nurse)

    def test_one_patient(self):
        self.assertEqual(self._round.total_cost, 3000)


class RoundTestCase3(unittest.TestCase):
    """Tests the calculate_total_cost method with 2 patients"""

    def setUp(self):
        self._office = Office(x=0, y=0)
        self._nurse = Nurse(1)
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

    def test_two_patients(self):
        self.assertEqual(self._round.total_cost, 6000)


class RoundTestCase4(unittest.TestCase):
    """Tests the calculate_total_cost method with 5 patients"""

    def setUp(self):
        self._office = Office(x=0, y=0)
        self._nurse = Nurse(1)
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

    def test_five_patients(self):
        self.assertEqual(self._round.total_cost, 12000)


class RoundTestCase5(unittest.TestCase):
    """Tests the calculate_total_cost method with 2 patients, the 2nd one having a precise visit time constraint"""

    def setUp(self):
        self._office = Office(x=0, y=0)
        self._nurse = Nurse(1)
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

    def test_two_patients_with_precise_time_constraint(self):
        self.assertEqual(self._round.total_cost, 13000)


class RoundTestCase6(unittest.TestCase):
    """Tests the calculate_total_cost method with 5 patients, one having a precise time constraint"""

    def setUp(self):
        self._office = Office(x=0, y=0)
        self._nurse = Nurse(1)
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

    def test_five_patients(self):
        self.assertEqual(self._round.total_cost, 14000)


class RoundTestCase7(unittest.TestCase):
    """Tests the calculate_total_savings method with empty patients_list"""

    def setUp(self):
        self._office = Office(x=0, y=0)
        self._nurse = Nurse(1)
        self._problem = Problem(self._office, [], [self._nurse])
        self._round = Round([], self._problem, self._nurse)

    def test_empty_list(self):
        self.assertEqual(self._round.total_savings, 0)


class RoundTestCase8(unittest.TestCase):
    """Tests the calculate_total_savings method with 1 patient"""

    def setUp(self):
        self._office = Office(x=0, y=0)
        self._nurse = Nurse(1)
        self._patient = Patient(x=1, y=0, duration_of_care=1000)
        self._problem = Problem(self._office, [self._patient], [self._nurse])
        self._problem.costs_matrix = np.zeros((2, 2))
        self._problem.costs_matrix[0, 1] = 1000
        self._problem.costs_matrix[1, 0] = 1000
        self._round = Round([self._patient], self._problem, self._nurse)

    def test_one_patient(self):
        self.assertEqual(self._round.total_savings, 0)


class RoundTestCase9(unittest.TestCase):
    """Tests the calculate_total_savings method with 2 patients"""

    def setUp(self):
        self._office = Office(x=0, y=0)
        self._nurse = Nurse(1)
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

    def test_two_patients(self):
        self.assertEqual(self._round.total_savings, 2000)


class RoundTestCase10(unittest.TestCase):
    """Tests the calculate_total_savings method with 5 patients"""

    def setUp(self):
        self._office = Office(x=0, y=0)
        self._nurse = Nurse(1)
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

    def test_five_patients(self):
        self.assertEqual(self._round.total_savings, 12000)


class RoundTestCase11(unittest.TestCase):
    """Tests the calculate_total_savings method with 2 patients, the 2nd one having a precise visit time constraint"""

    def setUp(self):
        self._office = Office(x=0, y=0)
        self._nurse = Nurse(1)
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

    def test_two_patients(self):
        self.assertEqual(self._round.total_savings, 0)


class RoundTestCase12(unittest.TestCase):
    """Tests the calculate_total_savings method with 5 patients, one having a precise time constraint"""

    def setUp(self):
        self._office = Office(x=0, y=0)
        self._nurse = Nurse(1)
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

    def test_five_patients(self):
        self.assertEqual(self._round.total_savings, 10000)


class RoundTestCase13(unittest.TestCase):
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
            .can_merge_right(Round(patients_list=[self._p[1], self._p[2], self._p[4]], problem=self._problem,
                                   nurse=self._n[0])))


class RoundTestCase14(unittest.TestCase):
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


class RoundTestCase15(unittest.TestCase):
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


class RoundTestCase16(unittest.TestCase):
    """Tests can_be_assigned_to method"""
    def setUp(self):
        self._p = [Patient(x=1, y=0, duration_of_care=1000),
                   Patient(x=2, y=0, duration_of_care=2000, must_be_visited_exactly_at=5000),
                   Patient(x=3, y=0, duration_of_care=3000)]
        self._n = [Nurse(1, 0, 10000), Nurse(2, 4000, 10000), Nurse(3,0,14000), Nurse(4,0,20000)]
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
        round2 = Round([self._p[(i+1)%3] for i in range(3)], self._problem, self._n[3])
        self.assertFalse(round1.can_be_assigned_to(self._n[0]))
        self.assertFalse(round1.can_be_assigned_to(self._n[1]))
        self.assertTrue(round1.can_be_assigned_to(self._n[2]))
        self.assertFalse(round2.can_be_assigned_to(self._n[0]))
        self.assertFalse(round2.can_be_assigned_to(self._n[1]))
        self.assertFalse(round2.can_be_assigned_to(self._n[2]))


if __name__ == '__main__':
    unittest.main()
