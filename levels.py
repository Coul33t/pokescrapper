from bs4 import BeautifulSoup as BS
import requests
import argparse

def main(pokename):
    base_url = 'https://pokemondb.net/'
    pokelist = []

    response = requests.get(base_url + 'pokedex/game/sword-shield')
    soup = BS(response.content, 'html.parser')

    pokecards = soup.find_all('div', class_='infocard')

    for card in pokecards:
        name = card.find('a', class_='ent-name').contents[0]

        if pokename == name:
            link_to_page = card.find('a', class_='ent-name')['href']
            response = requests.get(base_url + link_to_page)
            soup = BS(response.content, 'html.parser')

            evo_line = soup.find('div', class_='infocard-list-evo')
            all_evo = evo_line.find_all('div', class_='infocard')
            next_evo = evo_line.find_all('span', class_='infocard infocard-arrow')

            print(f'Evolution line for {name}:')

            for i in range(len(next_evo)):
                print(f"{all_evo[i].find('a', class_='ent-name').text}", end=' --')
                print(f"{next_evo[i].find('small').text}", end='--> ')
            print(f"{all_evo[-1].find('a', class_='ent-name').text}")

            break

    else:
        print(f'ERROR: {pokename} not found in the database (are you sure you used english names?)')
        return





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str)
    args = parser.parse_args()
    main(args.name)