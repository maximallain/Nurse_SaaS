API URLs : 

1 - http://127.0.0.1:8000/api/v1/nurses
Get the list of the nurses with their availabilities

2 - http://127.0.0.1:8000/api/v1/nurses/<officepk>/
Get the list of the nurses with their availabilities for a given office. 
Need to put the id of the office as a parameter.

3 - http://127.0.0.1:8000/api/v1/nurse/<nursepk>/
Get a specified nurse with his availabilites. The parameter is the id of the nurse.

4 - http://127.0.0.1:8000/api/v1/visits
Get the lists of the availabilities with their date and duration

5 - http://127.0.0.1:8000/api/v1/visits/?<date>?<officepk>
Get the lists of the availabilities with their date and duration
Format of date : "2017-1_12"
Can put parameters date and officepk

6 - http://127.0.0.1:8000/api/v1/visit/<visitpk>/
Get a specified visit. The parameter is the id of the visit.

7 -POST http://127.0.0.1:8000/api/v1/visits/create
Post a list of visits to update nurse_pk and start_time to the visit object.
Json expected in the body : 
[{"visit_pk":111, "nurse_pk":9, "time":"05:10"},{"visit_pk":112, "nurse_pk":8, "time":"10:10"}]