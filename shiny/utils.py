import pandas as pd
import json

def translate_countries_french(df):
    with open("./data/countries_french.json") as file:
        countries_french = json.load(file)

    df["pays"] = df["country"].apply(lambda x: countries_french.get(x))
    return df
