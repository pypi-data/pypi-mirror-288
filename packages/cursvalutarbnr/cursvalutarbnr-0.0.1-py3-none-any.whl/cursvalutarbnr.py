import os
import json
import tempfile
import requests
import xmltodict
from enum import StrEnum
from datetime import datetime, timedelta


class Currency(StrEnum):
    RON = "RON"
    AED = "AED"
    AUD = "AUD"
    BGN = "BGN"
    BRL = "BRL"
    CAD = "CAD"
    CHF = "CHF"
    CNY = "CNY"
    CZK = "CZK"
    DKK = "DKK"
    EGP = "EGP"
    EUR = "EUR"
    GBP = "GBP"
    HUF = "HUF"
    INR = "INR"
    JPY = "JPY"
    KRW = "KRW"
    MDL = "MDL"
    MXN = "MXN"
    NOK = "NOK"
    NZD = "NZD"
    PLN = "PLN"
    RSD = "RSD"
    RUB = "RUB"
    SEK = "SEK"
    THB = "THB"
    TRY = "TRY"
    UAH = "UAH"
    USD = "USD"
    XAU = "XAU"
    XDR = "XDR"
    ZAR = "ZAR"

    @classmethod
    def values(cls):
        return {e.value for e in cls}


def format_date(date: str = None):
    """
    Convert string date in '2024-07-31' (YYYY-MM-DD) format.
    Make sure date is not in the future.
    """

    previous_date = datetime.now().date() - timedelta(days=1)
    date_obj = (
        previous_date if date is None else datetime.strptime(date, "%Y-%m-%d").date()
    )

    if date_obj > previous_date:
        raise ValueError("Can't get BNR rates from the future or current day.")

    return date_obj


def get_exchange_rates_for_year(year: int = None):
    """
    Make a request to BNR API to get the XML with rates for the year provided.
    If year is not provided will get the latest rates for current date.

    The return will be a dictionary like:

    {'2024-01-03': {'AED': 1.239,
          'AUD': 3.0693,
          'CAD': 3.4127,
          etc},
      'YYYY-MM-DD': {'CURRENCY': RON_VALUE}
    }

    https://www.bnr.ro/nbrfxrates.xml
    https://www.bnr.ro/nbrfxrates10days.xml
    https://www.bnr.ro/files/xml/years/nbrfxrates{year}.xml
    """

    if year > datetime.now().date().year:
        raise ValueError("Can't get BNR rates from the future.")

    bnr_xml_url = (
        "https://www.bnr.ro/nbrfxrates.xml"
        if year is None
        else f"https://www.bnr.ro/files/xml/years/nbrfxrates{year}.xml"
    )

    r = requests.get(bnr_xml_url)
    r.raise_for_status()

    bnr_ron_rates = xmltodict.parse(r.content)

    exchange_rates = {}
    for entries in bnr_ron_rates["DataSet"]["Body"]["Cube"]:
        rates = {}
        for entry in entries["Rate"]:
            rates[entry["@currency"]] = round(
                float(entry["#text"]) * int(entry.get("@multiplier", 1)), 4
            )
        exchange_rates[entries["@date"]] = rates

    # print(f"Got new exchange rates from {bnr_xml_url}")
    return exchange_rates


def ron_exchange_rate(
    ammount: float, from_currency: Currency, to_currency: Currency, date: str = None
):
    """
    from_currency: one of Currency StrEnum value
    to_currency: one of Currency StrEnum value
    One of the parameters 'from_currency' or 'to_currency' must be RON.
    date: string isoformat date like '2024-07-31' (YYYY-MM-DD)
    
    Usage:

    ron_to_eur = ron_exchange_rate(
        ammount=1, from_currency=Currency.RON, to_currency=Currency.EUR
    )
    eur_to_ron = ron_exchange_rate(
        ammount=1, from_currency=Currency.EUR, to_currency=Currency.RON, date="2023-04-25"
    )
    """

    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    if from_currency not in Currency.values() or to_currency not in Currency.values():
        raise ValueError(
            "Currency provided is not supported. Please check Currency enum class."
        )

    if not (from_currency == Currency.RON or to_currency == Currency.RON):
        raise ValueError(
            "One of the parameters 'from_currency' or 'to_currency' must be RON."
        )

    date_obj = format_date(date)

    previous_saved_file = os.path.join(
        tempfile.gettempdir(), f"CursValutarBNRExchangeRatesForYear{date_obj.year}.json"
    )

    if os.path.exists(previous_saved_file):
        with open(previous_saved_file, "r") as file:
            exchange_rates = json.load(file)

        if date_obj.isoformat() not in exchange_rates:
            # print(f"Date '{date}' not found in file '{previous_saved_file}'. Getting new exchange rates...")
            exchange_rates = get_exchange_rates_for_year(date_obj.year)
            with open(previous_saved_file, "w") as file:
                json.dump(exchange_rates, file)
        # else:
        # print(f"Date '{date_obj.isoformat()}' was found in file '{previous_saved_file}'.")
    else:
        exchange_rates = get_exchange_rates_for_year(date_obj.year)
        with open(previous_saved_file, "w") as file:
            json.dump(exchange_rates, file)

    day_rates = exchange_rates[date_obj.isoformat()]

    # print(day_rates)

    if from_currency == Currency.RON:
        return round(ammount * day_rates[to_currency], 2)
    else:
        return round(ammount / day_rates[from_currency], 2)



# ron_to_eur = ron_exchange_rate(
#     ammount=1, from_currency=Currency.RON, to_currency=Currency.EUR
# )
# eur_to_ron = ron_exchange_rate(
#     ammount=100, from_currency=Currency.EUR, to_currency=Currency.RON, date="2023-04-25"
# )
# ron_to_gbp = ron_exchange_rate(1, Currency.RON, Currency.GBP)
# gbp_to_ron = ron_exchange_rate(1, Currency.GBP, Currency.RON)

# ron_to_mld = ron_exchange_rate(1, Currency.RON, Currency.MDL)
# mld_to_ron = ron_exchange_rate(1, Currency.MDL, Currency.RON)

# eur_to_mld = ron_exchange_rate(1, Currency.EUR, Currency.MDL)

# print("ron_to_eur (4.92)", ron_to_eur)
# print("eur_to_ron (0.20)", eur_to_ron)

# print("ron_to_gbp (5.9)", ron_to_gbp)
# print("gbp_to_ron (0.17)", gbp_to_ron)

# print("ron_to_mld (0.26)", ron_to_mld)
# print("mld_to_ron (3.83)", mld_to_ron)

# print("eur_to_mld", eur_to_mld)
