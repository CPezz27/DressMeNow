import mysql.connector
from utils import mysql_config

conn = mysql_config.get_database_connection()
cursor = conn.cursor()


def delete(id_taglia):

    delete_query = "DELETE FROM taglia WHERE id_taglia = %s"

    try:
        cursor.execute(delete_query, (id_taglia,))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def aggiungi_taglia(nome_taglia):
    nuova_taglia = Taglia(nome_taglia)
    return nuova_taglia.save()


def rimozione_taglia(id_taglia):
    return delete(id_taglia)


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
