import crawler
import os
import json
import requests

def api_url_test(url, test):
    request = requests.Request(
        "GET",
        url,
        params=test
    )
    prepared_request = request.prepare()

    print(prepared_request.url)

def get_populations_from_file(country_name):
    if not os.path.exists(crawler.hla_path):
        crawler.get_populations()

    with open(crawler.hla_path, "r", encoding="utf-8") as file:
        api_from_file = json.load(file)

    if api_from_file.get(country_name) is None:
        return []

    return api_from_file.get(country_name)["populations"]

def request_allele_frequencies(country_name, population_name):
    if population_name == "NONAME":
        api_value = country_name
    else:
        api_value = country_name + " " + population_name
        
    allele_frequency_endpoint = "https://www.allelefrequencies.net/api/hla/allele-frequencies/search?"
    try:
        params = {
            "country" : country_name,
            "population" : f"{api_value}"
            }

        api_url_test(allele_frequency_endpoint, params)
        # TODO
    except Exception as e:
        print(f"Error while sending get request: {e}")

def input_validation(user_input):
    while not user_input:
        print("Invalid input, try again")
        user_input = input("Enter input here: ")
    
    if user_input and not user_input.isalpha():
        return None

    if not user_input[0].isupper():
        user_input = user_input.capitalize()

    return user_input



# response = requests.get(allele_frequency_endpoint, params=params)
# data = response.json()