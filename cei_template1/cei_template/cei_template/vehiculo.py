from abc import ABC, abstractmethod

class Vehiculo(ABC):
    def __init__(self, matricula: str, estado_mantenimiento: str, kilometraje: float, descripcion_averia: str = "", coste_reparacion: float = 0.0):
        self.matricula = matricula
        self.estado_mantenimiento = estado_mantenimiento
        self.kilometraje = kilometraje
        self.descripcion_averia = descripcion_averia
        self.coste_reparacion = coste_reparacion

    @abstractmethod
    def realizar_mantenimiento(self):
        pass

    def reparar_averia(self):

        self.estado_mantenimiento = "Reparado"
        return "Vehículo " + self.matricula + " reparado. Descripción de la avería: " + self.descripcion_averia + ". Coste de reparación: " + str(self.coste_reparacion) + "."

    def obtener_info(self):
        tipo = self.__class__.__name__
        tipo = ''.join([' ' + c if c.isupper() else c for c in tipo]).strip()
  

        return {
            "matricula": self.matricula,
            "estado_mantenimiento": self.estado_mantenimiento,
            "kilometraje": self.kilometraje,
            "tipo_vehiculo": tipo,
            "descripcion_averia": self.descripcion_averia,
            "coste_reparacion": self.coste_reparacion
        }