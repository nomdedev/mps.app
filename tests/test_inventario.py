import unittest
from mps.database_utils import connect_database

class TestInventarioDatabase(unittest.TestCase):
    def setUp(self):
        try:
            self.connection = connect_database()
            print("Conexión establecida exitosamente.")
        except Exception as e:
            self.fail(f"Error al conectar con la base de datos: {e}")

    def tearDown(self):
        if self.connection:
            self.connection.close()
            print("Conexión cerrada.")

    def test_connection_successful(self):
        self.assertIsNotNone(self.connection, "La conexión a la base de datos falló.")
        print("Conexión exitosa a la base de datos.")

    def test_inventario_table_exists(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = 'inventario'
            """)
            result = cursor.fetchone()
            self.assertIsNotNone(result, "La tabla 'inventario' no existe en la base de datos.")
            print("La tabla 'inventario' existe en la base de datos.")
        except Exception as e:
            self.fail(f"Error al verificar la existencia de la tabla 'inventario': {e}")

    def test_fetch_all_inventario(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM inventario")
            rows = cursor.fetchall()
            self.assertIsInstance(rows, list, "El resultado no es una lista.")
            print("Datos de la tabla 'inventario':")
            for row in rows:
                print(row)
        except Exception as e:
            self.fail(f"Error al obtener los datos de la tabla 'inventario': {e}")
