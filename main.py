import sys
import get_api

country_input = input("Enter country here: ")
validated_input = get_api.input_validation(country_input)

if validated_input is None:
    print("Invalid input")
    sys.exit(1)

populations = get_api.get_populations_from_file(validated_input)
print(populations)

array_input = int(input("Enter popualtion index: "))
population_name = populations[array_input]["name"]

get_api.request_allele_frequencies(country_input, population_name)