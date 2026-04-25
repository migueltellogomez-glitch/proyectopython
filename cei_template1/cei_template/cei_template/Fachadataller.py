from cei_template.basedeDatos import BaseDeDatos
from cei_template.visualizacion import visualizacion
from cei_template.singleton import RegistroFlota
from cei_template.VehiculosFactory import VehiculoFactory
import pandas as pd


class Fachadataller:

    

    def __init__(self):
        self.vehiculo_factory = VehiculoFactory()
        self.flota = RegistroFlota.obtener_instancia(self.vehiculo_factory.crear_lista_vehiculos_desde_db())



    def get_vehiculos(self):
        return self.flota.data
    
    def agregar_vehiculo(self, vehiculo):
        self.flota.agregar_vehiculo(vehiculo)

    def actualizar_base_de_datos(self):
        bd = BaseDeDatos()
        bd.actualizar_bd(self.flota.data)

    
    def get_lista_graficos(self):
        self.lista_vehiculos = pd.DataFrame()
        bd = BaseDeDatos()
        self.lista_vehiculos = bd.read_database()
        vis = visualizacion()
        lista_graficos = []
        lista_graficos.append(vis.mostrar_vehiculos(self.lista_vehiculos))
        lista_graficos.append(vis.mostrar_distribucion_kilometraje(self.lista_vehiculos))
        lista_graficos.append(vis.mostrar_estado_vehiculos(self.lista_vehiculos))
        lista_graficos.append(vis.mostrar_kilometraje_vs_coste(self.lista_vehiculos))
        lista_graficos.append(vis.mostrar_coste_por_tipo(self.lista_vehiculos))
        lista_graficos.append(vis.mostrar_averias_comunes(self.lista_vehiculos))
        lista_graficos.append(vis.mostrar_nube_averias(self.lista_vehiculos))
        return lista_graficos
    
    def get_vehiculo_por_matricula(self, matricula: str):
        return next((v for v in self.get_vehiculos() if v.matricula == matricula), None)
    
    def reparar_vehiculo(self, matricula: str):
        vehiculo = self.get_vehiculo_por_matricula(matricula)
        if vehiculo:
            return vehiculo.reparar_averia()
        else:
            return "No se encontró un vehículo con matrícula " + matricula

    def realizar_mantenimiento(self, matricula: str):
        vehiculo = self.get_vehiculo_por_matricula(matricula)
        
        if vehiculo:
            return vehiculo.realizar_mantenimiento()
        else:
            return "No se encontró un vehículo con matrícula " + matricula

        