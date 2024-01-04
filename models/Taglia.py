import mysql.connector
from utils import mysql_config

conn = mysql_config.get_database_connection()
cursor = conn.cursor()


def aggiungi_taglia(nome_taglia):
    nuova_taglia = Taglia(nome_taglia)
    return nuova_taglia.save()


def rimozione_taglia(nome_taglia):
    taglia_da_rimuovere = Taglia(nome_taglia)
    return taglia_da_rimuovere.delete()


class Taglia:
    def __init__(self, nome_taglia):
        self.nome_taglia = nome_taglia

    def save(self):
        insert_query = "INSERT INTO taglia (nometaglia) VALUES (%s)"
        taglia_data = (self.nome_taglia,)

        try:
            cursor.execute(insert_query, taglia_data)
            conn.commit()
            return True
        except mysql.connector.Error as err:
            return False

    def delete(self):
        delete_query = "DELETE FROM taglia WHERE nometaglia = %s"
        taglia_data = (self.nome_taglia,)

        try:
            cursor.execute(delete_query, taglia_data)
            conn.commit()
            return True
        except mysql.connector.Error as err:
            return False
