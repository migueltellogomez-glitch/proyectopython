import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stopwords_spanish = set(stopwords.words('spanish'))

class visualizacion:
    def __init__(self):
        pass


    
    def mostrar_vehiculos(self, vehiculos):
        tipos = vehiculos['tipo_vehiculo'].value_counts()
        fig =plt.figure(figsize=(8, 5))
        plt.bar(tipos.index, tipos.values, color=['blue', 'orange', 'green'])
        plt.title('Cantidad de Vehículos por Tipo')
        plt.xlabel('Tipo de Vehículo')
        plt.ylabel('Cantidad')
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig
    
    def mostrar_distribucion_kilometraje(self, vehiculos):
        fig =plt.figure(figsize=(8, 5))
        plt.hist(vehiculos['kilometraje'].dropna(), bins=20, color='skyblue', edgecolor='black')
        plt.title('Distribución del Kilometraje de los Vehículos')
        plt.xlabel('Kilometraje')
        plt.ylabel('Frecuencia (Número de vehículos)')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        return fig
    
    def mostrar_estado_vehiculos(self, vehiculos):
        estados = vehiculos['estado_mantenimiento'].value_counts()
        fig =plt.figure(figsize=(7, 7))
        plt.pie(estados.values, labels=estados.index, autopct='%1.1f%%', startangle=140, 
                colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
        plt.title('Proporción de Vehículos por Estado')
        plt.tight_layout()
        return fig
    
    def mostrar_kilometraje_vs_coste(self, vehiculos):
        fig =plt.figure(figsize=(8, 5))
        plt.scatter(vehiculos['kilometraje'], vehiculos['coste_reparacion'], alpha=0.6, color='purple')
        plt.title('Relación entre Kilometraje y Coste de Reparación')
        plt.xlabel('Kilometraje')
        plt.ylabel('Coste de Reparación (€)')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        return fig
    
    def mostrar_coste_por_tipo(self, vehiculos):
        fig =plt.figure(figsize=(10, 6))
        tipos = vehiculos['tipo_vehiculo'].dropna().unique()
        datos_boxplot = [vehiculos[vehiculos['tipo_vehiculo'] == tipo]['coste_reparacion'].dropna() for tipo in tipos]
        plt.boxplot(datos_boxplot, labels=tipos, patch_artist=True, 
                    boxprops=dict(facecolor='lightblue', color='blue'))
        plt.title('Distribución del Coste de Reparación por Tipo de Vehículo')
        plt.xlabel('Tipo de Vehículo')
        plt.ylabel('Coste de Reparación (€)')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        return fig
    
    def mostrar_averias_comunes(self, vehiculos):
        averias = vehiculos['descripcion_averia'].value_counts().head(5)
        fig =plt.figure(figsize=(8, 5))
        plt.barh(averias.index, averias.values, color='coral')
        plt.title('Top 5 Averías Más Comunes')
        plt.xlabel('Cantidad de Casos')
        plt.ylabel('Descripción de la Avería')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        return fig
    

    def mostrar_nube_averias(self, vehiculos):

        stopwords = set(WordCloud().stopwords.union({"vehículo", "matrícula", "kilometraje", "coste", "reparación", "mantenimiento", "avería", "falla", "problema", "daño"}))
        texto_averias = " ".join(vehiculos['descripcion_averia'].dropna().astype(str))
        stopwords.update(stopwords_spanish)
        nube = WordCloud(width=800, height=400, 
                         background_color='white', 
                         colormap='viridis',
                         max_words=100,
                         stopwords=stopwords).generate(texto_averias) 
        fig =plt.figure(figsize=(10, 5))
        plt.imshow(nube, interpolation='bilinear')
        plt.axis('off')
        plt.title('Términos más frecuentes en Descripción de Averías', fontsize=14)
        plt.tight_layout()
        return fig
