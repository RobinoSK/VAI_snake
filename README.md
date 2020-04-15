# VAI_snake - projekt do predmetu VAI

## Použitie:

Ako prvé je nutné __extrahovať komprimovaný súbor Data.rar__ do zložky __Data__, ten obsahuje dáta s niektorými generáciami a hadmi. Do tejto zložky sa zapisujú informácie o generáciach a hadoch, aby sa dali neskôr použiť znova, ako bude pochopené aj z ďalšieho vysvetlenia použita skriptu __main.py__.

Pri nachádzaní sa terminálom v zložke so skriptami a priečinkom Data, máme tri možnosti spustenia:

### 1) python main.py snake {id} {generation}
Nahrá sa informácia o neurónovej siete zvoleného hada, pokiaľ takýto súbor existuje v podpriečinku /Data. Parameter __'snake'__ (case insensitive) musí byť zadaný presne takto, inak sa zahlásí chyba. Chyba sa tiež zahlási, ak zvyšne parametre __{id}__ a __{generation}__ nebudú kladné celé čísla. Príklad použitia:   
__python main.py snake 717 15__

### 2) python main.py {number of snakes} {number of generations}
Vytvorí sa úplne nová populácia hadov a začne sa tréning od nuly. Počet hadov __{number of snakes}__ musí byť __aspoň 50__, aby tréning bol aspoň trochu zmysluplný (ja som používal od 200 do 5000 hadov). Počet tréningových generácii __{generation}__ musí byť kladné celé číslo. Pri nedodržaní podmienok sa zahlási chyba. Príklad použitia:   
__python main.py 500 100__

### 3) python main.py population {id} {generation}
Nahrajú sa hady z danej už trénovanej populácie, ktorá je označená svojím id __{id}__ a poradím generácie __{generation}__. Pokiaľ sa požadovaný súbor nenachádza v priečinku, zahlási sa chyba. Parameter __'population'__ (case insensitive) musí byť zadaný presne takto, inak sa zahlásí chyba. Chyba sa tiež zahlási, ak zvyšne parametre __{id}__ a __{generation}__ nebudú kladné celé čísla. Príklad použitia:   
__python main.py population 49551 46__

#### Predčasné ukončenie behu programu:
Priebeh skriptu je vždy možné zastaviť kliknutím na zatvárací krížik pygame okna. Ak sa nedarí zavrieť, je dobré skúsiť viackrát rýchlo za sebou kliknúť. Vyskytol sa totiž párkrát problém so zaregistrovaním kliknutia.

## Zaujímavosti:

- Vývoj populácie #717, ktorá bola trénovaná 15 generácii pri 5000 hadoch. Jednotliví najlepší hadi z generácie sa dajú postupne pozorovať postupným spúšťaním:   
__python main.py snake 717 1__   
__python main.py snake 717 2__    
.   
.   
.    
__python main.py snake 717 15__   
Je dobré si všimnúť, ako sa had vyhýba najkrajnejším miestam obrazovky až postupne do generácie číslo 15. V prípade rýchlej smrti hada (a to sa určite stane, nie sú extra inteligentní) odporúčam spustiť si ho znova.

- Pravotočivý verzus ľavotočivý had - porovnanie spustením (opäť radšej každého hada pustiť 2-3 krát):   
__python main.py snake 21783 33__   
__python main.py snake 49551 45__
