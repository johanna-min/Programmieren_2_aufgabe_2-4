import json


def load_person_data():
    """A Function that knows where the person database is and returns a dictionary with the persons"""
    file = open("data/person_db.json")
    person_data = json.load(file)
    return person_data

def get_person_list(person_data):
    """A Function that takes the persons-dictionary and returns a list auf all person names"""
    liste_von_Namen = []

    for eintrag in person_data:
        liste_von_Namen.append(eintrag["lastname"] + ", " +  eintrag["firstname"])
    return liste_von_Namen


suchstring  = "lastname, firstname"

def find_person_data_by_name(suchstring):
    """ Der Funktion wird ein String (= Suchstring) bestehend aus Vor- und Nachname übergeben
    und soll ein Dictionary zurückgeben"""

    person_data = load_person_data()
    if suchstring == "None":
        return {}

    two_names = suchstring.split(", ")
    Vorname = two_names[1]
    Nachname = two_names[0]
    
    for eintrag in person_data:
        if (eintrag["lastname"] == Nachname and eintrag["firstname"] == Vorname):
            print()

            return eintrag
    
    return {}




if __name__ == "__main__":
    my_person_db = load_person_data()
    print(get_person_list(my_person_db))
    current_person = find_person_data_by_name("Brown, Tom")
    
    

'''
Umgekehrt, also erster Vorname und dann Nachname:
def get_person_list(person_data):
    liste_von_Namen = []
    
    for eintrag in person_data:
        liste_von_Namen.append(eintrag["firstname"] + "," + eintrag["lastname"])
    return liste_von_Namen'''


