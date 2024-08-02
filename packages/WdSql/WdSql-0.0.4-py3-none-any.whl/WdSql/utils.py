from typing import Tuple

def format_result(data: list, description:Tuple)->list[dict]:
  columnas = [columna[0] for columna in description]
  tabla = []
  for fila in data:
    fila_dict = {}
    for i in range(len(columnas)):
      fila_dict[columnas[i]] = fila[i]
    tabla.append(fila_dict)
  return tabla