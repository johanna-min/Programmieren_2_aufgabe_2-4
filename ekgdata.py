import json
import pandas as pd
import plotly.express as px

import plotly.graph_objects as go


# %% Objekt-Welt

# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden

class EKGdata:

## Konstruktor der Klasse soll die Daten einlesen

    def __init__(self, ekg_dict):
        
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',])
        self.df = self.df.iloc[:5000]  # Entferne die erste Zeile, da sie nur die Spaltennamen enthält
        self.peaks = []
    
        
    def load_by_id(self, id):
        # Instanziiert einen EKG-Test anhand der ID und der Personen-Datenbank
        with open("data/person_db.json", "r", encoding="utf-8") as file:
            person_data = json.load(file)

        for person_dict in person_data: # durch die Personen durchgehen
            for ekg_test in person_dict["ekg_tests"]:   # durch die EKG Tests durchgehen
                if ekg_test["id"] == id:
                    return EKGdata(ekg_test)
    
    def find_peaks(self, threshold, respacing_factor=5):
        # Findet Peaks in den EKG-Daten und fügt diese als Attribut hinzu (hier können wir die Funktion aus der letzten Aufgabe verwenden)
        series = series = self.df["Messwerte in mV"] # die Spalte mit den EKG-Werten als Series speichern 
        series = series.iloc[::respacing_factor] # EKG-Daten ausdünnen
        series = series[series > threshold] # Nur Werte über dem Schwellwert behalten

        peaks = []
        last = 0
        current = 0
        next = 0

        for index, row in series.items():
            last = current
            current = next
            next = row

            if last < current and current > next and current > threshold:
                peaks.append(index - respacing_factor)

        self.peaks = peaks # Ergebnis als Attribut speichern

        self.df["is_peak"] = False
        self.df.loc[self.peaks, "is_peak"] = True

        return peaks

    def estimate_hr(self):
        # Berechnet die Herzfrequenz basierend auf den Peaks (Peaks/Minute)

        self.df_peaks = self.df.loc[self.df["is_peak"] == True]

        N_peaks = self.df_peaks["is_peak"].sum()      
        dt_ms = self.df_peaks["Zeit in ms"].iloc[-1] - self.df_peaks["Zeit in ms"].iloc[0]
        dt_min = dt_ms/(1000*60)

        avg_hr = N_peaks/dt_min # durchschnittliche Herzfrequenz in bpm
        return avg_hr
    
    def plot_time_series(self):

        # EKG-Kurve
        limit=2000

        fig = px.line(
            self.df.head(2000),
            x="Zeit in ms",
            y="Messwerte in mV",
            title="EKG Zeitreihe"
        )

        df_plot = self.df.head(limit) # Daten für die ersten 2000 Werte, um die Peaks zu plotten

        peak_df = df_plot.loc[df_plot.index.isin(self.peaks)] # DataFrame mit den Peak-Daten erstellen

        fig.add_trace(
            go.Scatter(
                x=peak_df["Zeit in ms"],
                y=peak_df["Messwerte in mV"],
                mode="markers",
                marker=dict(color="red", size=8),
                name="Peaks"
            )
        )

        self.fig = fig
        return fig



if __name__ == "__main__":
    print("This is a module with some functions to read the EKG data")
    file = open("data/person_db.json")
    person_data = json.load(file)
    ekg_dict = person_data[0]["ekg_tests"][0]
    print(ekg_dict)
    ekg = EKGdata(ekg_dict)
    print(ekg.df.head())
    peaks = ekg.find_peaks(340)
    fig = ekg.plot_time_series()
    fig.show()
