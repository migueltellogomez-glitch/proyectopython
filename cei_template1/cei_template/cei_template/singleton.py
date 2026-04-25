from typing import List
from cei_template.vehiculo import Vehiculo
from collections import UserList

class RegistroFlota(UserList):

    _instancia = None

    def __new__(cls, *args, **kwargs):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def __init__(self):
        if not hasattr(self, '_inicializado'):
            super().__init__()
            self._inicializado = True

    @classmethod
    def obtener_instancia(cls, vehiculos: List[Vehiculo]) -> 'RegistroFlota':
        if cls._instancia is None:
            cls._instancia = cls()
        cls._instancia.sincronizar_con_db(vehiculos)
        return cls._instancia

    def sincronizar_con_db(self, vehiculos: List[Vehiculo]):
        self.data = vehiculos

    def agregar_vehiculo(self, v: Vehiculo):
        self.append(v)