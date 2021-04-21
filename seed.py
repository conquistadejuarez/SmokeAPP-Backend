#!.venv/bin/python
import time
import csv
import json
import requests

base_url = "http://localhost:8888"


def seed_add_brand(name, pack_price, pack_quantity, model_strength):
    url = base_url + "/api/brands"

    payload = json.dumps(
        {
            "name": name,
            "pack_price": pack_price,
            "pack_quantity": pack_quantity,
            "model_strength": model_strength
        })

    headers = {
        'Content-Type': 'text/plain'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    assert (response.status_code == 200)

    return response


def seed_add_disease(name, description, disease_difficulty, time_to_recover):
    url = base_url + "/api/diseases"

    payload = json.dumps(
        {
            "name": name,
            "description": description,
            "disease_difficulty": disease_difficulty,
            "time_to_recover": time_to_recover,
        })

    headers = {
        'Content-Type': 'text/plain'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    assert (response.status_code == 200)

    return response


def do_seed():
    with open('csvFiles/brands.csv', 'r') as csv_file:
        csv_reader1 = csv.reader(csv_file)
        for line in csv_reader1:
            seed_add_brand(line[1], int(line[2]), int(line[3]), int(line[4]))

    with open('csvFiles/diseases.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            if not line:
                continue
            seed_add_disease(line[0], line[1], int(line[2]), int(line[3]))

import os

def kill_service():
    os.system("""ps aux | grep python | grep service.py | awk '{print "kill -9 "$2}' | bash""")

def create_database():
    user = 'milos123'
    # TODO: procitaj iz ajla


    os.system(f"""echo "drop database mb_users" | psql -U {user} template1""")
    os.system(f"""echo "create database mb_users" | psql -U {user} template1""")

def start_service():

    os.system('./service.py &')
    time.sleep(2)

if __name__ == '__main__':

    kill_service()
    create_database()
    start_service()

    do_seed()
    kill_service()


