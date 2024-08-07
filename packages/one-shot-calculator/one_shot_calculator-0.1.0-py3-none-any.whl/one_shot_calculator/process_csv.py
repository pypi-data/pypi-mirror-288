"""
This module processes a CSV file obtained from the Monster Compendium Excel sheet.

If you have trouble due to your file being in a different encoding, try using the check_encoding function,
then edit the process_csv_3e function as needed.
"""

import pandas as pd
import charset_normalizer
from importlib import resources as impresources
from . import csv

def check_encoding(csv_filename):
    """Tries to guess the encoding of a csv file and prints the result"""
    #using importlib.resources to control access to the csv files
    csv_file=impresources.files(csv) / csv_filename
    with csv_file.open("rb") as rawdata:
        print(charset_normalizer.detect(rawdata.read(50000)))

def process_csv_3p5():
    """Processes the CSV file into a usable pandas dataframe and returns the result"""

    #using importlib.resources to control access to the csv files
    csv_file=impresources.files(csv) / 'Monster Compendium (Graphless).csv'

    third_ed_monster_table=pd.read_csv(csv_file,encoding="windows-1250")

    #dropping the weird extra NaN line at the end
    third_ed_monster_table=third_ed_monster_table[~third_ed_monster_table.Creature.isna()]

    #dropping extra columns at the end that were used for a legend in the Excel sheet
    third_ed_monster_table=third_ed_monster_table.drop(third_ed_monster_table.columns[31:],axis=1)
    
    #get rid of the weird CR - monsters
    third_ed_monster_table=third_ed_monster_table[~(third_ed_monster_table.CR=='-')]

    #convert things that should be numbers to numbers
    third_ed_monster_table["CR"]=third_ed_monster_table["CR"].map(eval)
    third_ed_monster_table["HD"]=third_ed_monster_table["HD"].map(eval)
    third_ed_monster_table["(hp)"]=third_ed_monster_table["(hp)"].map(int)
    third_ed_monster_table["Spd"]=third_ed_monster_table["Spd"].map(lambda x: x if x!=x else int(x))
    third_ed_monster_table["AC"]=third_ed_monster_table["AC"].map(int)
    third_ed_monster_table["t"]=third_ed_monster_table["t"].map(int)
    third_ed_monster_table["ff"]=third_ed_monster_table["ff"].map(lambda x: x if x=='-' else int(x))
    third_ed_monster_table["Grpl"]=third_ed_monster_table["Grpl"].map(lambda x: x if x=='-' else int(x))
    third_ed_monster_table["F"]=third_ed_monster_table["F"].map(int)
    third_ed_monster_table["R"]=third_ed_monster_table["R"].map(lambda x: x if x=='-' else int(x))
    third_ed_monster_table["W"]=third_ed_monster_table["W"].map(int)
    third_ed_monster_table["S"]=third_ed_monster_table["S"].map(lambda x: x if x=='-' else int(x))
    third_ed_monster_table["D"]=third_ed_monster_table["D"].map(lambda x: x if x=='-' else int(x))
    third_ed_monster_table["Co"]=third_ed_monster_table["Co"].map(lambda x: x if x=='-' else int(x))
    third_ed_monster_table["I"]=third_ed_monster_table["I"].map(lambda x: x if x=='-' else int(x))
    third_ed_monster_table["W.1"]=third_ed_monster_table["W.1"].map(int)
    third_ed_monster_table["Ch"]=third_ed_monster_table["Ch"].map(int)

    #rename columns for user-friendliness
    third_ed_monster_table=third_ed_monster_table.rename(columns={"(hp)":"hp","s/f/b/c":"SwimFlyBurrowClimb","t":"TouchAC","ff":"FlatFootedAC","F":"Fort","R":"Ref","W":"Will","S":"Str","D":"Dex","Co":"Con","I":"Int","W.1":"Wis","Ch":"Cha"})

    #fixing a mistake in the original compendium, in case you get the CSV directly from there
    third_ed_monster_table.loc[third_ed_monster_table["Creature"]=="Dragon, Chromatic, Blue, Young Adult","CR"]=11.0

    return third_ed_monster_table