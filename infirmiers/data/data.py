#File to create automatically datas in database

#Need to create manually the cabinet

from random import randint
from random import uniform
from .place import Place
from datetime import timedelta, date

from nurses_app.models.nurse import Nurse
from nurses_app.models.interval import Interval
from patients_app.models.Patients import Patient
from patients_app.models.soins import Soin
from signUp.models.office import Office

weekday = ["M", "T", "W", "Th", "F", "S", "Su"]
FN = ["Alexandre","Max", "Pierre", "Baudouin", "Matthieu", "Quentin"]
LN = ["Sioufi", "Allain", "Léger", "Coco", "Hello","Marcel"]
PN = ["0000000000", "0000000001", "0000000002", "0000000003", "0000000004", "0000000005"]


def create_nurse_to_db(firstname, lastname, gender, phonenumber):
    office = Office.objects.filter(user_id = 8 )[0]
    A = Nurse(FirstName = firstname, LastName = lastname, Gender=gender, PhoneNumber=phonenumber, office=office)
    A.save()
    return A

def create_interval_to_db(starttime, endtime, week_day):
    A = Interval(start_time = starttime, end_time = endtime, weekday = week_day)
    A.save()
    return A

def create_patient_to_db(LastName, FirstName, Adress, PhoneNumber, Email):
    office = Office.objects.filter(user_id = 8 )[0]
    A = Patient(LastName = LastName, FirstName = FirstName, Adress = Adress, PhoneNumber = PhoneNumber,Email = Email, office = office)
    A.save()
    return A

def create_soin_to_db(name_soin):
    start_date = date.today() + timedelta(days=1)
    type_soin = "SID"
    frequence_soin = ["0", "1", "2", "3", "4", "5", "6"]
    soin =  Soin(name_soin=name_soin,
                 type_soin = type_soin,
                 frequence_soin = frequence_soin,
                 start_date=start_date,
                 )
    soin.save()
    return soin

    

def random_place_in_paris():
    """return a random location in Paris"""
    MAX_LAT = 48.87
    MIN_LAT = 48.84
    MAX_LNG = 2.295
    MIN_LNG = 2.285

    rand_lat = uniform(MIN_LAT, MAX_LAT)
    rand_lng = uniform(MIN_LNG, MAX_LNG)
    return Place(lat=rand_lat, lng=rand_lng)

#We will create the following intervals: 10:00-14:00, 14:00-18:00, 18:00-22:00 for each day

def main_nurses():
    #Create the nurses
    L = []
    for i in range(len(FN)):
        A = create_nurse_to_db(FN[i],LN[i],"M",PN[i])
        L.append(A)

    #Create the intervals and associate it to the nurses
    I1 = create_interval_to_db(40, 56, "M")
    L[0].intervals.add(I1)
    I2 = create_interval_to_db(56, 72, "M")
    L[1].intervals.add(I2)
    I3 = create_interval_to_db(72, 88, "M")
    L[2].intervals.add(I3)

    I4 = create_interval_to_db(40, 56, "T")
    L[3].intervals.add(I4)
    I5 = create_interval_to_db(56, 72, "T")
    L[4].intervals.add(I5)
    I6 = create_interval_to_db(72, 88, "T")
    L[5].intervals.add(I6)

    I7 = create_interval_to_db(40, 56, "W")
    L[1].intervals.add(I7)
    I8 = create_interval_to_db(56, 72, "W")
    L[0].intervals.add(I8)
    I9 = create_interval_to_db(72, 88, "W")
    L[2].intervals.add(I9)

    I10 = create_interval_to_db(40, 56, "Th")
    L[5].intervals.add(I10)
    I11 = create_interval_to_db(56, 72, "Th")
    L[3].intervals.add(I11)
    I12 = create_interval_to_db(72, 88, "Th")
    L[4].intervals.add(I12)

    I13 = create_interval_to_db(40, 56, "F")
    L[2].intervals.add(I13)
    I14 = create_interval_to_db(56, 72, "F")
    L[0].intervals.add(I14)
    I15 = create_interval_to_db(72, 88, "F")
    L[1].intervals.add(I15)

    I16 = create_interval_to_db(40, 56, "S")
    L[5].intervals.add(I16)
    I17 = create_interval_to_db(56, 72, "S")
    L[3].intervals.add(I17)
    I18 = create_interval_to_db(72, 88, "S")
    L[4].intervals.add(I18)

    I19 = create_interval_to_db(40, 56, "Su")
    L[1].intervals.add(I19)
    I20 = create_interval_to_db(56, 72, "Su")
    L[2].intervals.add(I20)
    I21 = create_interval_to_db(72, 88, "Su")
    L[0].intervals.add(I21)

def main_patients():
    #Create the nurses
    for i in range(0,30):
        LastName = "Patient" + str(i)
        FirstName = "Patient" + str(i)
        PhoneNumber = str(randint(1000000000, 9999999999))
        Email = "email" + str(i) + "@gmail.com"
        Adress = random_place_in_paris().address
        patient = create_patient_to_db(LastName, FirstName, Adress, PhoneNumber, Email)

        name_soin = "Soin" + str(i)
        soin = create_soin_to_db(name_soin)

        patient.treatments.add(soin)


    






    




