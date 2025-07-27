# Get info country

## Description

get country of america of internet

## Response

- name: string
- capital: string
- currency: string
- language: string
- region: string
- subregion: string
- flag: string
    el atributo flag es una url de tipo png.

## Example

```json
{
    "name": "Peru",
    "capital": "Lima",
    "currency": "Peruvian sol",
    "language": "Aymara",
    "region": "Americas",
    "subregion": "South America",
    "flag": "https://restcountries.com/data/pe.png"
}
```
## steps

buscar la informacion de internet y guardar un archivo en .json en un array, los objetos de cada pais con sus datos.

se guardara en la carpeta "source"

solo paises de america

## stack

- python 3
- pip3
- requests
- json

## enfoque

el programa se realiza con python 3, pip3
debe guardarse en la carpeta "src".

crear un archivo .md con las tecnologias y el enfoque del proyecto en carpeta "src".

el archivo .md se llama "README.md".

codigo fuente en ingles.

## ejecutar el programa

python3 src/get_countries.py
y verificar la existencia del archivo source/countries.json con contenido
