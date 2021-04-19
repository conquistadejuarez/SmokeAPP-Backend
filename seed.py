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


def seed_add_disease(name, description, disease_difficulty):
    url = base_url + "/api/diseases"

    payload = json.dumps(
        {
            "name": name,
            "description": description,
            "disease_difficulty": disease_difficulty
        })

    headers = {
        'Content-Type': 'text/plain'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    assert (response.status_code == 200)

    return response


if __name__ == '__main__':

    #  a = seed_add_brand('marlboro',200,20,10)
    #  a = seed_add_brand('best',200,20,10)

    with open('csvFiles/brands.csv', 'r') as csv_file:
        csv_reader1 = csv.reader(csv_file)
        for line in csv_reader1:
            seed_add_brand(line[1], int(line[2]), int(line[3]), int(line[4]))

    with open('csvFiles/diseases.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            if not line:
                continue
            seed_add_disease(line[1], line[2], int(line[3]))
