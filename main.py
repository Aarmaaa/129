from attr import attr
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

start_url = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome("chromedriver.exe")
browser.get(start_url)
time.sleep(10)

headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyper_link"]
planet_data = []

def scrape():

    #Loop for 203 pages
    for i in range(0, 203):
        while True:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source,"html.parser")

            #Checking the page Number
            currentPageNumber = int(soup.find_all("input",attrs={"class","page_num"})[0].get("value"))
            if currentPageNumber < i:
                browser.find_element('xpath', '//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif currentPageNumber > i:
                browser.find_element('xpath', '//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break
            
                        
        #Finding all the rows - ul tags with class = exoplanet - 25 iterations
        for ul_tag in soup.find_all("ul",attrs={"class","exoplanet"}):
            li_tags = ul_tag.find_all("li") #5 li tags

            temp_list = []
            for j, li_tag in enumerate(li_tags):
                if j == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")

            hyperlink = li_tags[0]
            temp_list.append("https://exoplanets.nasa.gov/"+hyperlink.find_all("a",href = True)[0]["href"])
            
            planet_data.append(temp_list)
        
        browser.find_element('xpath', '//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print("page "+str(i)+" scarping completed" )

scrape()

new_planets_data = []

def more_Data(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parser")
        temp_list = []
        for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div", attrs={"class":"value"})[0].contents[0])
                except:
                    temp_list.append("")
        
        new_planets_data.append(temp_list)
    
    except:
        time.sleep(1)
        more_Data(hyperlink)


for i, data in enumerate(planet_data):
    more_Data(data[5])
    print("scraping at hyperLink"+str(i+1))

print(new_planets_data[0: 10])

final_data = []
for i, data in enumerate(planet_data):
    new_item = new_planets_data[i]
    new_item = [item.replace("\n","") for item in new_item]
    new_item = new_item[:7]
    final_data.append(data+new_item)

with open("final.csv","w") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(final_data)