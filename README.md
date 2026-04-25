cei_template
------------


![alt text](https://badgen.net/badge/python/3.10/cyan?icon=pypi)


Fachada Taller - Sistema de Gestión de Flotas
Este módulo implementa el patrón de diseño Facade (Fachada) para simplificar la interacción con el sistema de gestión de vehículos, base de datos y visualización de datos de un taller.

## Descripción
La clase Fachadataller actúa como un punto de entrada único que coordina diversas sub-librerías (BaseDeDatos, Visualizacion, VehiculoFactory, etc.). Permite gestionar el ciclo de vida de los vehículos, realizar reparaciones, mantenimientos y generar informes visuales sin necesidad de interactuar directamente con la complejidad interna del sistema.

## Patrones de Diseño Utilizados
Facade: Proporciona una interfaz unificada y simplificada.

Singleton: Utilizado en RegistroFlota para asegurar una única instancia de la flota de vehículos.

Factory: Utilizado en VehiculoFactory para la creación de objetos de tipo vehículo a partir de datos.

## Funcionalidades Principales
1. Gestión de Flota
Carga Automática: Al inicializarse, carga la lista de vehículos desde la base de datos.

Agregar Vehículos: Permite añadir nuevos registros a la flota en memoria.

Búsqueda: Localización de vehículos específicos mediante su matrícula.

2. Operaciones de Taller
Reparar Vehículo: Gestiona la reparación de averías de un vehículo específico.

Mantenimiento: Ejecuta las rutinas de mantenimiento preventivo.

3. Persistencia y Análisis
Sincronización: Actualiza los cambios realizados en la flota de vuelta a la base de datos persistente.

Visualización: Genera una batería de gráficos estadísticos (kilometraje, costes, estados, averías comunes, etc.).

## Gráficos Disponibles
El método get_lista_graficos() devuelve una lista con las siguientes representaciones visuales:

Inventario general de vehículos.

Distribución de kilometraje.

Estado actual de la flota (operativos vs. en reparación).

Relación entre kilometraje y costes.

Desglose de costes por tipo de vehículo.

Análisis de averías más frecuentes.

Nube de palabras de descripciones de averías.

## Ejemplo de Uso
Python
from your_module import Fachadataller

# Inicializar la fachada
taller = Fachadataller()

# Obtener todos los vehículos
flota = taller.get_vehiculos()

# Reparar un vehículo específico
resultado = taller.reparar_vehiculo("ABC-1234")
print(resultado)

# Generar reportes visuales
graficos = taller.get_lista_graficos()

# Guardar cambios en la base de datos
taller.actualizar_base_de_datos()
# Requisitos
ver requirement.txt

Python = 3.14.3

Módulos internos: cei_template (BaseDeDatos, Visualizacion, Singleton, VehiculosFactory)


## Credits

### Owner
- Your Name <miguel.tello.gomez@alumnoscei.es>
