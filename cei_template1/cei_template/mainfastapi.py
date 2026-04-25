from http.client import HTTPException
import io

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from cei_template.Fachadataller import Fachadataller
import os
import sys

sys.path.append(os.path.abspath("cei_template"))
app = FastAPI()

# Instanciamos la fachada al arrancar
# Esto cargará el DataFrame una sola vez en memoria
taller = Fachadataller()

@app.get("/")
def home():
    return {"mensaje": "API de Gestión de Taller activa"}

@app.get("/vehiculos")
def obtener_vehiculos():
    """Retorna la lista de vehículos en formato JSON"""
    df = taller.get_vehiculos()
    
    # Convertimos el DataFrame a un formato compatible con JSON (orientado a registros)
    datos = df.to_dict(orient="records")
    return JSONResponse(content=datos)

@app.get("/grafico/{grafico_id}")
def obtener_grafico(grafico_id: int):
    lista_graficos = taller.get_lista_graficos()
    if grafico_id < 0 or grafico_id >= len(lista_graficos):
        raise HTTPException(status_code=404, detail="Gráfico no encontrado en la lista")
    buf = io.BytesIO()
    lista_graficos[grafico_id].savefig(buf, format='png')
    imagen_bytes = buf.getvalue()

    
    return Response(content=imagen_bytes, media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)