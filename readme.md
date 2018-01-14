# Description:
This application lets offices of nurses to handle nurses, patients, cares, and to optimize the journeys of the nurses.

# Pre-requesite:
- Install the latest version of Python 3.6 (be sure that pip is installed on your machine)
- Install python modules used for the project with :                     `pip install -r requirements.txt`


# Download the app:
Install the repo git: `git clone https://gitlab.centralesupelec.fr/projet-nimitz/Boudin.git`

# Steps to run the app:
- Go to the folder "infirmiers" via your terminal:                         `cd infirmiers`
- Run the following command via your terminal (to run the django app):     `python manage.py runserver`
- Go to the folder "optimisation" via your terminal:                       `cd optimisation`
- Run the following command via your terminal (to run the optimizer):      `python optimizer_api.py`
- Browse the following url: 127.0.0.1:8000/

*NB: To use the optimizer, you need a working internet connection (to retrieve distances from Google Maps API)*