from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pycountry

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
        'IvoryCoast',
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
            print(get_country_from_string(population))
            file.write(population + "\n")

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