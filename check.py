from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pycountry

CONST_EMPTY_POPULATION_TEST = "NONAME"
api_populations = {}

# Extracts the country name from the given option
def get_country_from_string(text):
    countries = [country.name for country in pycountry.countries]
    countries.extend([
        'Azores',
        'Bolivia',
        'Borneo',
        'Cape Verde',
        'Cretan Islanders',
        'Czech Republic',
        'England',
        'Gaza',
        'Iran',
        'Ivory Coast',
        'Kosovo',
        'Macedonia',
        'Madeira',
        'Russia',
        'Sao Tome Island',
        'Scotland',
        'South Korea',
        'Tanzania',
        'Taiwan',
        'Turkey',
        'Trinidad',
        'USA',
        'Venezuela',
        'Vietnam',
        'Wales',
        'Western Samoa'])
    
    for country in countries:
        if text.lower().startswith(country.lower()):
            return country

    return None

# Append a parsed population to the api_populations dictionary
def api_populations_append(country, population_test, n_value):
    # Check whether the country exists in the dictionary, create it if it does not
    if country not in api_populations:
        api_populations[country] = {
            "populations": []
        }

    # Append the population name and sample size to the country's populations list
    api_populations[country]["populations"].append({
        "name" : CONST_EMPTY_POPULATION_TEST if population_test == "" else population_test,
        "n" : n_value
    })

# Extracts the population sample value, including parentheses, from the given option
def get_population_sample_value_from_string(text):
    return "(" + text.rsplit("(", 1)[1]

# Parses the given option and returns a tuple in the format (country, population_name, population_sample)
def parse_option(text):
    # (1st part) Extract the country name
    country = get_country_from_string(text)

    # (3rd part) Extract the population sample value
    population_sample = get_population_sample_value_from_string(text)
    n_value = "".join(character for character in population_sample if character.isdigit())

    # (2nd part) Extract the population name by removing the country name and population sample from the original text
    population_test = text.replace(country, "").replace(population_sample, "").strip()

    return (country, population_test, n_value)

def get_populations():
    url = "https://www.allelefrequencies.net/hla/classical-allele-frequency-search/"
    hla_path = "local-db/hla_info.txt"

    options = Options()
    options.binary_location = (
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    )

    # Create an instance of the browser
    driver = webdriver.Chrome(options=options)

    try:
        # Open a file to write the populations to
        file = open(hla_path, "w", encoding="utf-8")

        # Navigate the browser to the URL
        driver.get(url)

        # Wait for the population options to load
        WebDriverWait(driver, 30).until(
            lambda d:
                len(d.find_elements(By.CSS_SELECTOR, "#population option"))
            > 1 )

        # Parse the page source
        parsed_page = BeautifulSoup(driver.page_source, "html.parser")

        # Get a specific element from the parsed page
        table = parsed_page.select_one("#population")

        # Select each population option one by one
        for element in table.select("option"):
            population = element.get_text(strip = True)
            if (population == "All"):
                continue

            # Step 1: Parse the selected option
            (country, population_test, n_value) = parse_option(population)

            # Step 2: Append the parsed population to the dictionary
            api_populations_append(country, population_test, n_value)

    # Handle errors that occur when opening or writing to the file
    except OSError as e:
        print(f"Error while opening file: {e}")

    # Handle errors that occur when the page fails to load within the specified time
    except TimeoutException as e:
        print(f"Error while crawling: {e}")

    # Handle any other unexpected errors
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        driver.quit()

get_populations()