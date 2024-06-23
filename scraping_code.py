# WEBSCRAPING payhip
import requests
import json
from bs4 import BeautifulSoup

# Send an HTTP GET request to the website
url = "https://payhip.com/projectstartups/blog/vclist-online"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
response = requests.get(url, headers=headers)

dict_link ={}
company_places_dict = {}
main_dict = {}

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    vc_link_list = soup.find_all(class_='blog-post-name')
    for link in vc_link_list:
        link_value = link.find('a')['href']
        link_name = link.find('a').text
        dict_link[link_name] = link_value
    print(dict_link)
    for link_value in list(dict_link.keys()):
        print(dict_link[link_value])
        link_response = requests.get(dict_link[link_value], headers=headers)
        soup_link = BeautifulSoup(link_response.text, 'html.parser')
        body1 = soup_link.find(class_="blog-post-content")
        ul_element = body1.find('ul')
        list_items = ul_element.find_all('li')
        for item in list_items:
            try:
                company = item.get_text().split('-')[0].strip()
                places = item.get_text().split('-')[1].strip()
                company_places_dict[company] = places
                print(company,places)
            except Exception as e:
                print("Error:",str(e),item.get_text())
                
        lp = link_value.split('VC list')[0].strip()
        if lp == 'InsurTech':
            lp = 'Insurance'
        elif lp == 'RetailTech':
            lp = 'Retail'
        elif lp == 'AgTech':
            lp = 'Agriculture'
        elif lp == 'EdTech':
            lp = 'Education'
        elif lp == 'HRTech':
            lp = 'Human Resource'
        elif lp == 'MarTech':
            lp = 'Marketing'
        elif lp == 'Digital Health':
            lp = 'Health Hospitality'
        elif lp in ['Gaming','Cyber Security', 'Robotics', 'IoT', 'Blockchain', 'AI']:
            lp = 'Software Technology'
        if lp not in main_dict:
            main_dict[lp] = company_places_dict
        else:
            main_dict[lp].update(company_places_dict)
        company_places_dict = {}

    json_str = json.dumps(main_dict)
    with open('Main_dictionary.json', 'w') as output_file:
      json.dump(json_str, output_file, indent=4)
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")


#LinkedIN (API)
# Key gives us only  200 records per one Bearer Token

import requests
import json
import ast

url = "https://api.coresignal.com/cdapi/v1/linkedin/member/search/filter"

payload = json.dumps(
    {"title":"Venture capitalist","location":"United states"}
)
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJFZERTQSIsImtpZCI6IjZkOWY1MjMyLTdjOWUtMTM4OC1jNGMyLWZjYWRhOWJhZDk0YyJ9.eyJhdWQiOiJidWZmYWxvIiwiZXhwIjoxNzI2NTM4NDk2LCJpYXQiOjE2OTQ5ODE1NDQsImlzcyI6Imh0dHBzOi8vb3BzLmNvcmVzaWduYWwuY29tOjgzMDAvdjEvaWRlbnRpdHkvb2lkYyIsIm5hbWVzcGFjZSI6InJvb3QiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJidWZmYWxvIiwic3ViIjoiZmEwYzRjOWMtYzIxYy1mZmRmLWMwYjktNDhhZWQ1YWY5YzE2IiwidXNlcmluZm8iOnsic2NvcGVzIjoiY2RhcGkifX0.EypLu85leHLKwubXr-7kGL6q5oEoDEuZ4wLNy7Lt_xkIcuDy2VLRC02JWhFPxVFOMcTTMGErNkcePnG6xSlrDQ'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
list_ppl = response.text
data_list = ast.literal_eval(list_ppl)
print(len(data_list))

for ppl in data_list:
    url = "https://api.coresignal.com/cdapi/v1/linkedin/member/collect/{}".format(ppl)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        data_name = response.json()['name']
        data_id = response.json()['id']
        file_name = 'E:/local/'+str(data_id) + '.json'
        print(data)
        with open(file_name, 'w') as output_file:
            json.dump(data, output_file, indent=4)
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
