# Documentación Técnica - AI Alcohol

## Arquitectura del Sistema

### 1. Pipeline de Procesamiento

El sistema sigue un pipeline de 6 pasos secuenciales:

```
Video Input → Audio Conversion → Audio Processing → Diarization → Transcription → AI Analysis → Visualization
```

#### 1.1 Conversión de Video a Audio
- **Módulo**: `src/audio_processing/convertir_de_video_a_audio.py`
- **Tecnología**: FFmpeg (via pydub)
- **Formato de salida**: MP3
- **Configuración**: 16kHz, mono

#### 1.2 Preprocesamiento de Audio
- **Módulo**: `src/audio_processing/procesamiento_de_audio.py`
- **Funciones**:
  - Normalización de volumen
  - Filtrado de ruido
  - Conversión a formato WAV para Whisper
- **Configuración**: 16kHz, 16-bit PCM

#### 1.3 Diarización
- **Módulo**: `src/audio_processing/diarizacion_de_personas.py`
- **Tecnología**: Pyannote.audio
- **Objetivo**: Identificar segmentos de habla por hablante
- **Salida**: JSON con segmentos temporales

#### 1.4 Transcripción
- **Módulo**: `src/audio_processing/transcripcion_de_audio.py`
- **Tecnología**: OpenAI Whisper
- **Modelo**: Whisper base (español)
- **Salida**: Texto con marcas de tiempo precisas

#### 1.5 Análisis con IA
- **Módulo**: `src/ai_analysis/extraer_animales_con_ai.py`
- **Tecnología**: Ollama + Llama3:8b
- **Funciones**:
  - Detección de nombres de animales
  - Identificación de posibles errores de pronunciación
  - Clasificación semántica

#### 1.6 Visualización
- **Módulo**: `src/visualization/graficacion_de_resultados.py`
- **Tecnologías**: Matplotlib, Pandas
- **Salidas**:
  - Gráficas de fluidez temporal
  - Estadísticas descriptivas
  - Reportes en Excel/JSON

### 2. Estructura de Datos

#### 2.1 Archivos de Entrada
```
data/raw/
├── asociaciones.json          # Mapeo video → nombre paciente
└── datos_pacientes.sav        # Datos clínicos (SPSS)
```

#### 2.2 Archivos de Procesamiento
```
data/processed/video_XXXXX/
├── video_XXXXX.mp3           # Audio extraído
├── video_XXXXX_converted_whisper_ready.wav  # Audio procesado
├── diarization_results.json   # Resultados de diarización
├── aligned_transcription.json # Transcripción con tiempos
├── palabras_con_tiempos.json  # Palabras individuales
├── lista_animales.json        # Animales detectados
├── grupos_semanticos.json     # Clasificación semántica
├── resumen_fluidez_XXXXX.json # Métricas finales
└── fluidez_XXXXX.png          # Gráfica de fluidez
```

#### 2.3 Estructura de Resultados
```json
{
  "tiempo_inicio": 0.0,
  "tiempo_final": 49.34,
  "total_palabras": 10,
  "ppm_promedio": 17.47,
  "desviacion_estandar": 7.46,
  "ppm_final": 12.16,
  "animales": ["cerdo", "borrego", ...],
  "grupos_semanticos": {
    "domésticos": ["cerdo", "borrego"],
    "aves": ["paloma", "colibrí"]
  },
  "conteo_por_grupo": {
    "domésticos": 2,
    "aves": 2
  }
}
```

### 3. Configuración del Sistema

#### 3.1 Configuración de Audio
```python
AUDIO_CONFIG = {
    "sample_rate": 16000,      # Hz
    "channels": 1,             # Mono
    "format": "wav",           # Formato de salida
    "codec": "pcm_s16le"       # Codec de audio
}
```

#### 3.2 Configuración de IA
```python
AI_CONFIG = {
    "model": "llama3:8b",      # Modelo de Ollama
    "ollama_url": "http://localhost:11434",
    "max_tokens": 2048,        # Máximo tokens de respuesta
    "temperature": 0.1         # Temperatura de generación
}
```

#### 3.3 Configuración de Whisper
```python
WHISPER_CONFIG = {
    "model": "base",           # Tamaño del modelo
    "language": "es",          # Idioma
    "task": "transcribe"       # Tarea
}
```

### 4. Métricas de Fluidez

#### 4.1 Cálculo de PPM (Palabras por Minuto)
```python
def calcular_ppm(tiempo_total_segundos, total_palabras):
    minutos = tiempo_total_segundos / 60
    return total_palabras / minutos if minutos > 0 else 0
```

#### 4.2 Fluidez Acumulada
```python
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
```

### 5. Análisis Estadístico

#### 5.1 Pruebas Utilizadas
- **Mann-Whitney U**: Comparación entre grupos
- **Nivel de significancia**: α = 0.05
- **Corrección**: Bonferroni para múltiples comparaciones

#### 5.2 Variables Analizadas
1. **PPM Promedio**: Fluidez general
2. **PPM Final**: Fluidez al final de la prueba
3. **Desviación Estándar**: Variabilidad en la fluidez
4. **Total de Palabras**: Productividad verbal
5. **Tiempo de Inicio/Final**: Duración de la prueba

### 6. Interfaz de Usuario

#### 6.1 GUI Principal
- **Tecnología**: Tkinter
- **Funcionalidades**:
  - Selección de archivos individuales
  - Procesamiento por lotes
  - Ejecución paso a paso
  - Log en tiempo real

#### 6.2 Flujo de Usuario
1. Seleccionar archivo o carpeta
2. Ejecutar procesamiento completo
3. Revisar resultados en directorio de salida
4. Analizar gráficas y métricas

### 7. Dependencias Externas

#### 7.1 Ollama
- **Propósito**: Ejecución local de modelos de IA
- **Modelo**: llama3:8b
- **Instalación**: `curl -fsSL https://ollama.ai/install.sh | sh`
- **Descarga**: `ollama pull llama3:8b`

#### 7.2 FFmpeg
- **Propósito**: Conversión de video/audio
- **Instalación**: `sudo apt install ffmpeg` (Ubuntu/Debian)

#### 7.3 Pyannote.audio
- **Propósito**: Diarización de hablantes
- **Modelo**: pyannote/speaker-diarization@2.1
- **Autenticación**: Token de Hugging Face requerido

### 8. Optimización y Rendimiento

#### 8.1 Optimizaciones Implementadas
- **Procesamiento paralelo**: Múltiples videos simultáneos
- **Caché de modelos**: Reutilización de modelos cargados
- **Compresión de audio**: Reducción de tamaño de archivos
- **Validación de datos**: Verificación de integridad

#### 8.2 Límites del Sistema
- **Tamaño máximo de video**: 500MB
- **Duración máxima**: 10 minutos
- **Número de hablantes**: 1-2
- **Idioma**: Español

### 9. Manejo de Errores

#### 9.1 Tipos de Errores
1. **Errores de archivo**: Archivos corruptos o no encontrados
2. **Errores de audio**: Problemas de conversión o procesamiento
3. **Errores de IA**: Fallos en la comunicación con Ollama
4. **Errores de transcripción**: Whisper no puede transcribir

#### 9.2 Estrategias de Recuperación
- **Reintentos automáticos**: Para errores temporales
- **Logging detallado**: Para diagnóstico
- **Validación de salidas**: Verificación de resultados
- **Fallbacks**: Métodos alternativos cuando es posible

### 10. Seguridad y Privacidad

#### 10.1 Protección de Datos
- **Procesamiento local**: Sin envío a servidores externos
- **Eliminación temporal**: Archivos intermedios se eliminan
- **Anonimización**: Nombres de pacientes en archivos de salida

#### 10.2 Cumplimiento
- **HIPAA**: Compatible con estándares de salud
- **GDPR**: Protección de datos personales
- **Auditoría**: Logs de procesamiento mantenidos

### 11. Mantenimiento y Actualizaciones

#### 11.1 Actualizaciones de Modelos
- **Whisper**: Actualizaciones automáticas via pip
- **Ollama**: `ollama pull llama3:8b` para actualizar
- **Pyannote**: Actualizaciones manuales según necesidad

#### 11.2 Monitoreo
- **Logs de sistema**: Registro de errores y uso
- **Métricas de rendimiento**: Tiempo de procesamiento
- **Calidad de resultados**: Validación de salidas

### 12. Escalabilidad

#### 12.1 Horizontal
- **Procesamiento distribuido**: Múltiples máquinas
- **Cola de trabajos**: Redis/Celery para lotes grandes
- **Almacenamiento**: S3/Google Cloud Storage

#### 12.2 Vertical
- **GPU acceleration**: Para Whisper y Pyannote
- **Memoria**: Optimización para archivos grandes
- **CPU**: Paralelización de tareas

---

*Esta documentación se actualiza regularmente. Última actualización: Diciembre 2024* 