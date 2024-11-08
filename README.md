# Rapport Downloader



## Kofigurationsfil

Det er muligt at ændre forskellige ting i konfigurationsfilen.

Det følgende skal inkluderes i konfigurationsfilen:


* ```KILDEFIL``` angiver stien til kildefilen, hvor pdf-navnene og url'erne skal loades fra.

* ```RAPPORTMAPPE``` angiver stien til den mappe, hvor pdf'erne skal gemmes.

* ```STATUSFIL``` angiver stigen til statusfilen, som indeholder information om, hvorledes en fil er blevet downloadet eller ej.

* ```NAVNKOLONNE``` angiver de kolonner i kildefilen, som pdf-rapporterne skal navngives efter i prioriteret rækkefølge. Flere kolonner adskilles med komma uden mellemrum.

* ```NAVNKOLONNETYPE``` angiver hvorvidt ```NAVNKOLONNE``` skal behandles som et indeks: ```"INDEKS"``` eller et kolonnenavn: ```"NAVN"```. Understøttede indeks-typer er tal f.eks. (1, 8, 22, ...) og excelkolonnenotation f.eks: (A, S, AL, ...)

* ```DOWNLOADKOLONNE``` angiver de kolonner i kildefilen, som skal forsøges at downloades fra i prioriteret rækkefølge. Flere kolonner adskilles med komma uden mellemrum.

* ```DOWNLOADKOLONNETYPE``` angiver hvorvidt ```DOWNLOADKOLONNE``` skal behandles som et indeks: ```"INDEKS"``` eller et kolonnenavn: ```"NAVN"```. Understøttede indeks-typer er tal f.eks. (1, 8, 22, ...) og excelkolonnenotation f.eks: (A, S, AL, ...)

Der er også nogle valgfra nøgleord i konfigurationsfilen:

* ```TIMEOUT``` angiver den maksimale download-tid for hver pdf-rapport angivet i sekunder. Denne har en standardværdi på 30.

* ```THREADS``` angiver antallet af pdf-rapporter, som må forsøges downloadet på samme tid. Denne har en standardværdi på 10.

### Eksempel på en konfigurationsfil

```
KILDEFIL=C:\Users\user\Documents\kilde.xlsx

RAPPORTMAPPE=reports/

STATUSFIL=files\out.xlsx

NAVNKOLONNE=BRnum
NAVNKOLONNETYPE=NAVN

DOWNLOADKOLONNE=AL,AM
DOWNLOADKOLONNETYPE=INDEKS

THREADS=5
```