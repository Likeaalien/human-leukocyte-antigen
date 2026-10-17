import crawler

crawler.site_status

hla_array = []

with open("local-db/hla_info.txt", "a+", encoding="utf-8") as file:
    file.seek(0)
    hla_array = file.read().splitlines()
print("Postojeci podaci", hla_array)

hla_population = input("Unesi prvi podatak: ")
hla_country = input("Unesi drugi podatak: ")
hla_info = hla_population + " " + hla_country
with open("local-db/hla_info.txt", "a", encoding="utf-8") as file:
    file.write(hla_population + " " + hla_country +"\n")

hla_array.append(hla_info)

for i in crawler.array:
    if i.strip() in hla_array:
        continue

    with open("local-db/hla_info.txt", "a", encoding="utf-8") as file:
        file.write(i)
    

print("Svi podaci", hla_array)