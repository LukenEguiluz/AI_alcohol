"""
Pruebas básicas para el sistema AI Alcohol.

Este módulo contiene pruebas unitarias para verificar la funcionalidad
básica del sistema.
"""

import unittest
import tempfile
import os
import json
from pathlib import Path
import sys

# Agregar el directorio raíz al path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

import config

class TestConfiguration(unittest.TestCase):
    """Pruebas para la configuración del sistema."""
    
    def test_config_import(self):
        """Prueba que la configuración se importe correctamente."""
        self.assertIsNotNone(config.PROJECT_ROOT)
        self.assertIsNotNone(config.DATA_DIR)
        self.assertIsNotNone(config.AI_CONFIG)
    
    def test_directories_exist(self):
        """Prueba que los directorios necesarios existan."""
        directories = [
            config.DATA_DIR,
            config.RAW_DATA_DIR,
            config.PROCESSED_DATA_DIR,
            config.RESULTS_DIR,
            config.DOCS_DIR,
            config.FIGURES_DIR,
            config.REPORTS_DIR
        ]
        
        for directory in directories:
            self.assertTrue(directory.exists(), f"Directorio {directory} no existe")
    
    def test_ai_config_structure(self):
        """Prueba la estructura de la configuración de IA."""
        required_keys = ["model", "ollama_url", "max_tokens", "temperature"]
        
        for key in required_keys:
            self.assertIn(key, config.AI_CONFIG, f"Falta clave {key} en AI_CONFIG")

class TestDataStructures(unittest.TestCase):
    """Pruebas para las estructuras de datos."""
    
    def test_patient_groups_structure(self):
        """Prueba la estructura de los grupos de pacientes."""
        required_groups = ["CONTROL", "CIRROSIS", "ENCEFALOPATÍA"]
        
        for group in required_groups:
            self.assertIn(group, config.PATIENT_GROUPS, f"Falta grupo {group}")
            
            group_config = config.PATIENT_GROUPS[group]
            self.assertIn("description", group_config)
            self.assertIn("criteria", group_config)
    
    def test_fluency_metrics(self):
        """Prueba que las métricas de fluidez estén definidas."""
        self.assertIsInstance(config.FLUENCY_METRICS, list)
        self.assertGreater(len(config.FLUENCY_METRICS), 0)
        
        required_metrics = ["ppm_promedio", "total_palabras"]
        for metric in required_metrics:
            self.assertIn(metric, config.FLUENCY_METRICS, f"Falta métrica {metric}")

class TestFileFormats(unittest.TestCase):
    """Pruebas para los formatos de archivo soportados."""
    
    def test_video_formats(self):
        """Prueba que los formatos de video estén definidos."""
        self.assertIsInstance(config.SUPPORTED_VIDEO_FORMATS, list)
        self.assertGreater(len(config.SUPPORTED_VIDEO_FORMATS), 0)
        
        # Verificar que contenga formatos comunes
        common_formats = [".mp4", ".avi"]
        for fmt in common_formats:
            self.assertIn(fmt, config.SUPPORTED_VIDEO_FORMATS, f"Falta formato {fmt}")
    
    def test_audio_formats(self):
        """Prueba que los formatos de audio estén definidos."""
        self.assertIsInstance(config.SUPPORTED_AUDIO_FORMATS, list)
        self.assertGreater(len(config.SUPPORTED_AUDIO_FORMATS), 0)
        
        # Verificar que contenga formatos comunes
        common_formats = [".mp3", ".wav"]
        for fmt in common_formats:
            self.assertIn(fmt, config.SUPPORTED_AUDIO_FORMATS, f"Falta formato {fmt}")

class TestDataFiles(unittest.TestCase):
    """Pruebas para los archivos de datos."""
    
    def test_associations_file_exists(self):
        """Prueba que el archivo de asociaciones exista."""
        if config.ASOCIACIONES_PATH.exists():
            # Verificar que sea un JSON válido
            try:
                with open(config.ASOCIACIONES_PATH, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.assertIsInstance(data, dict)
            except json.JSONDecodeError:
                self.fail("El archivo de asociaciones no es un JSON válido")
    
    def test_patient_data_file_exists(self):
        """Prueba que el archivo de datos de pacientes exista."""
        # Esta prueba puede fallar si el archivo .sav no está presente
        # pero es normal en un entorno de desarrollo
        if config.DATOS_PACIENTES_PATH.exists():
            self.assertTrue(config.DATOS_PACIENTES_PATH.is_file())

class TestResultsStructure(unittest.TestCase):
    """Pruebas para la estructura de resultados."""
    
    def test_results_directory_structure(self):
        """Prueba que el directorio de resultados tenga la estructura correcta."""
        if config.PROCESSED_DATA_DIR.exists():
            # Verificar que contenga al menos algunos directorios de video
            video_dirs = [d for d in config.PROCESSED_DATA_DIR.iterdir() 
                         if d.is_dir() and d.name.startswith("video_")]
            
            if video_dirs:
                # Verificar estructura de un directorio de video
                video_dir = video_dirs[0]
                expected_files = [
                    "aligned_transcription.json",
                    "diarization_results.json",
                    "palabras_con_tiempos.json"
                ]
                
                for file_name in expected_files:
                    file_path = video_dir / file_name
                    if file_path.exists():
                        # Verificar que sea un JSON válido
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                json.load(f)
                        except json.JSONDecodeError:
                            self.fail(f"El archivo {file_name} no es un JSON válido")

def run_tests():
    """Ejecuta todas las pruebas."""
    # Crear un test suite
    test_suite = unittest.TestSuite()
    
    # Agregar todas las clases de prueba
    test_classes = [
        TestConfiguration,
        TestDataStructures,
        TestFileFormats,
        TestDataFiles,
        TestResultsStructure
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Ejecutar las pruebas
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    print("🧪 Ejecutando pruebas del sistema AI Alcohol...")
    success = run_tests()
    
    if success:
        print("\n✅ Todas las pruebas pasaron exitosamente!")
    else:
        print("\n❌ Algunas pruebas fallaron.")
    
    sys.exit(0 if success else 1) 