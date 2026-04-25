from typing import List, Dict, Any
from cei_template.vehiculo import Vehiculo
from cei_template.CamionBasura import CamionBasura
from cei_template.Barredora import Barredora
from cei_template.basedeDatos import BaseDeDatos
import pandas as pd

class VehiculoFactory:
    def __init__(self):
        pass

    def crear_lista_vehiculos_desde_db(self):
        self.conector_db = BaseDeDatos()
        self.db = self.conector_db.read_database()
        vehiculos = []
        for _, fila in self.db.iterrows():
            tipo = fila['tipo_vehiculo']
            datos = {
                "matricula": fila['matricula'],
                "estado_mantenimiento": fila['estado_mantenimiento'],
                "kilometraje": fila['kilometraje'],
                "descripcion_averia": fila['descripcion_averia'],
                "coste_reparacion": fila['coste_reparacion']
            }
            if tipo == "Camion Basura":
                datos.update({
                    "capacidad_toneladas": 12,
                    "tipo_compactador": "Compactador de tornillo"
                })
            elif tipo == "Barredora":
                datos.update({
                    "capacidad_agua_litros": 5000,
                    "numero_cepillos": 4
                })
            else:
                print("Tipo de vehículo desconocido en la base de datos:" + tipo)
                continue
                
            vehiculo = self.crear_vehiculo(tipo, datos)
            vehiculos.append(vehiculo)
        return vehiculos




    def crear_vehiculo(self, tipo: str, datos: Dict[str, Any]) -> Vehiculo:
        if tipo == "Camion Basura":
            return CamionBasura(**datos)
        elif tipo == "Barredora":
            return Barredora(**datos)
        else:
            raise ValueError("Tipo de vehículo desconocido: " + tipo)
        