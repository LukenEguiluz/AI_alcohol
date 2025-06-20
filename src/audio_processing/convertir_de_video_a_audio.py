import os
import shutil
import subprocess

EXTENSIONES_VIDEO = (".mp4", ".mov", ".mkv")

def convertir_de_video_a_audio(video_path, output_dir):
    log = {
        "archivo_original": video_path,
        "video_copiado": None,
        "audio_generado": None,
        "estado": "iniciado",
        "mensaje": ""
    }

    if not os.path.isfile(video_path):
        log["estado"] = "error"
        log["mensaje"] = f"Archivo no encontrado: {video_path}"
        print(f"❌ {log['mensaje']}")
        return None

    os.makedirs(output_dir, exist_ok=True)

    # Copiar video a carpeta destino
    nombre_archivo = os.path.basename(video_path)
    destino_video = os.path.join(output_dir, nombre_archivo)
    shutil.copy(video_path, destino_video)
    log["video_copiado"] = destino_video
    print(f"📂 Video copiado a: {destino_video}")

    extension = os.path.splitext(nombre_archivo)[1].lower()
    if extension not in EXTENSIONES_VIDEO:
        # No es video: se usa como audio directamente
        log["estado"] = "audio_directo"
        log["mensaje"] = "Archivo tratado como audio directamente (no es video)."
        log["audio_generado"] = destino_video
        return destino_video  # Ruta al archivo copiado

    # Convertir a mp3 dentro del mismo directorio
    base_sin_ext = os.path.splitext(nombre_archivo)[0]
    mp3_path = os.path.join(output_dir, base_sin_ext + ".mp3")

    try:
        subprocess.run([
            "ffmpeg",
            "-i", destino_video,
            "-vn",
            "-ab", "192k",
            "-ar", "44100",
            "-y",
            mp3_path
        ], check=True)

        log["audio_generado"] = mp3_path
        log["estado"] = "convertido"
        log["mensaje"] = f"Audio generado correctamente: {mp3_path}"
        print(f"🎧 Audio convertido guardado en: {mp3_path}")
        return mp3_path

    except subprocess.CalledProcessError as e:
        log["estado"] = "error"
        log["mensaje"] = f"Error de conversión con ffmpeg: {e}"
        print(f"❌ {log['mensaje']}")
        return None

# Uso como script (opcional)
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Uso: python video_a_mp3.py <ruta_video> <output_dir>")
    else:
        ruta_mp3 = convertir_de_video_a_audio(sys.argv[1], sys.argv[2])
        print(f"\n➡️ Resultado: {ruta_mp3}")
