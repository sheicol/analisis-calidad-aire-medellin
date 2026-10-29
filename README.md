# Calidad del aire en Medellín — análisis con Python

Análisis exploratorio de registros publicados en Datos Abiertos Colombia. El script filtra explícitamente el municipio y genera un resumen de cobertura. **Esta revisión corrige el método; los resultados actualizados requieren ejecutar la descarga.**

## Reproducir

```bash
python -m pip install -r requirements.txt
python analisis_calidad_aire_COL.py --municipio Medellín --out outputs
```

Para trabajar con una descarga local de la misma fuente:

```bash
python analisis_calidad_aire_COL.py --input datos_originales.csv --out outputs
```

## Fuente y alcance

[API de origen](https://www.datos.gov.co/resource/kekd-7v7h.json). La descarga recorre páginas ordenadas por identificador. La API es mutable: conservar el CSV de entrada es necesario para reproducir una ejecución exacta.

El script valida columnas, normaliza el nombre del municipio, convierte promedio y año a números y excluye registros sin campos críticos. Si no hay registros válidos de Medellín, falla explícitamente. La cobertura temporal y la cantidad de registros se calculan al ejecutar; no se presuponen.

## Archivos generados

- `outputs/datos_filtrados.csv`: registros válidos del municipio.
- `outputs/cobertura.json`: fuente, fecha de ejecución, filas y años.
- `outputs/resumen.csv`: promedio de registros por contaminante, unidad y estación.
- `outputs/contaminante_*.png`: gráficos separados por contaminante y unidad.

No existe un notebook en esta entrega: el código es `analisis_calidad_aire_COL.py`.

## Limitaciones

Los registros pueden resumir periodos y coberturas diferentes. El promedio simple de valores publicados no equivale a exposición de la población ni a un promedio anual ponderado. No se combinan unidades distintas ni se evalúa cumplimiento normativo.

Los tres PNG históricos en la raíz fueron generados por la versión anterior, sin filtro municipal explícito; no deben interpretarse como resultados validados de Medellín. Los nuevos resultados se guardan en `outputs/`.

## Portafolio

[IBKR Portfolio Analytics](https://github.com/sheicol/ibkr-quant-portfolio-analysis) · [SheyQuant Research Lab](https://github.com/sheicol/quant-research-portfolio)
