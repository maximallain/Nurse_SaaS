import requests as req
import datetime
from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions

from algo import *

app = FlaskAPI(__name__)
days = ["M", "T", "W", "Th", "F", "S", "Su"]


@app.route("/optimize", methods=["GET"])
def launch_optimizer():
    args = request.args
    office_pk = args["officepk"]
    date = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    day_of_week = days[int(datetime.datetime.strptime(date, '%Y-%m-%d').weekday())]
    # récuperer l'adresse de l'office, des patients à visiter à la date donnée (avec chacun leur adresse), ainsi que les nurses et leurs disponibilités
    nurses_list = []
    nurses_of_office = req.request("GET", "http://127.0.0.1:8000/api/v1/nurses/" + office_pk + "/").json()
    for nurse in nurses_of_office:
        for interval in nurse.get("intervals").get(day_of_week):
            start, end = interval.get("real_start_time"), interval.get("real_end_time")
            start_seconds, end_seconds = 3600*int(start.split(":")[0]) + 60*int(start.split(":")[1]), \
                                         3600*int(end.split(":")[0]) + 60*int(end.split(":")[1])
            nurses_list.append(Nurse(nurse.get("pk"), start_seconds, end_seconds - start_seconds))
    office = Office(address=(nurses_of_office[0].get("office").get("address")))
    patients_list = []
    visits = req.request("GET", "http://127.0.0.1:8000/api/v1/visits/" + office_pk + '/' + date + '/')
    for patient in visits:
        patients_list.append(Patient(address=patient.get("address"), duration_of_care=patient.get("duration")))
    problem = Problem(office, patients_list, nurses_list)
    solver = Solver(problem)
    solver.compute_clarke_and_wright("Parallel")
    solution = problem.solutions_list[-1]
    arg_sorted_round_costs = np.argsort([round.total_cost for round in solution.rounds_list])[::-1]
    arg_sorted_nurses_availabilities = np.argsort([nurse.availability for nurse in nurses_list])[::-1]
    visits_summary = []
    for i in range(min(len(nurses_list), len(solution.rounds_list))):
        nurse = nurses_list[arg_sorted_nurses_availabilities[i]]
        round = solution.rounds_list[arg_sorted_round_costs[i]]
        for patient in round.patients_list:
            time_when_visited = solution.time_when_patient_visited(patient, nurse, problem)
            visits_summary.append({"visit_pk": patient.pk, "nurse_pk": nurse.pk, "time": str(time_when_visited//3600) + ':' + str((time_when_visited%3600)//3600)})
    req.request("PUT", "http://127.0.0.1:8000/api/v1/visits", data=visits_summary)
    return ""


if __name__ == "__main__":
    app.run(debug=True)

