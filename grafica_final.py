import pandas as pd
import json
import os

# === RUTAS ===
asociaciones_path = "base/asociaciones.json"
sav_path = "base/datos_pacientes.sav"
carpeta_resultados = "resultados"

# === CARGAR ASOCIACIONES ===
with open(asociaciones_path, "r", encoding="utf-8") as f:
    asociaciones = json.load(f)

# Invertir asociaciones: nombre -> video
nombre_a_video = {v.strip().upper(): k for k, v in asociaciones.items()}

# === CARGAR DATOS .SAV ===
df = pd.read_spss(sav_path)

# === ASIGNAR VIDEO SEGÚN NOMBRE ===
df["video"] = df["NOMBRE"].str.upper().map(nombre_a_video)
df["ppm_promedio"] = None

# === EXTRAER PPM DESDE JSON POR VIDEO ===
for idx, row in df.iterrows():
    video = row["video"]
    if pd.notna(video):
        resumen_path = os.path.join(carpeta_resultados, video, f"resumen_fluidez_{video}.json")
        if os.path.exists(resumen_path):
            try:
                with open(resumen_path, "r", encoding="utf-8") as f:
                    resumen = json.load(f)
                    df.at[idx, "ppm_promedio"] = resumen.get("ppm_promedio")
            except Exception as e:
                print(f"⚠️ Error al procesar {resumen_path}: {e}")

# === CREAR NUEVO DATAFRAME SOLO CON NOMBRE, DNOpositivos Y PPM ===
df_salida = df[["NOMBRE", "DNOpositivos", "ppm_promedio"]].copy()

# === GUARDAR CSV DE RESULTADO ===
df_salida.to_csv("salida_ppm_por_paciente.csv", index=False, encoding="utf-8")
print("✅ Archivo generado: salida_ppm_por_paciente.csv")
