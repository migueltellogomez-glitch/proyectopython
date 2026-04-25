import pandas as pd
import os

ruta_directa = os.path.join(os.path.dirname(__file__), "vehiculos.csv")


class ErrorActualizacionBD(Exception):
    
    

    def __init__(self, mensaje):

        mensaje = "Error al actualizar la base de datos: " + str(mensaje)
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class BaseDeDatos:
    def __init__(self):
        self.vehiculos = pd.DataFrame()
    
    def read_csv(self, file_path):
        try:
            self.vehiculos = pd.read_csv(file_path)
        except Exception as e:
            print("Error al leer el archivo CSV: " + str(e))

    def read_database(self):
        self.read_csv(ruta_directa)
        return self.vehiculos
    
    def actualizar_bd(self, vehiculos):
        try:
            ruta2 = os.path.join(os.path.dirname(__file__), "vehiculos"+str(len(vehiculos))+".csv")
            vehiculos_df = pd.DataFrame([v.obtener_info() for v in vehiculos])
            vehiculos_df.to_csv(ruta2, index=False)
        except Exception as e:
            raise ErrorActualizacionBD(e)