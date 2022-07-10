import requests
import bs4
import pandas as pd
from tqdm import tqdm

def parse_url(url):
    r = requests.get(url)
    page = bs4.BeautifulSoup(r.text, "html.parser")

    # Components or sensors
    componments = []
    power = ''
    connectivity = ''
    compatibility = ''
    for a in page.find_all("a"):
        if "/wearables/device-categories/components" in str(a):
            componments.append(a.text)

        if "/wearables/device-categories/power" in str(a):
            power = a.text

        if "connectivity" in str(a):
            connectivity =  a.text
        
        if "compatibility" in str(a):
            compatibility = a.text

    #Price  // float or No Announcement Yet
    price = ''
    price_div_list = page.find_all("div", class_="span3")
    price_div = []
    for div in price_div_list:
        price_div.extend(div)

    #print(price_div)
    for i in range(len(price_div)):
        if "Price" in str(price_div[i]):
            price = price_div[i+2].text.strip()    
            if "USD" in price or "EUR" in price or "CAD" in price or "GBP" in price:
                price = price[1:-3].strip()
                continue
            if "No Announcement Yet" in price:
                price = None



    #Body location & Primary Application
    body_location_div = list(page.find("div", class_="span4"))
    body_location = ''
    primary_application = ''
    #print(body_location_div)
    for i in range(len(body_location_div)):
        if "Body Location" in str(body_location_div[i]):
            body_location = body_location_div[i+2].text
        if 'Primary Application' in str(body_location_div[i]):
            primary_application = body_location_div[i+2].text
            
    # Company and device name
    company_list = page.find_all("div", class_="span3")
    company_div = []
    company = ''
    device_name = ''
    for div in company_list:
        company_div.extend(div)
    for i in range(len(company_div)):
        if "Company" in company_div[i]:
            company = company_div[i+2].text.strip()
        if "Device Name" in company_div[i]:
            device_name = company_div[i+2].text.strip()

    df_dict = {'Device_name':device_name, 'Company':company, 'Price':price, 'Body_location':body_location, 'Components':','.join(componments), 'Power':power, 'Connectivity':connectivity, 'Compatibility':compatibility, 'Primary_Application':primary_application}
    
    return df_dict

def get_url_list():
    url = "https://vandrico.com/wearables/list.html"
    r = requests.get(url)
    page = bs4.BeautifulSoup(r.text, "html.parser")

    website_list = []
    website_name = [] 
    all_devices = page.find("div", class_="row-fluid margin-120")
    devices = all_devices.find_all("div")
    for device in devices:
        for div in device.find_all("div"):
            for li in div.find("ul").find_all("li"):
                for data in li:
                    website_list.append(url[:-20] + data["href"])
                    website_name.append(data.text)
    return website_list

url_list = get_url_list()

to_csv_dict = {}

label_list = ['Device_name', 'Company', 'Price', 'Body_location', 'Components', 'Power', 'Connectivity', 'Compatibility', 'Primary_Application']

for label in label_list:
    to_csv_dict[label] = []

for i in tqdm(range(1, len(url_list))):
    if i == 353 or i == 419 or i == 422 or i == 424 or i == 428:
        continue
    data_dict = parse_url(url_list[i])

    for label in label_list:
        to_csv_dict[label].append(data_dict[label])
    #print(i, data_dict, url_list[i])

print(len(to_csv_dict))

df = pd.DataFrame.from_dict(to_csv_dict)
df.to_csv('neo4j_import.csv')