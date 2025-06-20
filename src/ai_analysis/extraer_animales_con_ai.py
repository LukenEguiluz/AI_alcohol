import json
import os
import ollama
import requests
import re

def verificar_ollama():
    """Verifica si el servidor local de Ollama está activo."""
    try:
        r = requests.get("http://localhost:11434")
        return r.status_code == 200
    except Exception:
        return False

def limpiar_posible_json(texto):
    """Limpia el texto crudo recibido para intentar extraer un bloque JSON válido."""
    texto = "\n".join([line for line in texto.splitlines() if not line.strip().startswith("//")])
    texto = re.sub(r'//.*', '', texto)
    start = texto.find("[")
    end = texto.rfind("]") + 1
    if start >= 0 and end > start:
        return texto[start:end]
    return texto.strip()

def extraer_animales_con_ai(path_json="palabras_con_tiempos.json", model="llama3:8b", salida="salida", output_dir="."):
    """
    Extrae animales explícitos y posibles menciones erróneas desde un texto plano generado a partir de palabras con tiempo.
    El modelo de IA no tiene memoria previa gracias a un reset explícito.
    """
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    if not verificar_ollama():
        print("❌ Ollama no está corriendo. Ejecuta `ollama serve` o abre la app.")
        return

    try:
        with open(path_json, 'r', encoding='utf-8') as f:
            palabras = json.load(f)
    except FileNotFoundError as e:
        print(f"❌ Archivo no encontrado: {e.filename}")
        return

    texto_completo = "\n".join(f"[start: {p['start']}] {p['word']}" for p in palabras)

    prompt_lista = f"""
    Tienes una lista de palabras extraídas de una transcripción de audio, cada una con su marca de tiempo (start time). Tu tarea es detectar qué palabras son nombres de **animales reales**, sin hacer suposiciones. 

    También debes identificar palabras que **podrían ser animales mal pronunciados o mal escritos**, por ejemplo "berrego" (en lugar de "borrego"). No asumas ni corrijas: incluye la palabra **tal cual aparece**.

    Devuelve solo una lista JSON con objetos que contengan:

    - "word": la palabra exacta como aparece en el texto
    - "start": el tiempo en segundos (float)
    - "posible": true si es una posible mención errónea o dudosa, false si es una mención clara y correcta

    Instrucciones importantes:
    - Solo considera palabras presentes en el texto.
    - No inventes animales.
    - No corrijas la ortografía.
    - Incluye todos los animales, incluso si se repiten.
    - No agrupes ni ordenes alfabéticamente.
    - No expliques nada fuera del JSON.

    Instruccion más importante!!!!!
    NO INCLUYAS NADA ADICIONAL AL JSON QUE TE ESTOY PIDIENDO, O SEA NO QUIERO QUE INCLUYAS TEXTO ADICIONAL!!!!!!!
    Revisa todas las palabras para ver todos los posibles animales y los que son!!!!!

    Ejemplo de salida:

    [
    {{ "word": "perro", "start": 12.3, "posible": false }},
    {{ "word": "libra", "start": 21.4, "posible": true }}
    ]

    Texto (palabras transcritas):
    {texto_completo}
    """

    try:
        ollama.chat(model=model, messages=[{'role': 'system', 'content': 'reset'}])

        response_lista = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': prompt_lista}]
        )
        raw_content = response_lista['message']['content']
        print("\n🔍 Respuesta cruda de la IA (raw_content):\n", raw_content)

        with open(os.path.join(output_dir, f"respuesta_raw_lista_{salida}.txt"), 'w', encoding='utf-8') as f:
            f.write(raw_content)

        try:
            data_animales = json.loads(raw_content)
        except json.JSONDecodeError:
            print("⚠️ JSON no válido. Intentando limpiar...")
            data_animales = json.loads(limpiar_posible_json(raw_content))

        if not isinstance(data_animales, list):
            print("⚠️ El contenido devuelto no es una lista válida.")
            return

        detectados = []
        for item in data_animales:
            if "word" in item and "start" in item:
                detectados.append({
                    "word": item["word"],
                    "start": float(item["start"]),
                    "posible": bool(item.get("posible", False))
                })

        print(f"🧮 Total de animales detectados: {len(detectados)}")
        if not detectados:
            print("⚠️ No se detectaron animales.")

        resultado_path = os.path.join(output_dir, "lista_animales.json")
        with open(resultado_path, "w", encoding="utf-8") as f:
            json.dump(detectados, f, indent=2, ensure_ascii=False)
        print(f"✅ Archivo guardado: {resultado_path}")

        # Nuevo prompt para grupos semánticos
        palabras_animales = [d["word"] for d in detectados]
        prompt_grupos = f"""
        A continuación se presenta una lista de nombres de animales. Agrúpalos en categorías semánticas lógicas (por ejemplo: animales domésticos, salvajes, marinos, aves, insectos, etc.)

        Devuelve solo un JSON con la siguiente estructura:

        {{
          "domésticos": ["perro", "gato"],
          "aves": ["colibrí", "loro"],
          "salvajes": ["león", "tigre"]
        }}

        No incluyas explicaciones ni texto adicional. Solo el JSON. 

        Recuerda que si agregas un grupo semantico, debe tener como mínimo 1 animal por grupo semántico.

        Lista:
        {json.dumps(palabras_animales, ensure_ascii=False)}
        """

        response_grupos = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': prompt_grupos}]
        )
        raw_grupos = response_grupos['message']['content']

        try:
            grupos = json.loads(raw_grupos)
        except json.JSONDecodeError:
            grupos = json.loads(limpiar_posible_json(raw_grupos))

        grupos_path = os.path.join(output_dir, "grupos_semanticos.json")
        with open(grupos_path, "w", encoding="utf-8") as f:
            json.dump(grupos, f, indent=2, ensure_ascii=False)
        print(f"✅ Grupos semánticos guardados en: {grupos_path}")

    except Exception as e:
        print(f"⚠️ Error al interactuar con Ollama: {e}")















########## Deteccion de animales con tiempos####


# import json
# import os
# import ollama
# import requests

# def verificar_ollama():
#     try:
#         r = requests.get("http://localhost:11434")
#         return r.status_code == 200
#     except Exception:
#         return False

# def limpiar_posible_json(texto):
#     start = texto.find("{")
#     end = texto.rfind("}") + 1
#     if start >= 0 and end > start:
#         return texto[start:end]
#     start = texto.find("[")
#     end = texto.rfind("]") + 1
#     if start >= 0 and end > start:
#         return texto[start:end]
#     return texto.strip()

# def extraer_animales_con_ai(path_json="aligned_transcription.json", model="mistral", salida="salida", output_dir="."):
#     output_dir = os.path.abspath(output_dir)
#     os.makedirs(output_dir, exist_ok=True)

#     if not verificar_ollama():
#         print("❌ Ollama no está corriendo. Ejecuta `ollama serve` o abre la app.")
#         return

#     try:
#         with open(path_json, 'r', encoding='utf-8') as f:
#             json_data = json.load(f)
#         with open("palabras_con_tiempos.json", "r", encoding="utf-8") as f:
#             palabras_con_tiempos = json.load(f)
#     except FileNotFoundError as e:
#         print(f"❌ Archivo no encontrado: {e.filename}")
#         return

#     # Convertir a texto plano
#     bloques = []
#     for bloque in json_data:
#         start = bloque.get("start_time")
#         end = bloque.get("end_time")
#         text = bloque.get("transcript", "")
#         bloques.append(f"[start_time: {start:.2f}, end_time: {end:.2f}] {text}")
#     transcripcion_texto = "\n".join(bloques)

#     # === PROMPT actualizado: Animales y posibles animales ===
#     prompt_lista = f"""
# Extrae todos los animales mencionados en el texto. Devuelve dos listas:

# 1. Una lista con los animales que están explícitamente escritos (sin repeticiones).
# 2. Una lista con posibles errores o palabras que probablemente intentaban ser animales aunque estén mal escritas.

# No corrijas las palabras. Devuélvelas como están en el texto. Formato JSON:
# {{
#   "exactos": ["perro", "elefante"],
#   "posibles": ["libra", "berrego"]
# }}

# Texto:
# {transcripcion_texto}
# """

#     try:
#         response_lista = ollama.chat(
#             model=model,
#             messages=[{'role': 'user', 'content': prompt_lista}]
#         )
#         raw_content = response_lista['message']['content']
#         print("\n🔍 Respuesta de la IA (animales + posibles):\n", raw_content)

#         with open(os.path.join(output_dir, f"respuesta_raw_lista_{salida}.txt"), 'w', encoding='utf-8') as f:
#             f.write(raw_content)

#         try:
#             data_animales = json.loads(raw_content)
#         except json.JSONDecodeError:
#             print("⚠️ JSON no válido. Intentando limpiar...")
#             data_animales = json.loads(limpiar_posible_json(raw_content))

#         exactos = set(data_animales.get("exactos", []))
#         posibles = set(data_animales.get("posibles", []))
#     except Exception as e:
#         print("⚠️ Error al generar lista de animales:", e)
#         return

#     # Buscar palabras con start time
#     detectados = []
#     for palabra in palabras_con_tiempos:
#         texto = palabra["word"]
#         start = palabra["start"]
#         if texto in exactos:
#             detectados.append({"word": texto, "start": start, "posible": False})
#         elif texto in posibles:
#             detectados.append({"word": texto, "start": start, "posible": True})

#     resultado_path = os.path.join(output_dir, "lista_animales.json")
#     with open(resultado_path, "w", encoding="utf-8") as f:
#         json.dump(detectados, f, indent=2, ensure_ascii=False)
#     print(f"✅ Animales detectados con tiempo guardado en: {resultado_path}")




############## Viejo Viejo


# import json
# import os
# import ollama
# import requests

# def verificar_ollama():
#     try:
#         r = requests.get("http://localhost:11434")
#         return r.status_code == 200
#     except Exception:
#         return False

# def limpiar_posible_json(texto):
#     # Intenta extraer el primer bloque JSON válido ({} o [])
#     start = texto.find("{")
#     end = texto.rfind("}") + 1
#     if start >= 0 and end > start:
#         return texto[start:end]
#     start = texto.find("[")
#     end = texto.rfind("]") + 1
#     if start >= 0 and end > start:
#         return texto[start:end]
#     return texto.strip()

# def extraer_animales_con_ai(path_json="aligned_transcription.json", model="mistral", salida="salida", output_dir="."):
#     output_dir = os.path.abspath(output_dir)
#     os.makedirs(output_dir, exist_ok=True)

#     if not verificar_ollama():
#         print("❌ Ollama no está corriendo. Ejecuta `ollama serve` o abre la app.")
#         return

#     try:
#         with open(path_json, 'r', encoding='utf-8') as f:
#             json_data = json.load(f)
#     except FileNotFoundError:
#         print(f"❌ Archivo no encontrado: {path_json}")
#         return

#     # Convertir a texto plano
#     bloques = []
#     for bloque in json_data:
#         start = bloque.get("start_time")
#         end = bloque.get("end_time")
#         text = bloque.get("transcript", "")
#         bloques.append(f"[start_time: {start:.2f}, end_time: {end:.2f}] {text}")
#     transcripcion_texto = "\n".join(bloques)

#     # === PROMPT 1: Lista de animales ===
#     prompt_lista = f"""
# Extrae todos los animales mencionados en el texto, manteniendo la forma en la que se encuentran en el JSON. Devuelve solo una lista en formato JSON, sin tiempos, sin repeticiones. No asumas cosas que no estan en el JSON, solo lo que esta escrito.

# Ejemplo:
# [
#   "elefante",
#   "gatos",
#   "perritos",
#   "perro",
#   .
#   .
#   .
# ]

# Texto:
# {transcripcion_texto}
# """
#     try:
#         response_lista = ollama.chat(
#             model=model,
#             messages=[{'role': 'user', 'content': prompt_lista}]
#         )
#         raw_content = response_lista['message']['content']
#         print("\n🔍 Respuesta de la IA (lista de animales):\n", raw_content)

#         # Guardar respuesta cruda
#         with open(os.path.join(output_dir, f"respuesta_raw_lista_{salida}.txt"), 'w', encoding='utf-8') as f:
#             f.write(raw_content)

#         try:
#             animales_unicos = json.loads(raw_content)
#         except json.JSONDecodeError:
#             print("⚠️ JSON no válido. Intentando limpiar...")
#             animales_unicos = json.loads(limpiar_posible_json(raw_content))

#         lista_path = os.path.join(output_dir, "lista_animales.json")
#         with open(lista_path, 'w', encoding='utf-8') as f:
#             json.dump(animales_unicos, f, indent=2, ensure_ascii=False)
#         print(f"✅ Lista de animales guardada en: {lista_path}")
#     except Exception as e:
#         print("⚠️ Error al generar lista de animales:", e)
#         return

#     # === PROMPT 2: Agrupación semántica ===
#     prompt_grupos = f"""
# Agrupa todos los animales mencionados en el siguiente texto por grupos semánticos (por ejemplo: animales marinos, mamíferos terrestres, aves, felinos, etc.).

# Devuelve el resultado en formato JSON como:
# {{
#   "mamíferos terrestres": ["elefante", "león"],
#   "animales marinos": ["delfín", "pulpo"]
# }}

# Texto:
# {transcripcion_texto}
# """
#     try:
#         response_grupos = ollama.chat(
#             model=model,
#             messages=[{'role': 'user', 'content': prompt_grupos}]
#         )
#         raw_content = response_grupos['message']['content']
#         print("\n🔍 Respuesta de la IA (agrupación semántica):\n", raw_content)

#         # Guardar respuesta cruda
#         with open(os.path.join(output_dir, f"respuesta_raw_grupos_{salida}.txt"), 'w', encoding='utf-8') as f:
#             f.write(raw_content)

#         try:
#             grupos = json.loads(raw_content)
#         except json.JSONDecodeError:
#             print("⚠️ JSON no válido. Intentando limpiar...")
#             grupos = json.loads(limpiar_posible_json(raw_content))

#         agrupados_path = os.path.join(output_dir, "animales_agrupados.json")
#         with open(agrupados_path, 'w', encoding='utf-8') as f:
#             json.dump(grupos, f, indent=2, ensure_ascii=False)
#         print(f"✅ Agrupación semántica guardada en: {agrupados_path}")
#     except Exception as e:
#         print("⚠️ Error al generar agrupación semántica:", e)
