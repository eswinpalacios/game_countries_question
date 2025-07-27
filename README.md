# Country Data Fetcher

## Descripción
Este script obtiene información de países desde la API REST Countries y la guarda en un archivo JSON con un formato específico.

Proyecto trabajado con Windsurf AI y modelo SWE-1.

## Tecnologías Utilizadas
- Python 3
- Bibliotecas:
  - requests: Para realizar peticiones HTTP a la API
  - json: Para manejar el formato JSON
  - typing: Para el tipado estático

## Estructura del Proyecto
```
.
├── src/
│   └── get_countries.py    # Script principal
├── source/
│   └── countries.json      # Archivo de salida generado
├── requirements.txt        # Dependencias
└── README.md              # Este archivo
```

## Instalación
1. Clonar el repositorio
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso
Ejecutar el script:
```bash
python src/get_countries.py
```

El archivo `countries.json` se generará en la carpeta `source/` con los datos de los países en el formato requerido.

## Formato de Salida
El archivo de salida contendrá un array de objetos, donde cada objeto representa un país con la siguiente estructura:

```json
{
  "name": "Nombre del país",
  "capital": "Capital del país",
  "currency": "Moneda principal",
  "language": "Idioma principal"
}
```

## Notas
- Se requiere conexión a internet para obtener los datos de la API
- Los datos se obtienen de REST Countries API (https://restcountries.com/)
