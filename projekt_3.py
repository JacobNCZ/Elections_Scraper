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
    """Zpracuje zadané url."""
    response = requests.get(url)
    if str(response) == "<Response [404]>":
        print(f"Zadaná stránka neexistuje. Zkontrolujte URL!\nUKONČUJI PROGRAM!")
        quit()
    elif str(response) == "<Response [500]>":
        print(f"Chyba serveru. Vyzkoušejte později.\nUKONČUJI PROGRAM!")
        quit()
    elif str(response) == "<Response [200]>":
        return BeautifulSoup(response.text, "html.parser")


def save_csv_report(file_name: str, data: list):
    """Zapíše a uloží výstupní soubor."""
    with open(file_name, mode="w", newline="") as csvfile:
        keys = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=keys, delimiter=";")

        writer.writeheader()
        for line_data in data:
            writer.writerow(line_data)


def main(url_district: str, file_name: str):
    """Vybere a zpracuje data z webových stránek

    Argumenty:
    url_district -- url odkaz celku
    file_name -- zvolený název souboru
    """
    # Pomocné proměnné:
    data_part_two = {}
    full_data = []

    soup = process_response_server(url_district)
    # Oznámení programu:
    print(f"STAHUJI DATA Z VYBRANÉHO URL: {url_district}\nUKLÁDÁM DO SOUBORU: {file_name}")

    # Průběh programu:
    html_data = soup.find_all("tr")
    for tr in pyprind.prog_bar(html_data, bar_char="█"):
        time.sleep(0.0005)

        codes = tr.find("td", class_="cislo")
        half_url_town = tr.find("a")
        towns = tr.find("td", class_="overflow_name")

        if (codes and half_url_town and towns) is not None:
            complete_url_town = f"https://www.volby.cz/pls/ps2017nss/" + half_url_town.get("href")
            details_towns = process_response_server(complete_url_town)
            all_tables = details_towns.find_all("table")
            tr_tag_table_one = all_tables[0].find_all("tr")
            td_tag_tables = tr_tag_table_one[2].find_all("td")

            # Zpracování první části dat:
            data_part_one = {
                "code": codes.get_text(),
                "location": towns.get_text(),
                "registered": td_tag_tables[3].get_text(),
                "envelopes": td_tag_tables[4].get_text(),
                "valid": td_tag_tables[7].get_text(),
            }

            # Zpracování druhé části dat
            tr_tag_table_two = all_tables[1].find_all("tr")

            for tr_two in tr_tag_table_two[2::]:
                td_tag = tr_two.find_all("td")
                party = td_tag[1].get_text()
                votes = td_tag[2].get_text()

                data_part_two.update({party: votes})
            # Sjednocení dat do datového typu "seznam":
            data_part_one.update(data_part_two)
            full_data.append(data_part_one)

    save_csv_report(file_name, full_data)

    # Oznámení o ukončení programu:
    print("UKONČUJI PROGRAM!")


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
