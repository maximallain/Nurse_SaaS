import datetime
from flask import request
from flask_api import FlaskAPI

from algo import *

app = FlaskAPI(__name__)
days = ["M", "T", "W", "Th", "F", "S", "Su"]


@app.route("/optimize", methods=["GET"])
def launch_optimizer():
    """
    Launches the optimization of tomorrow visits for the specified office (parameter officepk in request)
    :return: a dummy empty string
    """
    args = request.args
    office_pk = args["officepk"]
    date = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    day_of_week = days[int(datetime.datetime.strptime(date, '%Y-%m-%d').weekday())]
    # récuperer l'adresse de l'office, des patients à visiter à la date donnée (avec chacun leur adresse),
    # ainsi que les nurses et leurs disponibilités
    nurses_list = []
    print(office_pk, date)
    nurses_of_office = req.request("GET", "http://127.0.0.1:8000/api/v1/nurses/" + office_pk + "/").json()
    for nurse in nurses_of_office:
        availabilities = nurse.get("intervals").get(day_of_week)
        if availabilities is not None:
            for interval in availabilities:
                start, end = interval.get("real_start_time"), interval.get("real_end_time")
                start_seconds, end_seconds = 3600 * int(start.split(":")[0]) + 60 * int(start.split(":")[1]), \
                                             3600 * int(end.split(":")[0]) + 60 * int(end.split(":")[1])
                nurses_list.append(Nurse(nurse.get("pk"), start_seconds, end_seconds - start_seconds))
                print(nurses_list[-1])
    office = Office(address=(nurses_of_office[0].get("office").get("adress")))
    print(office)
    patients_list = []
    visits = req.request("GET", "http://127.0.0.1:8000/api/v1/visits/?officepk=" + office_pk + "&date=" + date).json()
    for patient in visits:
        new_patient = Patient(address=patient.get("soin").get("patient").get("adresse"),
                                     duration_of_care=patient.get("duration_visit"), pk=patient.get("pk"))
        specific_visit_time = patient.get("soin").get("specific_visit_time")
        if specific_visit_time is not None:
            must_be_visited_exactly_at = \
                3600 * int(specific_visit_time.split(":")[0]) + 60 * int(specific_visit_time.split(":")[1])
            new_patient.must_be_visited_exactly_at = must_be_visited_exactly_at
        patients_list.append(new_patient)
        print(patients_list[-1])
    problem = Problem(office, patients_list, nurses_list)
    solver = Solver(problem)
    solver.compute_clarke_and_wright("Parallel")
    solution = problem.solutions_list[-1]
    visits_summary = []
    for rnd in solution.rounds_list:
        for patient in rnd.patients_list:
            time_when_visited = rnd.time_when_patient_visited(patient)
            print(time_when_visited)
            visits_summary.append({"visit_pk": patient.pk, "nurse_pk": rnd.nurse.pk,
                                   "time": str(int(time_when_visited) // 3600) + ':' + str(
                                       (int(time_when_visited) % 3600) // 60)})
    print(visits_summary)
    req.post("http://127.0.0.1:8000/api/v1/visits/create", json=visits_summary)
    return ""


if __name__ == "__main__":
    app.run(debug=True)
