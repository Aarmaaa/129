import csv

data = []

with open("archive_dataset.csv") as file:
    reader = csv.reader(file)
    for i in reader:
        data.append(i)

headers = data[0]
planet_data = data[1:]

#Converting all the planet names to lower case
for i in planet_data:
    i[2] = i[2].lower()

#Sorting the planet names in alphabetical order
planet_data.sort(key=lambda planet_data:planet_data[2])

with open("sorted.csv", "a+") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(planet_data)

#Removing the blank lines
with open("sorted.csv") as input, open("sorted_final.csv", "w", newline="") as output:
    writer = csv.writer(output)
    reader = csv.reader(input)

    for i in reader:
        if any(text.strip() for text in i):
            writer.writerow(i)
            