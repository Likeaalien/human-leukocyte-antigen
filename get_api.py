import crawler
import os
import json
import requests

def api_url_test(url, retardinjo):
    request = requests.Request(
        "GET",
        url,
        params=retardinjo
    )
    prepared_request = request.prepare()

    print(prepared_request.url)

def api_country_population(country, population_id):
    allele_frequency_endpoint = "https://www.allelefrequencies.net/api/hla/allele-frequencies/search?"

    population_name = ""

    if not os.path.exists(crawler.hla_path):
        crawler.get_populations()

    with open(crawler.hla_path, "r", encoding="utf-8") as file:
        api_from_file = json.load(file)


    print(api_from_file.get(country))

    population_name = api_from_file.get(country)["populations"][population_id]["name"]
    print(population_name)

    api_value = country + " " + population_name
    params = {
        "country" : country,
        "population" : f"{api_value}"
    }

    api_url_test(allele_frequency_endpoint, params)

# response = requests.get(allele_frequency_endpoint, params=params)
# data = response.json()

country_input = input("Enter input here: ")
array_id = int(input("Which one you want to take out? "))
api_country_population(country_input, array_id)