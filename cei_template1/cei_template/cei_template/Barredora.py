from cei_template.vehiculo import Vehiculo

class Barredora(Vehiculo):
    def __init__(self, matricula: str, estado_mantenimiento: str, kilometraje: float, 
                 capacidad_agua_litros: float, numero_cepillos: int, descripcion_averia: str = "", coste_reparacion: float = 0.0):
        super().__init__(matricula, estado_mantenimiento, kilometraje, descripcion_averia, coste_reparacion)
        self.capacidad_agua_litros = capacidad_agua_litros
        self.numero_cepillos = numero_cepillos

    def realizar_mantenimiento(self):
        return ("[Barredora] Limpiando " + str(self.numero_cepillos) + " cepillos y revisando bomba de agua en vehículo " + self.matricula + ".")

    def obtener_info(self):
        info = super().obtener_info()
        info.update({
            "capacidad_agua_litros": self.capacidad_agua_litros,
            "numero_cepillos": self.numero_cepillos
        })
        return info