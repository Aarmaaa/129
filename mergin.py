import csv

data1 = []
data2 = []

with open("final.csv") as file :
    reader = csv.reader(file)
    for i in reader:
        data1.append(i)

with open("sorted_final.csv") as file :
    reader = csv.reader(file)
    for i in reader:
        data2.append(i)

headers1 = data1[0]
planetData1 = data1[1:]

headers2 = data2[0]
planetData2 = data2[1:]

headers = headers1 + headers2

planet_Data = []

for i, data in enumerate(planetData1):
    planet_Data.append(planetData1[i] + planetData2[i])

with open("merged.csv", "a+") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(planet_Data)