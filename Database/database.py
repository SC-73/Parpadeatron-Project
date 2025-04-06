import sqlite3, os, sys
from pathlib import Path

class Database:
    def __init__(self):
        # Obtener la ruta del directorio de datos del usuario
        if sys.platform == "win32":
            self.data_dir = os.path.join(os.environ["APPDATA"], "Parpadeatron")
        else:
            self.data_dir = os.path.join(os.path.expanduser("~"), ".parpadeatron")
        
        # Crear el directorio si no existe
        os.makedirs(self.data_dir, exist_ok=True)

        # Ruta completa de la base de datos
        self.db_path = os.path.join(self.data_dir, "parpadeatron.db")
        
        # Si la base de datos no existe, créala y configura las tablas
        if not os.path.exists(self.db_path):
            self.create_tables()

    def create_tables(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor() 

        # Crear tabla de registro de Tiempo
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Time (
            id_record_time INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT NOT NULL
        )
        ''')

        conn.commit()
        conn.close()

    def register_time(self, time):
        conn = sqlite3.connect((self.db_path))
        cursor = conn.cursor()
        try:
            # Insertar nuevo registro
            cursor.execute('''
            INSERT INTO Time (time)
            VALUES (?)
            ''', (time,))
            
            # Mantener solo los últimos 5 registros
            cursor.execute('''
            DELETE FROM Time 
            WHERE id_record_time NOT IN (
                SELECT id_record_time 
                FROM Time  
                ORDER BY id_record_time DESC 
                LIMIT 5
            )
            ''')
            
            conn.commit()
            return True
        except sqlite3.Error:
            return False
        finally:
            conn.close()

    def get_last_time(self):
        conn = sqlite3.connect((self.db_path))
        cursor = conn.cursor()

        try:
            cursor.execute('''
            SELECT time FROM Time 
            ORDER BY id_record_time DESC 
            LIMIT 1
            ''')
            
            result = cursor.fetchone()
            return result[0] if result else "00:00:00"
        except sqlite3.Error:
            print("Error in get_last_time method in database")
            return "00:00:00"  # En caso de error, retornamos el tiempo por defecto
        finally:
            conn.close()
    
    def imprimir_tabla_registro(self):
        with sqlite3.connect((self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Time')
            
            # Obtener los nombres de las columnas
            column_names = [description[0] for description in cursor.description]
            resultado = cursor.fetchall()
        
        # Encabezado de la tabla
        print(" | ".join(column_names))
        for registro in resultado:
            print(registro)