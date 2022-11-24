import argparse
import json
import requests
from bs4 import BeautifulSoup as BS

def translate_name(original_name):
    with open('names.json', 'r') as json_file:
        data = json.load(json_file)

        if isinstance(original_name, str):
            for pokemon in data:
                if original_name == pokemon['fr']:
                    return pokemon['en']
                if original_name == pokemon['en']:
                    return pokemon['fr']

            print(f'ERROR: {original_name} not found.')
            return

# TODO: scrap the data once for all and keep it in a file
def main(args):
    base_url = 'https://pokemondb.net/'

    response = requests.get(base_url + 'pokedex/game/scarlet-violet')
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

            if not evo_line:
                if args.lang == 'fr':
                    name = translate_name(name)
                print(f'[{name}]')
                return

            all_evo = evo_line.find_all('div', class_='infocard')
            next_evo = evo_line.find_all('span', class_='infocard infocard-arrow')

            print(f'Evolution line for {pokename_original}:')

            for i, _ in enumerate(next_evo):
                name = all_evo[i].find('a', class_='ent-name').text
                if args.nospoil:
                    if name != pokename_en:
                        name = '???'
                elif args.lang == 'fr':
                    name = translate_name(name)

                if name == pokename_original or name == pokename_en:
                    name = '[' + name + ']'

                print(f"{name}", end=' --')
                print(f"{next_evo[i].find('small').text}", end='--> ')


            if not args.nospoil:
                name = all_evo[-1].find('a', class_='ent-name').text

                if args.lang == 'fr':
                    name = translate_name(name)

                if name == pokename_original or name == pokename_en:
                    name = '[' + name + ']'

            else:
                name = all_evo[-1].find('a', class_='ent-name').text

                if args.lang == 'fr':
                    name = translate_name(name)

                if name == pokename_original or name == pokename_en:
                    name = '[' + name + ']'

                if args.nospoil:
                    name = '???'


            print(f"{name}")

            break

    else:
        print(f'ERROR: {pokename_original} not found in the database (are you sure you used english names?)')
        return



def scrap_names():
    response = requests.get(r'https://bulbapedia.bulbagarden.net/wiki/List_of_French_Pok%C3%A9mon_names')
    soup = BS(response.content, 'html.parser')

    name_list = []

    for table in soup.find_all('table', class_='roundy'):
        for row in table.find_all('tr', attrs={'style': 'background:#FFF'}):
            
            row_data = list(filter(None,row.text.replace('\n', ' ').split(' ')))
            try:
                name_list.append({'en': row_data[1], 'fr': row_data[2]})
            except IndexError:
                name_list.append({'en': row_data[0], 'fr': row_data[1]})


    with open('names.json', 'w') as json_output:
        json.dump(name_list, json_output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", type=str)
    parser.add_argument("-l", "--lang", default="en", type=str)
    parser.add_argument("-ns", "--nospoil", action='store_true')
    args = parser.parse_args()
    #scrap_names()
    main(args)

    # scrap_names()
