# VAI_snake
Projekt do predmetu VAI

Použitie:

Ako prvé je nutné extrahovať komprimovaný súbor Data.rar do zložky Data, ten obsahuje dáta s niektorými generáciami a hadmi. Do tejto zložky sa zapisujú informácie o generáciach a hadoch, aby sa dali neskôr použiť znova, ako bude pochopené aj z ďalšieho vysvetlenia použita skriptu main.py.

Pri nachádzaní sa terminálom v zložke so skriptami a priečinkom Data, máme tri možnosti spustenia:

1) python main.py snake {id} {generation}
2) python main.py {number of snakes} {number of generations}
3) python main.py population {id} {generation}

Pri 1) možnosti sa nahrá informácia o neurónovej siete zvoleného hada, pokiaľ takýto súbor existuje v podpriečinku /Data. Parameter 'snake' (case insensitive) musí byť zadaný presne takto, inak sa zahlásí chyba, rovnako sa chyba zahlási, ak zvyšne parametre {id} a {generation} nebudú kladné celé čísla. Príklad použitia:
python main.py snake 717 15

Pri 2) možnosti sa vytvorí úplne nová populácia hadov a začne sa tréning od nuly. Počet hadov {number of snakes} musí byť aspoň 50, aby tréning bol aspoň trochu zmysluplný, počet tréningových generácii {generation} musí byť kladné celé číslo. Pri nedodržaní podmienok sa zahlási chyba. Príklad použitia:
python main.py 500 100

Pri 3) možnosti sa nahrajú hady z danej už trénovanej populácie, ktorá je označená svojím id {id} a poradím generácie {generation}. Pokiaľ sa požadovaný súbor nenachádza v priečinku, zahlási sa chyba. Parameter 'population' (case insensitive) musí byť zadaný presne takto, inak sa zahlásí chyba, rovnako sa chyba zahlási, ak zvyšne parametre {id} a {generation} nebudú kladné celé čísla. Príklad použitia:
python main.py population 49551 46

Priebeh skriptu je vždy možné zastaviť kliknutím na zatvárací krížik pygame okna. Ak sa nedarí zavrieť, je dobré skúsiť viackrát rýchlo za sebou kliknúť. Vyskytol sa totiž párkrát problém so zaregistrovaním kliknutia.
