from bs4 import BeautifulSoup as BS
import requests
import json
from dataclasses import dataclass, field
from typing import List
import re

STATS = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Total']
@dataclass
class GeneralInfo:
    poketype: List[str] = field(default_factory=list)
    species: str = 'EMPTY'
    height: float = -1.0
    weight: float = -1.0
    abilities: List[str] = field(default_factory=list)
    local_number: List[int]  = field(default_factory=list)  # One for each game
    national_number: int = -1

@dataclass
class TrainingInfo:
    ev_yield: list = field(default_factory=list)  # number and stat
    catch_rate: int = -1
    base_friendship: int = -1
    base_exp: int = -1
    growth_rate: str = 'EMPTY'

@dataclass
class BreedingInfos:
    egg_groups: list = field(default_factory=list)
    gender: list = field(default_factory=list)
    egg_cycles: int = -1

@dataclass
class PokeStats:
    base_hp: list = field(default_factory=list)
    base_atk: list = field(default_factory=list)
    base_def: list = field(default_factory=list)
    base_spe_atk: list = field(default_factory=list)
    base_spe_def: list = field(default_factory=list)
    base_speed: list = field(default_factory=list)
    base_total: list = field(default_factory=list)

@dataclass
class Move:
    name: str = 'EMPTY'
    move_type: str = 'EMPTY'
    category: str = 'EMPTY'
    power: int = -1
    accuracy: int = -1
    lvl: int = -1

@dataclass
class Pokemoves:
    level_learnt: list = field(default_factory=list)
    tm_learnt: list = field(default_factory=list)
    egg_moves: list = field(default_factory=list)
    tr_learnt: list = field(default_factory=list)

    def add_move(self, learnt_by, move):
        if learnt_by == 'level_up':
            self.level_learnt.append(move)
        else:
            move.lvl = -1
            if learnt_by == 'tm':
                self.tm_learnt.append(move)
            elif learnt_by == 'egg':
                self.egg_moves.append(move)
            elif learnt_by == 'tr':
                self.tm_learnt.append(move)

@dataclass
class EvolutionLine:
    number_of_evo: int = -1
    leveling_condition: list = field(default_factory=list)  # List of strings

@dataclass
class PokeInfos:
    general_info: GeneralInfo = GeneralInfo()

    training_info: TrainingInfo = TrainingInfo()

    breeding_info: BreedingInfos = BreedingInfos()

    stats: PokeStats = PokeStats()

    type_affinities: list = field(default_factory=list)

    evolution_line: EvolutionLine = EvolutionLine()

    pokedex_entries: list = field(default_factory=list)

    location: list = field(default_factory=list)


class Pokemon:
    def __init__(self, name, link_to_page=None, data=None):
        self.name = name
        self.link_to_page = link_to_page
        self.data = data

def get_general_info(table):
    general_info = GeneralInfo()
    row_name = [x.text for x in table.find_all('th')]
    row_values = table.find_all('td')

    general_info.national_number = int(row_values[0].text)
    general_info.poketype = row_values[1].text.replace('\n', '')
    general_info.species = row_values[2].text
    general_info.height = float(row_values[3].text.split('\xa0')[0])
    general_info.weight = float(row_values[4].text.split('\xa0')[0])

    # TODO abilities = re.sub(r'[0-9.]', '', row_values[5].text)

    # TODO: multiple local numbers
    general_info.local_number = int(row_values[6].text.split(' ')[0])

    return general_info

def get_training_info(table):
    training_info = TrainingInfo()
    row_name = [x.text for x in table.find_all('th')]
    row_values = table.find_all('td')
    breakpoint()

def get_pokemon_info(pokelist):
    response = requests.get(pokelist.link_to_page)
    soup = BS(response.content, 'html.parser')

    infos = PokeInfos()
    tables = soup.find_all('div', class_='grid-col')

    for table in tables:
        table_name = table.find('h2')
        if table_name:
            print(table_name)
            if table_name.text == 'Pokédex data':
                infos.general_info = get_general_info(table)
            if table_name.text == 'Training':
                infos.training_info = get_training_info(table)


    breakpoint()

    # TODO:
    # get all grid-col classes
    # Check h2


    # for table in tables:
    #     if table.get('class')[0] == 'vitals-table':
    #         row_name = [x.text for x in table.find_all('th')]
    #         row_value = table.find_all('td') #[x.text.replace('\xa0', ' ') for x in table.find_all('td', text=True)]

    #         for i, val in enumerate(row_value):
    #             try:
    #                 content = row_name[i]
    #             except:
    #                 print(row_name)
    #                 print(row_value)
    #                 breakpoint()
    #             if 'National' in content:
    #                 infos.general_info.national_number = val.text
    #             if 'Type' in content:
    #                 infos.general_info.poketype = val.text
    #             if 'Species' in content:
    #                 infos.general_info.species = val.text

    # for pokemon in pokelist:
    #     pass

def main():
    base_url = 'https://pokemondb.net/'
    pokelist = []

    response = requests.get(base_url + 'pokedex/game/sword-shield')
    soup = BS(response.content, 'html.parser')

    pokecards = soup.find_all('div', class_='infocard')

    for card in pokecards:
        name = card.find('a', class_='ent-name').contents
        link_to_page = card.find('a', class_='ent-name')['href']
        pokelist.append(Pokemon(name, base_url + link_to_page))

    get_pokemon_info(pokelist[9])


if __name__ == '__main__':
    main()