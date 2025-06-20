"""
Archivo de configuración para el proyecto AI Alcohol.

Contiene todas las configuraciones, rutas y parámetros del sistema.
"""

import os
from pathlib import Path

# Rutas base del proyecto
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
RESULTS_DIR = DATA_DIR / "results"
DOCS_DIR = PROJECT_ROOT / "docs"
FIGURES_DIR = DOCS_DIR / "figures"
REPORTS_DIR = DOCS_DIR / "reports"

# Rutas de datos específicos
ASOCIACIONES_PATH = RAW_DATA_DIR / "asociaciones.json"
DATOS_PACIENTES_PATH = RAW_DATA_DIR / "datos_pacientes.sav"
RESULTADOS_PATH = PROCESSED_DATA_DIR

# Configuración de audio
AUDIO_CONFIG = {
    "sample_rate": 16000,
    "channels": 1,
    "format": "wav",
    "codec": "pcm_s16le"
}

# Configuración de IA
AI_CONFIG = {
    "model": "llama3:8b",
    "ollama_url": "http://localhost:11434",
    "max_tokens": 2048,
    "temperature": 0.1
}

# Configuración de Whisper
WHISPER_CONFIG = {
    "model": "base",
    "language": "es",
    "task": "transcribe"
}

# Configuración de diarización
DIARIZATION_CONFIG = {
    "min_speakers": 1,
    "max_speakers": 2,
    "min_duration": 0.5
}

# Configuración de visualización
VISUALIZATION_CONFIG = {
    "figure_size": (10, 6),
    "dpi": 300,
    "style": "seaborn-v0_8",
    "color_palette": "Set2"
}

# Configuración de análisis estadístico
STATISTICAL_CONFIG = {
    "alpha": 0.05,
    "test_type": "mann-whitney",
    "correction": "bonferroni"
}

# Grupos de pacientes
PATIENT_GROUPS = {
    "CONTROL": {
        "description": "Pacientes sin enfermedad hepática",
        "criteria": {"etiologia": "", "phes": 0}
    },
    "CIRROSIS": {
        "description": "Pacientes con cirrosis sin encefalopatía",
        "criteria": {"etiologia": "not_empty", "phes": 0}
    },
    "ENCEFALOPATÍA": {
        "description": "Pacientes con cirrosis y encefalopatía",
        "criteria": {"etiologia": "not_empty", "phes": 1}
    }
}

# Métricas de fluidez
FLUENCY_METRICS = [
    "ppm_promedio",
    "ppm_final", 
    "desviacion_estandar",
    "total_palabras",
    "tiempo_inicio",
    "tiempo_final"
]

# Extensiones de archivo soportadas
SUPPORTED_VIDEO_FORMATS = [".mp4", ".avi", ".mov", ".mkv"]
SUPPORTED_AUDIO_FORMATS = [".mp3", ".wav", ".m4a", ".flac"]

# Configuración de logging
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "ai_alcohol.log"
}

# Crear directorios si no existen
def ensure_directories():
    """Crea todos los directorios necesarios si no existen."""
    directories = [
        DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, RESULTS_DIR,
        DOCS_DIR, FIGURES_DIR, REPORTS_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# Ejecutar al importar el módulo
ensure_directories() 