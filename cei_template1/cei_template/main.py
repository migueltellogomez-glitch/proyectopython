import os
import sys
from cei_template.Fachadataller import Fachadataller

sys.path.append(os.path.abspath("cei_template"))

def main():
    
    taller = Fachadataller()
    print(taller.get_vehiculos())
    for i, grafico in enumerate(taller.get_lista_graficos()):
        grafico.show()
        grafico.savefig(os.path.join(os.path.dirname(__file__), "graficos", "imagen_" + str(i) + ".png"))

    print(taller.realizar_mantenimiento("ABC123"))
    print(taller.realizar_mantenimiento("BAB654"))
    taller.agregar_vehiculo(taller.vehiculo_factory.crear_vehiculo("Camion Basura", {
        "matricula": "NEW999",
        "estado_mantenimiento": "Bueno",
        "kilometraje": 5000,
        "capacidad_toneladas": 10,
        "tipo_compactador": "Compactador de tornillo"
    }))
    taller.actualizar_base_de_datos()
    print([vehiculo.obtener_info() for vehiculo in taller.get_vehiculos()])
    taller.reparar_vehiculo("NEW999")
    print(taller.get_vehiculo_por_matricula("NEW999").obtener_info())
    

    


if __name__ == '__main__':
    main()
