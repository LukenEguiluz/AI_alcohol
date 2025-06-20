import json
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import os
import pandas as pd

# === Fluidez acumulada por palabra ===
def calcular_fluidez_acumulada(data):
    data = sorted(data, key=lambda x: x['start'])
    tiempos = []
    fluidez = []

    tiempo_inicio = data[0]['start']

    for i, entrada in enumerate(data, 1):
        t = entrada['start'] - tiempo_inicio
        minutos = t / 60
        fpm = i / minutos if minutos > 0 else 0
        tiempos.append(round(t, 2))
        fluidez.append(fpm)

    return tiempos, fluidez

# === Función principal solo con evolución real ===
def graficacion_de_resultados(lista_animales_path="lista_animales.json", nombre_salida="salida", incluir_posibles=True, output_dir="."):
    with open(lista_animales_path, encoding="utf-8") as f:
        animales = json.load(f)

    if not animales:
        print("⚠️ No se encontraron animales en el archivo.")
        return

    animales_filtrados = [
        a for a in animales
        if incluir_posibles or not a.get("posible", False)
    ]

    if not animales_filtrados:
        print("⚠️ No hay animales confirmados para graficar.")
        return

    # Calcular fluidez verbal acumulada
    tiempos, fluidez = calcular_fluidez_acumulada(animales_filtrados)

    # Graficar evolución real
    plt.figure(figsize=(10, 5))
    plt.plot(tiempos, fluidez, marker='o', linestyle='-', label="Fluidez acumulada")
    plt.title("Evolución de la Fluidez Verbal (Real)")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Palabras por minuto acumuladas")
    plt.grid(True)
    plt.xlim(0, tiempos[-1] + 5)
    plt.legend()
    plt.tight_layout()

    img_path = os.path.join(output_dir, f"fluidez_{nombre_salida}.png")
    plt.savefig(img_path)
    plt.close()

    # Estadísticas
    media_fpm = float(np.mean(fluidez))
    std_fpm = float(np.std(fluidez))
    fpm_final = float(fluidez[-1])
    tiempo_inicial = round(tiempos[0], 2)
    tiempo_final = round(tiempos[-1], 2)
    total_palabras = len(animales_filtrados)
    nombres_animales = [a['word'] for a in animales_filtrados if 'word' in a]

    # Cargar grupos semánticos si existe
    grupos_semanticos = {}
    conteo_por_grupo = {}
    grupos_path = os.path.join(output_dir, "grupos_semanticos.json")
    if os.path.exists(grupos_path):
        with open(grupos_path, encoding="utf-8") as f:
            grupos_semanticos = json.load(f)

            print(f"Grupos semanticos items: {grupos_semanticos.items()}")

        for grupo, lista in grupos_semanticos.items():
            print(f"Lista: {lista}")
            conteo = len(lista)
            conteo_por_grupo[grupo] = conteo
            print(f"Grupo: {grupo} - Conteo: {conteo}")

    resumen = {
        "tiempo_inicio": tiempo_inicial,
        "tiempo_final": tiempo_final,
        "total_palabras": total_palabras,
        "ppm_promedio": round(media_fpm, 2),
        "desviacion_estandar": round(std_fpm, 2),
        "ppm_final": round(fpm_final, 2),
        "animales": nombres_animales,
        "grupos_semanticos": grupos_semanticos,
        "conteo_por_grupo": conteo_por_grupo
    }

    print(f"✅ Fluidez promedio: {media_fpm:.2f} ppm | Desviación estándar: {std_fpm:.2f} | Final: {fpm_final:.2f} ppm")
    print(f"📈 Gráfica guardada como: {img_path}")

    # Guardar resumen en JSON
    json_path = os.path.join(output_dir, f"resumen_fluidez_{nombre_salida}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(resumen, f, indent=2, ensure_ascii=False)
    print(f"📄 Resumen guardado en: {json_path}")

    # Guardar también en Excel
    excel_path = os.path.join(output_dir, f"fluidez_{nombre_salida}.xlsx")
    df = pd.DataFrame([resumen])
    df.drop(columns=["animales", "grupos_semanticos"], errors="ignore").to_excel(excel_path, index=False)
    print(f"📄 Excel guardado en: {excel_path}")














# import json
# import matplotlib.pyplot as plt
# from scipy.interpolate import CubicSpline
# import numpy as np
# from collections import Counter
# import os
# import pandas as pd

# def calcular_fluidez_por_palabra(data):
#     data = sorted(data, key=lambda x: x['start'])
#     tiempos = [0.0]  # tiempo relativo 0
#     fluidez = [1.0]  # valor inicial fijo

#     for i in range(1, len(data)):
#         t_actual = data[i]['start']
#         t_anterior = data[i - 1]['start']
#         intervalo = t_actual - t_anterior
#         t_relativo = t_actual - data[0]['start']

#         if intervalo > 0:
#             fpm = 1 / (intervalo / 60)
#         else:
#             fpm = 0

#         tiempos.append(round(t_relativo, 2))
#         fluidez.append(fpm)

#     return tiempos, fluidez


# def graficacion_de_resultados(lista_animales_path="lista_animales.json", nombre_salida="salida", incluir_posibles=True):
#     with open(lista_animales_path, encoding="utf-8") as f:
#         animales = json.load(f)

#     if not animales:
#         print("⚠️ No se encontraron animales en el archivo.")
#         return

#     animales_filtrados = [
#         a for a in animales
#         if incluir_posibles or not a.get("posible", False)
#     ]

#     if not animales_filtrados:
#         print("⚠️ No hay animales confirmados para graficar.")
#         return

#     tiempos, fluidez = calcular_fluidez_por_palabra(animales_filtrados)

#     # Agregar punto de caída a 0 después del último
#     ultimo_tiempo = tiempos[-1]
#     tiempos.append(ultimo_tiempo + 8)
#     fluidez.append(0)

#     # Crear spline con el nuevo punto añadido
#     spline = CubicSpline(tiempos, fluidez)

#     # Ajustar el rango de interpolación
#     limite_interp = max(70, tiempos[-1])
#     tiempos_interp = np.linspace(tiempos[0], limite_interp, 500)
#     fluidez_interp = spline(tiempos_interp)
#     fluidez_interp = np.clip(fluidez_interp, 0, None)

#     # Graficar
#     plt.figure(figsize=(10, 5))
#     plt.plot(tiempos[:-1], fluidez[:-1], 'o', label="Original")
#     plt.plot(tiempos_interp, fluidez_interp, '-', label="Spline cúbico + caída")
#     plt.title("Evolución de la Fluidez Verbal")
#     plt.xlabel("Tiempo (s)")
#     plt.ylabel("Palabras por minuto acumuladas")
#     plt.grid(True)
#     plt.xlim(0, limite_interp)
#     plt.legend()
#     plt.tight_layout()
#     plt.savefig(f"fluidez_{nombre_salida}.png")
#     plt.close()

#     media_fpm = float(np.mean(fluidez[:-1]))
#     std_fpm = float(np.std(fluidez[:-1]))

#     nombres = [a["word"].lower() for a in animales_filtrados]
#     contador = Counter(nombres)
#     repetidos = {k: v for k, v in contador.items() if v > 1}

#     print(f"✅ Fluidez promedio: {media_fpm:.2f} ppm | Desviación estándar: {std_fpm:.2f}")
#     print(f"📈 Gráfica guardada como: fluidez_{nombre_salida}.png")
#     print(f"🔁 Animales repetidos: {repetidos if repetidos else 'Ninguno'}")

#     resumen = {
#         "fluidez_promedio": round(media_fpm, 2),
#         "desviacion_estandar": round(std_fpm, 2),
#         "total_palabras": len(animales_filtrados),
#         "palabras_repetidas": repetidos
#     }

#     tiempo_base = animales_filtrados[0]['start']
#     animales_ajustados = [{
#         "word": a["word"],
#         "start": round(a["start"] - tiempo_base, 2),
#         "posible": a.get("posible", False)
#     } for a in animales_filtrados]

#     with open(f"lista_de_animales_mencionados_{nombre_salida}.json", "w", encoding="utf-8") as f:
#         json.dump(animales_ajustados, f, indent=2, ensure_ascii=False)
#     print(f"📄 Lista ajustada guardada en: lista_de_animales_mencionados_{nombre_salida}.json")

#     palabras_por_tiempo = {round(a['start'] - tiempo_base, 2): a['word'] for a in animales_filtrados}
#     df_interp = pd.DataFrame({
#         "tiempo (s)": tiempos_interp,
#         "palabra": [palabras_por_tiempo.get(round(t, 2), "") for t in tiempos_interp],
#         "palabras por minuto acumuladas": fluidez_interp
#     })

#     df_interp.to_excel(f"fluidez_{nombre_salida}.xlsx", index=False)
#     print(f"📄 Excel con interpolación guardado en: fluidez_{nombre_salida}.xlsx")

#     with open(f"resumen_fluidez_{nombre_salida}.json", "w", encoding="utf-8") as f:
#         json.dump(resumen, f, indent=2, ensure_ascii=False)
#     print(f"📄 Resumen guardado en: resumen_fluidez_{nombre_salida}.json")
