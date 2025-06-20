"""
Ejemplo básico de uso del sistema AI Alcohol.

Este script demuestra cómo procesar un video individual y obtener
métricas de fluidez verbal.
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.audio_processing import (
    convertir_de_video_a_audio,
    procesamiento_de_audio,
    realizar_diarizacion,
    transcripcion_de_audio
)
from src.ai_analysis import extraer_animales_con_ai
from src.visualization import graficacion_de_resultados
import config

def process_single_video(video_path, output_dir=None):
    """
    Procesa un video individual y genera métricas de fluidez.
    
    Args:
        video_path (str): Ruta al archivo de video
        output_dir (str): Directorio de salida (opcional)
    
    Returns:
        dict: Diccionario con las métricas calculadas
    """
    
    # Configurar directorio de salida
    if output_dir is None:
        video_name = Path(video_path).stem
        output_dir = config.RESULTS_DIR / video_name
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🎬 Procesando: {video_path}")
    print(f"📁 Directorio de salida: {output_dir}")
    
    try:
        # Paso 1: Convertir video a audio
        print("🎬 Paso 1: Convirtiendo video a audio...")
        audio_file = convertir_de_video_a_audio(video_path, str(output_dir))
        print(f"✅ Audio generado: {audio_file}")
        
        # Paso 2: Preprocesar audio
        print("🎧 Paso 2: Preprocesando audio...")
        processed_audio = procesamiento_de_audio(audio_file, output_dir=str(output_dir))
        print(f"✅ Audio preprocesado: {processed_audio}")
        
        # Paso 3: Diarización
        print("🗣️ Paso 3: Realizando diarización...")
        diarization_results = realizar_diarizacion(processed_audio, output_dir=str(output_dir))
        print(f"✅ Diarización completada: {diarization_results}")
        
        # Paso 4: Transcripción
        print("✍️ Paso 4: Transcribiendo audio...")
        transcription_results = transcripcion_de_audio(
            processed_audio, 
            diarization_results, 
            output_dir=str(output_dir)
        )
        print(f"✅ Transcripción completada: {transcription_results}")
        
        # Paso 5: Análisis con IA
        print("🦁 Paso 5: Analizando con IA...")
        palabras_json = output_dir / "palabras_con_tiempos.json"
        extraer_animales_con_ai(
            path_json=str(palabras_json),
            model=config.AI_CONFIG["model"],
            salida=Path(video_path).stem,
            output_dir=str(output_dir)
        )
        print("✅ Análisis con IA completado")
        
        # Paso 6: Generar gráficas
        print("📊 Paso 6: Generando gráficas...")
        lista_animales_path = output_dir / "lista_animales.json"
        graficacion_de_resultados(
            lista_animales_path=str(lista_animales_path),
            nombre_salida=Path(video_path).stem,
            output_dir=str(output_dir)
        )
        print("✅ Gráficas generadas")
        
        # Cargar resultados finales
        resumen_path = output_dir / f"resumen_fluidez_{Path(video_path).stem}.json"
        if resumen_path.exists():
            import json
            with open(resumen_path, 'r', encoding='utf-8') as f:
                resultados = json.load(f)
            
            print("\n📊 RESULTADOS FINALES:")
            print(f"   PPM Promedio: {resultados.get('ppm_promedio', 'N/A')}")
            print(f"   PPM Final: {resultados.get('ppm_final', 'N/A')}")
            print(f"   Total Palabras: {resultados.get('total_palabras', 'N/A')}")
            print(f"   Desviación Estándar: {resultados.get('desviacion_estandar', 'N/A')}")
            print(f"   Tiempo Total: {resultados.get('tiempo_final', 'N/A')} segundos")
            
            return resultados
        
        return None
        
    except Exception as e:
        print(f"❌ Error durante el procesamiento: {e}")
        return None

def main():
    """Función principal del ejemplo."""
    
    print("🚀 AI Alcohol - Ejemplo de Uso Básico")
    print("=" * 50)
    
    # Verificar si se proporcionó un archivo de video
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
    else:
        # Usar un archivo de ejemplo si existe
        example_video = config.PROCESSED_DATA_DIR / "video_00001" / "video_00001.mp4"
        if example_video.exists():
            video_path = str(example_video)
            print(f"📹 Usando archivo de ejemplo: {video_path}")
        else:
            print("❌ No se encontró archivo de video.")
            print("Uso: python basic_usage.py <ruta_al_video>")
            return
    
    # Procesar el video
    resultados = process_single_video(video_path)
    
    if resultados:
        print("\n✅ Procesamiento completado exitosamente!")
        print(f"📁 Revisa los resultados en: {config.RESULTS_DIR}")
    else:
        print("\n❌ El procesamiento no se completó correctamente.")

if __name__ == "__main__":
    main() 