import get_api

country_input = input("Enter input here: ")
validated_input = get_api.input_validation(country_input)

if validated_input is None:
    print("Invalid input, try again")
else:
    array_id = int(input("Which one you want to take out? "))
    get_api.api_country_population(validated_input, array_id)