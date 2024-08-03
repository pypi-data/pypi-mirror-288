# Curs valutar BNR pentru RON

Librarie python care poate fi folosita pentru a afla cursul BNR pentru o anumita data.

- Documentatie BNR: https://www.bnr.ro/Exchange-rate-list-in-XML-format-7512-Mobile.aspx


## Utilizare

Instaleaza libraria cu: 

```py
pip install cursvalutarbnr
```

Poti incepe conversiile in felul urmator:

```py

from cursvalutarbnr import Currency, ron_exchange_rate

ron_to_eur = ron_exchange_rate(
    ammount=1,                    # suma pe care vrei sa o convertesti din 'from_currency' la 'to_currency'
    from_currency=Currency.RON,   # valuta (curency) corespunzatoare pentru ammount 
    to_currency=Currency.EUR      # valuta (curency) in care vrei sa fie convertita suma specificata in 'ammount' 
)

eur_to_ron = ron_exchange_rate(
    ammount=100, 
    from_currency=Currency.EUR, 
    to_currency=Currency.RON, 
    date="2023-04-25"             # poti specifica si data in isoformat pentru care vrei sa fie convertita suma
)

```

Unul din parametri `from_currency` sau `to_currency` trebuie sa fie RON. 
Parametrul `date` e optional. Daca e nespecificat va prelua cursul valutar din ziua precedenta.


Datele de la BNR sunt salvate in folderul `temp` astfel se evita o eventuala banare si e mult mai rapid.
