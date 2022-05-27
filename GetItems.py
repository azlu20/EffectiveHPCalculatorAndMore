# Used to get the URL
import requests
# Used to export the data to a CSV
import csv
import json

def data_version():
    ddragon = "https://ddragon.leagueoflegends.com/realms/euw.json"
    euw_json = requests.get(ddragon).json()
    return euw_json['n']['item']


def build_data_url():
    return "http://ddragon.leagueoflegends.com/cdn/" + data_version() + "/data/en_GB/item.json"


def get_jsons():
    data_url = build_data_url()
    data_json = requests.get(data_url).json()
    item_list = data_json['data'].keys()
    return data_json, item_list


def row_headings():
    return [
        "Name",
        "Gold",
        "Health",
        "Armor",
        "Magic Resist"
    ]


def item_create_file():
    data_json, item_list = get_jsons()
    file_name = 'patch_' + data_version() + '_itemStats.csv'
    with open(file_name, 'w', newline='', encoding='utf8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(row_headings())
        for item in item_list:
            write = False
            name = data_json['data'][item]['name']
            gold = data_json['data'][item]['gold']['total']
            hp = 0
            armor = 0
            mr = 0
            if "FlatHPPoolMod" in data_json['data'][item]['stats']:
                write = True
                hp = data_json['data'][item]['stats']["FlatHPPoolMod"]
            if "FlatArmorMod" in data_json['data'][item]['stats']:
                write = True
                armor = data_json['data'][item]['stats']["FlatArmorMod"]
            if "FlatSpellBlockMod" in data_json['data'][item]['stats']:
                write = True
                mr = data_json['data'][item]['stats']["FlatSpellBlockMod"]

            if write:
                writer.writerow([name, gold, hp, armor, mr])
    return file_name


