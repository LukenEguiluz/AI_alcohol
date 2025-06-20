"""
Módulo de procesamiento de audio.

Contiene funciones para:
- Conversión de video a audio
- Preprocesamiento de audio
- Diarización de hablantes
- Transcripción de audio
"""

from .convertir_de_video_a_audio import convertir_de_video_a_audio
from .procesamiento_de_audio import procesamiento_de_audio
from .diarizacion_de_personas import realizar_diarizacion
from .transcripcion_de_audio import transcripcion_de_audio

__all__ = [
    'convertir_de_video_a_audio',
    'procesamiento_de_audio',
    'realizar_diarizacion',
    'transcripcion_de_audio'
] 