import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from proceso.procesamiento_de_audio import procesamiento_de_audio
from proceso.diarizacion_de_personas import realizar_diarizacion
from proceso.transcripcion_de_audio import transcripcion_de_audio
from proceso.extraer_animales_con_ai import extraer_animales_con_ai
from proceso.convertir_de_video_a_audio import convertir_de_video_a_audio
from proceso.correccion_de_lista_animales import sobreescribir_tiempos
from proceso.graficacion_de_resultados import graficacion_de_resultados

class AIAlcoholGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Procesador de Video con IA")
        self.root.geometry("720x600")
        self.root.configure(bg="#1e1e1e")
        self.archivo = ""

        self.lbl_archivo = tk.Label(root, text="Archivo: Ninguno seleccionado", bg="#1e1e1e", fg="white")
        self.lbl_archivo.pack(pady=10)

        self.btn_select = tk.Button(root, text="Seleccionar Archivo", command=self.seleccionar_archivo, bg="#2d2d2d", fg="white", width=40)
        self.btn_select.pack(pady=5)

        self.btn_folder = tk.Button(root, text="📁 Procesar Carpeta Completa", command=self.procesar_carpeta, bg="#2d2d2d", fg="white", width=40)
        self.btn_folder.pack(pady=5)

        self.btn_todo = tk.Button(root, text="🔁 Ejecutar todo", command=self.ejecutar_todo, bg="#007acc", fg="white", width=40)
        self.btn_todo.pack(pady=10)

        self.btns = [
            ("🎬 Paso 0: Convertir a MP3", self.paso_convertir),
            ("🎧 Paso 1: Preprocesar Audio", self.paso_audio),
            ("🗣️ Paso 2: Diarización", self.paso_diarizacion),
            ("✍️ Paso 3: Transcripción", self.paso_transcripcion),
            ("🦁 Paso 4: Extraer con IA", self.paso_ollama),
            ("📊 Paso 5: Graficar resultados", self.paso_pdf),
        ]
        for texto, comando in self.btns:
            tk.Button(root, text=texto, command=comando, bg="#444", fg="white", width=40).pack(pady=3)

        self.output = scrolledtext.ScrolledText(root, height=12, bg="#252526", fg="white", font=("Consolas", 10))
        self.output.pack(fill="both", expand=True, padx=10, pady=10)

    def log(self, msg):
        self.output.insert(tk.END, msg + "\n")
        self.output.see(tk.END)

    def seleccionar_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=[("Video/Audio", "*.mp4 *.mp3 *.wav *.m4a *.mov *.mkv")])
        if archivo:
            self.archivo = archivo
            self.nombre_base = os.path.splitext(os.path.basename(archivo))[0]
            self.output_dir = os.path.join("resultados", self.nombre_base)
            os.makedirs(self.output_dir, exist_ok=True)
            self.lbl_archivo.config(text=f"Archivo: {archivo}")
            self.log(f"📂 Archivo seleccionado: {archivo}")

    def procesar_carpeta(self):
        carpeta = filedialog.askdirectory()
        if carpeta:
            extensiones_validas = (".mp4", ".mp3", ".wav", ".m4a", ".mov", ".mkv")
            archivos = [f for f in os.listdir(carpeta) if f.lower().endswith(extensiones_validas)]
            if not archivos:
                messagebox.showwarning("Vacío", "No se encontraron archivos válidos en la carpeta.")
                return
            for archivo in archivos:
                ruta = os.path.join(carpeta, archivo)
                self.archivo = ruta
                self.nombre_base = os.path.splitext(os.path.basename(archivo))[0]
                self.output_dir = os.path.join("resultados", self.nombre_base)
                os.makedirs(self.output_dir, exist_ok=True)
                self.log(f"\n🚀 Procesando archivo: {archivo}")
                try:
                    self.ejecutar_todo()
                except Exception as e:
                    self.log(f"❌ Error al procesar {archivo}: {e}")
            self.log("📁 Procesamiento por carpeta completado.")

    def paso_convertir(self):
        self.log("🎬 Paso 0: Convirtiendo a MP3...")
        self.audio_file = convertir_de_video_a_audio(self.archivo, self.output_dir)
        if os.path.exists(self.audio_file):
            self.log(f"✅ Audio listo: {self.audio_file}")
        else:
            self.log("❌ Error al convertir a audio")

    def paso_audio(self):
        self.audio_file = os.path.join(self.output_dir, f"{self.nombre_base}.mp3")
        self.log("🎧 Paso 1: Preprocesando audio...")
        self.processed_audio = procesamiento_de_audio(self.audio_file, output_dir=self.output_dir)
        self.log("✅ Preprocesamiento completado.")

    def paso_diarizacion(self):
        self.processed_audio = os.path.join(self.output_dir, f"{self.nombre_base}_converted_whisper_ready.wav")
        self.log("🗣️ Paso 2: Ejecutando diarización...")
        self.diarization_results = realizar_diarizacion(self.processed_audio, output_dir=self.output_dir)
        self.log("✅ Diarización completada.")

    def paso_transcripcion(self):
        self.processed_audio = os.path.join(self.output_dir, f"{self.nombre_base}_converted_whisper_ready.wav")
        self.log("✍️ Paso 3: Transcribiendo audio...")
        self.transcribed_results = transcripcion_de_audio(self.processed_audio, self.diarization_results, output_dir=self.output_dir)
        self.log("✅ Transcripción completada.")

    def paso_ollama(self):
        path_json = os.path.join(self.output_dir, "palabras_con_tiempos.json")
        self.log("🦁 Paso 4: Ejecutando análisis con IA...")
        extraer_animales_con_ai(
            path_json=path_json,
            model="llama3:8b",
            salida=self.nombre_base,
            output_dir=self.output_dir
        )
        self.log("✅ Extracción completada.")

    def paso_pdf(self):
        lista_animales_path = os.path.join(self.output_dir, "lista_animales.json")
        self.log("📊 Paso 5: Generando gráficas...")
        try:
            graficacion_de_resultados(
                lista_animales_path=lista_animales_path,
                nombre_salida=self.nombre_base,
                output_dir=self.output_dir
            )
            self.log("✅ Gráficas generadas exitosamente.")
        except Exception as e:
            self.log(f"❌ Error generando gráficas: {e}")

    def ejecutar_todo(self):
        try:
            self.paso_convertir()
            self.paso_audio()
            self.paso_diarizacion()
            self.paso_transcripcion()
            self.paso_ollama()
            self.paso_pdf()
            self.log("🎉 Procesamiento COMPLETO")
        except Exception as e:
            self.log(f"❌ Error en ejecución completa: {e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = AIAlcoholGUI(root)
    root.mainloop()


























# import os
# import shutil
# import tkinter as tk
# from tkinter import filedialog, messagebox
# from proceso.procesamiento_de_audio import procesamiento_de_audio
# from proceso.diarizacion_de_personas import realizar_diarizacion
# from proceso.transcripcion_de_audio import transcripcion_de_audio
# from proceso.extraer_animales_con_ai import extraer_animales_con_ai
# from proceso.convertir_de_video_a_audio import convertir_de_video_a_audio
# from proceso.correccion_de_lista_animales import sobreescribir_tiempos
# from proceso.graficacion_de_resultados import graficacion_de_resultados 

# def ai_alcohol(archivo_entrada, output_dir):
#     os.makedirs(output_dir, exist_ok=True)
#     original_dir = os.getcwd()
#     os.chdir(output_dir)

#     nombre_base = os.path.splitext(os.path.basename(archivo_entrada))[0]

#     print(f"\n🚀 Procesando: {archivo_entrada}\n")

#     print("🎬 Paso 0: Verificando si es video y convirtiendo a .mp3 si es necesario...")
#     audio_file = convertir_de_video_a_audio(archivo_entrada, output_dir)
#     if not audio_file or not os.path.exists(audio_file):
#         print("❌ No se pudo obtener archivo de audio válido. Abortando.\n")
#         os.chdir(original_dir)
#         return
#     print(f"✅ Audio listo para procesar: {audio_file}\n")

#     print("🎧 Paso 1: Preprocesando audio...")
#     processed_audio = procesamiento_de_audio(audio_file)
#     print("✅ Preprocesamiento completado.\n")

#     print("🗣️ Paso 2: Ejecutando diarización...")
#     diarization_results = realizar_diarizacion(processed_audio)
#     print("✅ Diarización completada.\n")

#     print("✍️ Paso 3: Transcribiendo audio...")
#     transcribed_results = transcripcion_de_audio(processed_audio, diarization_results)
#     print("✅ Transcripción completada.\n")

#     print("🦁 Paso 4: Ejecutando análisis con IA...")
#     extraer_animales_con_ai(
#         path_json="palabras_con_tiempos.json",
#         model="llama3:8b",
#         salida=nombre_base,
#         output_dir=""
#     )

#     print("✅ Extracción completada.\n")

#     # sobreescribir_tiempos(
#     #     os.path.join(original_dir, output_dir, "palabras_con_tiempos.json"),
#     #     os.path.join(original_dir, output_dir, "lista_animales.json")
#     # )


#     print("📊 Paso 5: Generando graficas de resultados...")
#     try:
#         graficacion_de_resultados(
#             lista_animales_path=os.path.join(original_dir, output_dir, "lista_animales.json"),
#             # palabras_path="palabras_con_tiempos.json",
#             nombre_salida=nombre_base
#         )
#         print("✅ Gráficas generadas exitosamente.\n")
#     except Exception as e:
#         print(f"❌ Error al generar graficas {e}")

#     os.chdir(original_dir)
#     print(f"✅ Procesamiento COMPLETADO para: {archivo_entrada}")
#     print(f"📁 Archivos guardados en: {output_dir}\n{'-'*50}\n")

# def seleccionar_archivo():
#     archivo = filedialog.askopenfilename(filetypes=[("Video/Audio files", "*.mp4 *.mp3 *.wav *.m4a *.mov *.mkv")])
#     if archivo:
#         nombre_base = os.path.splitext(os.path.basename(archivo))[0]
#         output_dir = os.path.join("resultados", nombre_base)
#         ai_alcohol(archivo, output_dir)
#         messagebox.showinfo("Listo", f"Archivo procesado:\n{archivo}")

# def seleccionar_carpeta():
#     carpeta = filedialog.askdirectory()
#     if carpeta:
#         extensiones_validas = (".mp4", ".mp3", ".wav", ".m4a", ".mov", ".mkv")
#         archivos = [f for f in os.listdir(carpeta) if f.lower().endswith(extensiones_validas)]
#         if not archivos:
#             messagebox.showwarning("Vacío", "No se encontraron archivos válidos en la carpeta.")
#             return
#         for archivo in archivos:
#             ruta = os.path.join(carpeta, archivo)
#             nombre_base = os.path.splitext(archivo)[0]
#             output_dir = os.path.join("resultados", nombre_base)
#             ai_alcohol(ruta, output_dir)
#         messagebox.showinfo("Listo", f"Se procesaron {len(archivos)} archivos de la carpeta.")

# def iniciar_gui():
#     root = tk.Tk()
#     root.title("Procesador de Video con IA")
#     root.geometry("420x240")
#     root.resizable(False, False)

#     lbl = tk.Label(root, text="Selecciona un archivo o carpeta para procesar", font=("Arial", 12))
#     lbl.pack(pady=20)

#     btn_archivo = tk.Button(root, text="🎯 Procesar archivo individual", command=seleccionar_archivo, width=35, height=2)
#     btn_archivo.pack(pady=10)

#     btn_carpeta = tk.Button(root, text="📁 Procesar carpeta completa", command=seleccionar_carpeta, width=35, height=2)
#     btn_carpeta.pack(pady=10)

#     root.mainloop()

# if __name__ == "__main__":
#     iniciar_gui()
