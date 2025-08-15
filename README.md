# ElSol-Challenge

## Cómo ejecutar el proyecto

1. Clonar el repositorio y crear un entorno virtual.
2. Instalar dependencias: `pip install -r requirements.txt`.
3. Copiar `.env.example` a `.env` y completar las credenciales de Azure OpenAI.
4. Ejecutar el servidor: `uvicorn app.main:app --reload`.

## 📡 Endpoints

| Método | Endpoint      | Descripción                                         |
|--------|---------------|-----------------------------------------------------|
| POST   | `/transcribe` | Sube un archivo `.wav` o `.mp3` y devuelve la transcripción y datos estructurados. |
| POST   | `/chat`       | Recibe una pregunta y responde usando los datos almacenados en la base vectorial. |

## Testing

```
pytest
```

## Supuestos

- Se utiliza **Azure OpenAI** tanto para la transcripción como para la generación de embeddings y respuestas.
- La base vectorial usa **Qdrant** en modo en memoria para simplificar el despliegue local.
- La extracción de datos estructurados se realiza con patrones simples; para producción se recomienda un LLM dedicado a esta tarea.

## Buenas prácticas aplicadas

- Código modular y documentado.
- Variables sensibles cargadas desde `.env`.
- Pruebas unitarias básicas y prueba opcional de credenciales.
- Tipado estático con `pydantic` y anotaciones de tipos.
