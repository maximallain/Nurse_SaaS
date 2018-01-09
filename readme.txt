Description:
This application lets offices of nurses to handle nurses, patients, cares, and to optimize the journeys of the nurses.

Pre-requesite:
1/ Install the latest version of Python 3.6 (be sure that pip is installed on your machine)
2/ Install django, requests, django-multiselectfield, djangorestframework and flask with `pip install -r requirements.txt`


Download the app:
1/ Install the repo git: git clone https://gitlab.centralesupelec.fr/projet-nimitz/Boudin.git

Steps to run the app:
1/ Go to the folder "infirmiers" via your terminal: cd infirmiers
2/ Run the following command via your terminal (to run the django app): python manage.py runserver
3/ Go to the folder "optimisation" via your terminal: cd optimisation
4/ Run the following command via your terminal (to run the optimizer): python optimizer_api
5/ Browse the following url: 127.0.0.1:8000/
