from requests import get, HTTPError


#Chatenay-Malabry
Ad1 = 'Chatenay-Malabry'
#Arcueil
Ad2 = 'Arcueil'
#Sceaux
Ad3 = 'Antony'
Ad4 = 'Gif-sur-Yvette'
Ad5 = 'Bures-sur-Yvette'


def google_api_search(DepartArrivee, WaypointList):
    """
    :param DepartArrivee: Adresse de départ de l'infirmier
    :param WaypointList: Liste d'adresses à visiter
    :return: Un fichier json
    """
    text_API = 'https://maps.googleapis.com/maps/api/directions/json?origin='+DepartArrivee+'&destination='+DepartArrivee+'&waypoints=optimize:true'
    for e in WaypointList :
        text_API = text_API+'|'+e
    text_API = text_API+'&key=AIzaSyBC6f_FfYW0nRxnGIb2kxzyd-Bjowix0tI'
    resp = get(text_API)
    if resp.status_code != 200:
        raise HTTPError('GET /tasks/ {}'.format(resp.status_code))
    result = resp.json()
    return result

def list_parcours_optimise(DepartArrivee, WaypointList):
    result = google_api_search(DepartArrivee, WaypointList)
    order = result.get('routes')[0].get('waypoint_order')
    list_res = [DepartArrivee]
    i=1
    for e in order :
        list_res.append(WaypointList[e])
        i = i+1
    list_res.append(DepartArrivee)
    return list_res

def list_temps_trajet(DepartArrivee, WaypointList) :
    result = google_api_search(DepartArrivee, WaypointList)
    list_leg = result.get('routes')[0].get('legs')
    list_res = []
    for e in list_leg :
        list_res.append(e.get('duration').get('text'))
    return list_res

def feuille_de_route(DepartArrivee, WaypointList):
    print("Bonjour, voici les étapes de votre journée :")
    list_villes = list_parcours_optimise(DepartArrivee, WaypointList)
    list_temps = list_temps_trajet(DepartArrivee, WaypointList)
    for i in range(0,list_temps.__len__()):
        print("Etape n°{} : {} -> {} | durée : {}".format(i+1,list_villes[i],list_villes[i+1],list_temps[i]))
    pass


List=[Ad2,Ad3,Ad4,Ad5]
feuille_de_route(Ad1,List)