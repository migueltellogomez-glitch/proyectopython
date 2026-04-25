from cei_template.vehiculo import Vehiculo


class CamionBasura(Vehiculo):
    def __init__(self, matricula: str, estado_mantenimiento: str, kilometraje: float, 
                 capacidad_toneladas: float, tipo_compactador: str, descripcion_averia: str = "", coste_reparacion: float = 0.0):
        super().__init__(matricula, estado_mantenimiento, kilometraje, descripcion_averia, coste_reparacion)
        self.capacidad_toneladas = capacidad_toneladas
        self.tipo_compactador = tipo_compactador

    def realizar_mantenimiento(self):
        return ("[Camión Basura] Mantenimiento preventivo del compactador " + self.tipo_compactador + " en vehículo " + self.matricula + ".")
    
    

    def obtener_info(self):
        info = super().obtener_info()
        info.update({
            "capacidad_toneladas": self.capacidad_toneladas,
            "tipo_compactador": self.tipo_compactador
        })
        return info