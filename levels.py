from bs4 import BeautifulSoup as BS
import requests
import argparse
import json

def translate_name(original_name):
    with open('names.json', 'r') as json_file:
        data = json.load(json_file)

        if isinstance(original_name, str):
            for pokemon in data:
                if original_name == pokemon['fr']:
                    return pokemon['en']
                if original_name == pokemon['en']:
                    return pokemon['fr']

            else:
                print(f'ERROR: {original_name} not found.')

        elif isinstance(original_name, list):
            new_list = []
            for pokemon in data:
                if pokemon['fr'] in original_name:
                    return pokemon['en']
                if original_name == pokemon['en']:
                    return pokemon['fr']

#TODO: scrap the data once for all and keep it in a file
def main(args):
    base_url = 'https://pokemondb.net/'
    pokelist = []

    response = requests.get(base_url + 'pokedex/game/sword-shield')
    soup = BS(response.content, 'html.parser')

    pokecards = soup.find_all('div', class_='infocard')

    pokename_original = args.name

    pokename_en = args.name

    if args.lang == 'fr':
        pokename_en = translate_name(pokename_original)

    for card in pokecards:
        name = card.find('a', class_='ent-name').contents[0]

        if pokename_en == name:
            link_to_page = card.find('a', class_='ent-name')['href']
            response = requests.get(base_url + link_to_page)
            soup = BS(response.content, 'html.parser')

            evo_line = soup.find('div', class_='infocard-list-evo')
            all_evo = evo_line.find_all('div', class_='infocard')
            next_evo = evo_line.find_all('span', class_='infocard infocard-arrow')

            print(f'Evolution line for {pokename_original}:')

            for i in range(len(next_evo)):
                print(f"{all_evo[i].find('a', class_='ent-name').text}", end=' --')
                print(f"{next_evo[i].find('small').text}", end='--> ')
            print(f"{all_evo[-1].find('a', class_='ent-name').text}")

            break

    else:
        print(f'ERROR: {pokename} not found in the database (are you sure you used english names?)')
        return



def scrap_names():
    response = requests.get(r'https://bulbapedia.bulbagarden.net/wiki/List_of_French_Pok%C3%A9mon_names')
    soup = BS(response.content, 'html.parser')

    name_list = []

    for table in soup.find_all('table', class_='roundy'):
        for row in table.find_all('tr', attrs={'style': 'background:#FFF'}):
            row_data = row.text.replace('\n', '').split(' ')
            name_list.append({'en': row_data[3], 'fr': row_data[4]})


    with open('names.json', 'w') as json_output:
        json.dump(name_list, json_output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", type=str)
    parser.add_argument("-l", "--lang", default="fr", type=str)
    args = parser.parse_args()
    main(args)

    #scrap_names()