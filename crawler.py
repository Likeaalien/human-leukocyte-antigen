import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.allelefrequencies.net/hla6006b.asp")
site_status = print("Aleles site:" , response.status_code)
soup = BeautifulSoup(response.text, "html.parser")

array = []

table = soup.select_one("table.table04")
table_element = table.select_one("select[name=\"hla_population\"]")
for element in table_element.select("option[value]:not([selected])"):
    array.append(element.text + "\n")
print(array)
