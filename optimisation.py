import math
import numpy as np
import random
import requests as req


def generate_random_clients(nb, xmin, xmax, ymin, ymax):
    return [(random.random() * (xmax - xmin) + xmin, random.random() * (ymax - ymin) + ymin, i) for i in range(nb+1)]


def calculate_cost_matrix(listOfPatientsWithOrigin):
    mat_dim = len(listOfPatientsWithOrigin)
    cost_matrix = np.zeros((mat_dim, mat_dim))
    for i in range(1, mat_dim) :  # costs from client i to client j
        for j in range(1, mat_dim) :
            cost_matrix[i,j] = distance(listOfPatientsWithOrigin[i][0],listOfPatientsWithOrigin[i][1],listOfPatientsWithOrigin[j][0],listOfPatientsWithOrigin[j][1])
    return cost_matrix


def calculate_savings_matrix(listOfPatientsWithOrigin):
    mat_dim = len(listOfPatientsWithOrigin) - 1
    savings_matrix = np.zeros((mat_dim, mat_dim))
    cost_matrix = calculate_cost_matrix(listOfPatientsWithOrigin)
    for i in range(mat_dim) :
        for j in range(mat_dim):
            if i != j :
                savings_matrix[i,j] = cost_matrix[i+1, 0] + cost_matrix[0,j+1]- cost_matrix[i+1,j+1]
    return savings_matrix


def clarke_and_wright_init(listOfPatientsWithOrigin):
    savings_mat = calculate_savings_matrix(listOfPatientsWithOrigin)
    savings_flat = np.ndarray.flatten(savings_mat)
    arg_sorted_savings = np.argsort(savings_flat)
    sorted_savings = [savings_flat[i] for i in arg_sorted_savings]
    return sorted_savings, arg_sorted_savings


def _get_patients_pair_from_arg(patients_list, arg_k):
    number_of_patients = len(patients_list)
    client_i = arg_k // number_of_patients  # departure client
    client_j = arg_k % number_of_patients   # arrival client
    return patients_list[client_i], patients_list[client_j]


def _sequential_merge_if_possible(current_round, candidate_round):
    if(current_round[-1] == candidate_round[0]):
        current_round.append(candidate_round[1])
        return True
    else :
        return False


def sequential_build_deliveries(sorted_savings, arg_sorted_savings, patients_list):
    rounds_list = []
    n = len(sorted_savings)
    visited_patients = []   # list of the clients that are already in a round
    while len(visited_patients) != len(patients_list) :
        round = []
        i = 1
        while i <= n :
            number_of_delivered_clients = len(visited_patients)
            if round == []:   # a new round must be started. Two compatible clients must be found
                client_a, client_b = _get_patients_pair_from_arg(patients_list, arg_sorted_savings[n - i])   # arg_sorted_savings is sorted in the increasing order of savings, so the research begins at the end, which accounts for the n-i
                if client_a != client_b and not (client_a[2] in visited_patients) and not (client_b[2] in visited_patients) :  # if both clients are not delivered yet, and if they are compatible towards the max demand
                    round.append(client_a)   # both clients are added to the clients list
                    round.append(client_b)
                    visited_patients.append(client_a[2])   # they are added to the list of delivered clients
                    visited_patients.append(client_b[2])
                    i = 1   # the research restarts from the end of the sorted savings list
            else :   # two clients must be found : one that isn't in any round yet, and the other one must be in the current one
                client_a, client_b = _get_patients_pair_from_arg(patients_list, arg_sorted_savings[n - i])
                candidate_delivery = [client_a, client_b]   # this candidate will be merged to the current round if possible
                a_delivered, b_delivered = client_a[2] in visited_patients, client_b[2] in visited_patients
                if client_a != client_b and (not (a_delivered) or not (b_delivered)) :
                    if _sequential_merge_if_possible(round, candidate_delivery) :
                        if a_delivered :
                            visited_patients.append(client_b[2])
                        else :
                            visited_patients.append(client_a[2])
                        i = 1
            if len(visited_patients) == number_of_delivered_clients:
                i += 1
        if round == [] :
            break  # if the round is still empty after the preceding instructions, the algorithm can stop since it won't make new deliveries any more
        #round.update()
        rounds_list = rounds_list + [round]  # the new round is added to the deliveries list
    return rounds_list

def distance(x1, y1, x2, y2):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(x1) + "," + str(y1) + "&destinations=" + str(x2) + "," + str(y2) + "&key=AIzaSyC0eSQgRkKnFCo3gnu4UlPMDnpoLjwifso"
    return req.get(url).json().get("rows")[0].get("elements")[0].get("duration").get("value")

#print(distance(48, 2, 49, 3))


listOfPatients = generate_random_clients(10, 48, 49, 2, 3)
sorted_savings = clarke_and_wright_init(listOfPatients)[0]
arg_sorted_savings = clarke_and_wright_init(listOfPatients)[1]
L = sequential_build_deliveries(sorted_savings, arg_sorted_savings, listOfPatients[1:])[0]
print([client[2] for client in L])
print("optimized round cost :", sum([math.sqrt((L[i][0] - L[i+1][0])**2 + (L[i][1] - L[i+1][1])**2) for i in range(len(L)-1)]) + math.sqrt((L[0][0] - listOfPatients[0][0]) ** 2 + (L[0][1] - listOfPatients[0][1]) ** 2) + math.sqrt((L[len(L) - 1][0] - listOfPatients[0][0]) ** 2 + (L[len(L) - 1][1] - listOfPatients[0][1]) ** 2))
print("without optimization", sum([math.sqrt((listOfPatients[i][0] - listOfPatients[i + 1][0]) ** 2 + (listOfPatients[i][1] - listOfPatients[i + 1][1]) ** 2) for i in range(len(listOfPatients) - 1)]) + math.sqrt((listOfPatients[len(listOfPatients) - 1][0] - listOfPatients[0][0]) ** 2 + (listOfPatients[len(listOfPatients) - 1][1] - listOfPatients[0][1]) ** 2))


