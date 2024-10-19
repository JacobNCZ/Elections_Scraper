# Úvodní hlavička.
"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Jakub Nárožný
email: narozny.jakub@gmail.com
discord: Jakub N.
"""

# Import z knihoven.
import sys
import requests
from requests.exceptions import MissingSchema
from bs4 import BeautifulSoup
import csv
import pyprind
import time


def process_response_server(url: str) -> BeautifulSoup:
    """Zpracuje zadané url a vyhodnotí aktuální stav webu.

        Argumenty:
    url -- url odkaz celku
    """
    response = requests.get(url)
    if str(response) == "<Response [404]>":
        print(f"Zadaná stránka neexistuje. Zkontrolujte URL!\nUKONČUJI PROGRAM!")
        quit()
    elif str(response) == "<Response [500]>":
        print(f"Chyba serveru. Vyzkoušejte později.\nUKONČUJI PROGRAM!")
        quit()
    elif str(response) == "<Response [200]>":
        return BeautifulSoup(response.text, "html.parser")


def get_specific_data(soup: BeautifulSoup, tag1: str, tag2: str, class_name, keyword: str) -> list:
    """Seznam vybraných dat dle argumentů.
    Vybere a zpracuje data z webových stránek

    Argumenty:
    soup -- bs4 data z html
    tag1 -- zvolený tag
    tag2 -- zvolený tag
    class_name -- jméno třídy html
    keyword -- název sloupce/klíč ve slovníku
    """
    html_data = soup.find_all(tag1)
    specific_data = list()
    for tag1 in pyprind.prog_bar(html_data, bar_char="█", title="\nVýběr požadovaných dat:"):
        time.sleep(0.01)
        raw_data = tag1.find(tag2, class_=class_name)
        if raw_data is not None:
            column = {keyword: raw_data.get_text()}
            specific_data.append(column)
    return specific_data


def get_town_urls(soup: BeautifulSoup, tag1: str, tag2: str) -> list:
    """Vytvoří seznam url pro města daného kraje.

    Argumenty:
    soup -- bs4 data z html
    tag1 -- zvolený tag
    tag2 -- zvolený tag
    """
    html_data = soup.find_all(tag1)
    town_urls = list()
    for tag1 in pyprind.prog_bar(html_data, bar_char="█", title="\nPříprava dat pro zpracování:"):
        time.sleep(0.01)
        raw_data = tag1.find(tag2)
        if raw_data is not None:
            complete_url_town = f"https://www.volby.cz/pls/ps2017nss/" + raw_data.get("href")
            town_urls.append(complete_url_town)
    return town_urls


def data_from_tables(url_list) -> list:
    """Zpracuje data z tabulek webu - zpracování druhé části dat.

    Argumenty:
    url -- url odkaz města daného kraje
    """
    data_part_two = list()
    for url_town in pyprind.prog_bar(url_list, bar_char="█", title="\nFinální zpracování dat:"):
        time.sleep(0.005)
        details_towns = process_response_server(url_town)
        all_tables = details_towns.find_all("table")
        tr_tag_table_one = all_tables[0].find_all("tr")
        td_tag_tables = tr_tag_table_one[2].find_all("td")
        columns = {
            "registered": td_tag_tables[3].get_text(),
            "envelopes": td_tag_tables[4].get_text(),
            "valid": td_tag_tables[7].get_text(),
        }

        tr_tag_table_two = all_tables[1].find_all("tr")
        for tr_two in tr_tag_table_two[2::]:
            td_tag = tr_two.find_all("td")
            party = td_tag[1].get_text()
            votes = td_tag[2].get_text()
            columns.update({party: votes})
        # Sjednocení dat do datového typu "seznam":
        data_part_two.append(columns)
    return data_part_two


def merge_data(list_a: list, list_b: list, length: int) -> list:
    """Sloučí data vybraných slovníků.

    Argumenty:
    list_a -- datový seznam slovníků - stejný počet jako v listu B
    list_b -- datový seznam slovníků - stejný počet jako v listu A
    length -- délka vybraného seznamu - určuje pozice přiřazení
    """
    for position in range(0, length):
        list_a[position].update(list_b[position])
    return list_a


def save_csv_report(file_name: str, data: list) -> csv:
    """Zapíše a uloží výstupní soubor.

    Argumenty:
    file_name -- zvolený název souboru
    data -- zpracovaná data
    """
    with open(file_name, mode="w", newline="") as csvfile:
        keys = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=keys, delimiter=";")

        writer.writeheader()
        for line_data in data:
            writer.writerow(line_data)


def main(url_district: str, file_name: str):
    """Spouští jednotlivé funkce pro zpracování dat z webových stránek.

    Argumenty:
    url_district -- url odkaz celku
    file_name -- zvolený název souboru
    """
    soup_url_district = process_response_server(url_district)
    # Oznámení programu:
    print(f"\nSTAHUJI DATA Z VYBRANÉHO URL: {url_district}\nUKLÁDÁM DO SOUBORU: {file_name}")

    column_code = get_specific_data(soup_url_district, "tr", "td", "cislo", "code")
    column_location = get_specific_data(soup_url_district, "tr", "td", "overflow_name", "location")

    full_data = merge_data(column_code, column_location, len(column_code))

    municipality_urls = get_town_urls(soup_url_district, "tr", "a")
    table_data = data_from_tables(municipality_urls)

    full_data = merge_data(full_data, table_data, len(full_data))
    save_csv_report(file_name, full_data)

    # Oznámení o ukončení programu:
    print("\nUKONČUJI PROGRAM!\n")


if __name__ == "__main__":
    """Spuštění programu"""
    try:
        main(sys.argv[1], sys.argv[2])
    # Ukončení programu:
    except IndexError:
        print("Nebyly zadány všechny argumenty! Program bude ukončen.")
        quit()
    except MissingSchema:
        print("Argumenty byly zadány v nesprávném pořadí! Program bude ukončen.")
        quit()
