Election_Scraper – projekt_3
Třetí projekt do Engeto Online Python Akademie

Popis projektu:
Program slouží pro výpis dat zvoleného územního celku na stránkách voleb do poslanecké sněmovny za rok 2017: https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ

Instalace knihoven:
Požadované knihovny, které je potřeba nainstalovat pro správný průběh programu najdete v souboru requirments.txt

Spuštění projektu:
Py soubor můžeme spustit z terminálu při zadání dvou argumentů
python .\projekt_3.py <odkaz územního celku> <název ukládaného souboru>

Ukázka projektu:

Výsledky hlasování pro okres Prostějov:
1.	argument: "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"
2.	argument: "vysledky_prostejov.csv"

Spuštění programu:
python .\projekt_3.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "vysledky_prostejov.csv"

Průběh stahování:
STAHUJI DATA Z VYBRANÉHO URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
UKLÁDÁM DO SOUBORU: vysledky_prostejov.csv

Výběr požadovaných dat:
0% [██████████████████████████████] 100% | ETA: 00:00:00
Total time elapsed: 00:00:01

Výběr požadovaných dat:
0% [██████████████████████████████] 100% | ETA: 00:00:00
Total time elapsed: 00:00:01

Příprava dat pro zpracování:
0% [██████████████████████████████] 100% | ETA: 00:00:00
Total time elapsed: 00:00:01

Finální zpracování dat:
0% [██████████████████████████████] 100% | ETA: 00:00:00
Total time elapsed: 00:00:04

UKONČUJI PROGRAM!


Částečný výstup:
code	location	registered	envelopes	valid	Občanská demokratická strana	Řád národa - Vlastenecká unie	CESTA ODPOVĚDNÉ SPOLEČNOSTI	Česká str.sociálně demokrat.	Radostné Česko	STAROSTOVÉ A NEZÁVISLÍ	Komunistická str.Čech a Moravy	Strana zelených	ROZUMNÍ-stop migraci,diktát.EU	Strana svobodných občanů	Blok proti islam.-Obran.domova	Občanská demokratická aliance	Česká pirátská strana
506761	Alojzov	205	145	144	29	0	0	9	0	5	17	4	1	1	0	0	18
589268	Bedihošť	834	527	524	51	0	0	28	1	13	123	2	2	14	1	0	34
589276	Bílovice-Lutotín	431	279	275	13	0	0	32	0	8	40	1	0	4	0	0	30
589284	Biskupice	238	132	131	14	0	0	9	0	5	24	2	1	1	0	0	10
