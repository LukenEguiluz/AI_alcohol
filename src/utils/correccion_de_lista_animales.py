import json
import unicodedata
import re

def normalize(text):
    text = text.lower()
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )  # Elimina tildes
    text = re.sub(r'[^\wñ]+', '', text)  # Elimina puntuación
    return text

def sobreescribir_tiempos(transcripcion_path, ia_path):
    # Cargar los dos JSON
    with open(transcripcion_path, encoding="utf-8") as f:
        transcripcion = json.load(f)
    with open(ia_path, encoding="utf-8") as f:
        ia = json.load(f)

    # Indexar tiempos por palabra normalizada
    tiempos_disponibles = {}
    for palabra in transcripcion:
        key = normalize(palabra["word"])
        tiempos_disponibles.setdefault(key, []).append(palabra["start"])

    usados = set()  # Para evitar reutilizar tiempos

    # Sobrescribir los tiempos en el JSON de la IA
    for entrada in ia:
        key = normalize(entrada["word"])
        if key in tiempos_disponibles:
            for t in tiempos_disponibles[key]:
                if t not in usados:
                    entrada["start"] = t
                    usados.add(t)
                    break
            else:
                print(f"⚠️ Todos los tiempos para '{entrada['word']}' ya fueron usados.")
        else:
            print(f"⚠️ Palabra '{entrada['word']}' no encontrada en transcripción.")

    # Sobrescribe el archivo original de IA con los tiempos corregidos
    with open(ia_path, "w", encoding="utf-8") as f:
        json.dump(ia, f, indent=2, ensure_ascii=False)

    print(f"✅ Tiempos sobrescritos directamente en: {ia_path}")

# USO
# sobreescribir_tiempos("transcripcion.json", "ia_animales.json")
