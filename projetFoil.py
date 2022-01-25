from projetFoil_class import *
import sqlite3
from sqlite3.dbapi2 import Date
import requests
from os import getcwd
from datetime import datetime
import time


# application pour sa montre connectée qui donne en temps réel les dernières mesures sur 3 stations locales disposant d’un anémomètre.
# Elle souhaite savoir où se diriger pour trouver le vent nécessaire à ses futures activités.
# sa montre dispose d’un stockage particulièrement réduit,  la base de données locale devra être mise à jour régulièrement tout en s’assurant de ne pas dépasser un volume de stockage correspondant aux 10 derniers enregistrements.
# Enfin, elle souhaite absolument avoir la dernière sauvegarde qui devra être mise à jour régulièrement (une fois tous les 5 enregistrements).
# Pourrez-vous aider Cléante à réaliser son projet en moins de 48h chrono?

# Contrainte: usage de SQLite sur la montre
# Les données pourront être récupérées auprès d’anémomètres connectés: les “pioupiou”s https://www.openwindmap.org/PP308
# Ceux-ci disposent d’une API qui peut être interrogée: http://developers.pioupiou.fr/api/live/


def connection_bdd():
    
    connection = sqlite3.connect('foil.db')
    cursor = connection.cursor()
    #cursor.executescript('script_bd.sql')
    return cursor, connection


def connection_api(i):
    req = requests.get(f"http://api.pioupiou.fr/v1/live/{i}")
    req = req.json()

    # creation d'une instance de Station
    station = Station(req['data']['id'], req['data']['meta']['name'], req['data']
                      ['location']['latitude'], req['data']['location']['longitude'])

    # formatage de la date
    date = req['data']['measurements']['date']
    date = date.replace('T', " ")[2:19]
    date = datetime.strptime(date, '%y-%m-%d %H:%M:%S')

    # creation d une instance de Measure
    measure = Measure(date, station, req['data']['measurements']['wind_heading'], req['data']['measurements']
                      ['wind_heading'], req['data']['measurements']['wind_heading'], req['data']['measurements']['wind_heading'])

    return station, measure


def add_station(station, cursor):
    """[summary]

    Args:
        station ([type]): [description]
        cursor ([type]): [description]
    """
    # ajout d'une station, si la station exist IGNORE
    cursor.execute("INSERT OR IGNORE INTO station VALUES (?,?,?,?)", [
                   station.id, station.name, station.latitude, station.longitude])


def add_measure(measure, cursor):

    # # si on a deja plus de 10 resultats en bdd on supprime le plus ancien avant d'incerer une nouvelle ligne
    cursor.execute("DELETE FROM measure WHERE dat NOT IN (SELECT dat FROM measure ORDER BY dat DESC LIMIT 9 )")

    cursor.execute("INSERT OR IGNORE INTO measure VALUES (?,?,?,?,?,?)", [measure.date, measure.station.id, measure.wind_heading, measure.wind_speed_avg,  measure.wind_speed_max, measure.wind_speed_min])


def backup():
    base = sqlite3.connect('foil.db')
    backup = sqlite3.connect('backup_foil.db')
    base.backup(backup)




#--------------------------#
#           MAIN           #
#--------------------------#


spot = [110, 115, 123]
stop = False
count = 1
refresh = 15  # frequence de rafraichissement des données en minutes



while not stop:

    cursor = None
    connection = None
    # connection a la bdd
    try:
        cursor, connection = connection_bdd()

        for i in spot:

            # recup donnee api        
            try:
                station, measure = connection_api(i)
                # maj station bdd
                try:
                    add_station(station, cursor)
                    # maj measure bdd
                    try:
                        add_measure(measure, cursor)
                    except Exception as e:
                        print(e, f"echec insertion measure pour la station n°{i}")
                except Exception as e:
                    print(e,f"echec insertion station n°{i} ")               
            except Exception as e:
                print(e,f"echec connection api a la station n°{i}")
    except Exception as e:
        print(e,"echec connection bdd")
        break
    finally:
        # validation de la bdd
        connection.commit()
        
        if count % 5 == 0 :
            backup()
        try:
            if connection is not None:
                connection.close()
        except Exception as e:
            print(e)
            pass

        print (count, datetime.now().strftime("%H:%M:%S"))
        time.sleep(refresh * 60)
        count += 1
