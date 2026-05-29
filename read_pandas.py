# %%

# Paket für Bearbeitung von Tabellen
import pandas as pd
import plotly.express as px
import numpy as np


def read_my_csv():
    # Einlesen eines Dataframes
    ## "\t" steht für das Trennzeichen in der txt-Datei (Tabulator anstelle von Beistrich)
    ## header = None: es gibt keine Überschriften in der txt-Datei
    df = pd.read_csv("data/ekg_data/01_Ruhe.txt", sep="\t", header=None)

    # Setzt die Columnnames im Dataframe
    df.columns = ["Messwerte in mV","Zeit in ms"]
    
    # Gibt den geladen Dataframe zurück
    return df


def read_activity_csv():
    df = pd.read_csv("data/activities/activity.csv", sep=",")
    df["time in seconds"] = np.arange(len(df))
    df["time in minutes"] = df["time in seconds"]/60
    return df

def mean_leistung(df):
    return df["PowerOriginal"].mean()

def max_leistung(df):
    return df["PowerOriginal"].max()

def make_plot(df):

    # Erstellte einen Line Plot, der ersten 2000 Werte mit der Zeit aus der x-Achse
    fig = px.line(df.head(2000), x= "Zeit in ms", y="Messwerte in mV")
    return fig


def make_power_hr_plot(df):
    fig = px.line(df, x= "time in minutes", y= ["PowerOriginal","HeartRate"])
    return fig
'''
def add_zones(df):
    user_input = input("Bitte geben Sie die maximale Herzfrequenz ein: ") 
    max_heart_rate = float(user_input)

    df["Zone_1"] = df_activity["HeartRate"] < max_heart_rate * 0.6
    df["Zone_2"] = (df_activity["HeartRate"] < max_heart_rate * 0.6) & (df_activity["HeartRate"] < max_heart_rate * 0.7)
    df["Zone_3"] = (df_activity["HeartRate"] < max_heart_rate * 0.819)
    df["Zone_4"] = (df_activity["HeartRate"] < max_heart_rate * 0.9)
    df["Zone_5"] = (df_activity["HeartRate"] < max_heart_rate * 1.0)

    return df

def make_Zone_plot(df):
    fig = px.line(df,)
#df_activity[..........].mean()
'''
if __name__ == "__main__":
    ekg_df = read_my_csv()
    print(ekg_df.head())

    ekg_fig = make_plot(ekg_df)
    ekg_fig.show()
    excel = read_activity_csv()
    print(excel)
    excel_fig=make_power_hr_plot(excel)
    excel_fig.show()
    

    



# %%
