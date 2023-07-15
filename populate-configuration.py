import requests
from bs4 import BeautifulSoup

def generate_yaml():
    url = 'http://IP-OF-ECU-3/cgi-bin/parameters'
    r = requests.get(url)
    
    if r.status_code != 200:
        print('Error: ', r.status_code)
        return

    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('table')
    
    if table is None:
        print('No table found')
        return

    rows = table.find_all('tr')
    inverter_ids = []

    for row in rows:
        columns = row.find_all('td')
        if len(columns) == 6:
            inverter_ids.append(columns[0].text)

    with open('config_part.yaml', 'w') as f:
        for i, id in enumerate(inverter_ids, start=1):
            f.write(
                f'- platform: rest\n'
                f'  name: "Solar Panel {str(i).zfill(2)}"\n'
                f'  resource: http://homeassistant.local:8123/local/power_data.json\n'
                f'  value_template: \'{{{{ value_json["{id}"][0] }}}}\'\n'
                f'  unit_of_measurement: "W"\n\n'
            )

generate_yaml()
