# AI Alcohol - Análisis de Fluidez Verbal en Pacientes con Enfermedad Hepática

## 📋 Descripción

Sistema de análisis automatizado de fluidez verbal para evaluar la función cognitiva en pacientes con cirrosis hepática y encefalopatía hepática. El proyecto procesa videos de pruebas de fluidez verbal (nombrado de animales) y extrae métricas clínicamente relevantes utilizando técnicas de procesamiento de audio e inteligencia artificial.

## 🎯 Objetivo

Evaluar las diferencias en fluidez verbal entre tres grupos de pacientes:
- **CONTROL**: Pacientes sin enfermedad hepática
- **CIRROSIS**: Pacientes con cirrosis sin encefalopatía
- **ENCEFALOPATÍA**: Pacientes con cirrosis y encefalopatía hepática

## 🏗️ Arquitectura del Sistema

### Pipeline de Procesamiento (6 pasos)

1. **🎬 Conversión de Video a Audio**
   - Conversión de archivos MP4 a MP3
   - Optimización para procesamiento posterior

2. **🎧 Preprocesamiento de Audio**
   - Filtrado y normalización
   - Preparación para transcripción

3. **🗣️ Diarización**
   - Identificación de diferentes hablantes
   - Segmentación temporal del audio

4. **✍️ Transcripción**
   - Conversión de audio a texto
   - Marcas de tiempo precisas

5. **🦁 Análisis con IA**
   - Detección de animales mencionados
   - Clasificación semántica
   - Identificación de posibles errores de pronunciación

6. **📊 Visualización y Análisis**
   - Cálculo de métricas de fluidez
   - Generación de gráficas
   - Análisis estadístico

## 📊 Métricas Extraídas

- **PPM Promedio**: Palabras por minuto promedio
- **PPM Final**: Fluidez al final de la prueba
- **Desviación Estándar**: Variabilidad en la fluidez
- **Total de Palabras**: Número total de animales mencionados
- **Tiempo de Inicio/Final**: Duración de la prueba
- **Clasificación Semántica**: Agrupación de animales por categorías

## 🚀 Instalación Automática

### Opción 1: Script Automático (Recomendado)

#### Linux/macOS:
```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/AI_alcohol.git
cd AI_alcohol

# Ejecutar script de configuración automática
./setup_environment.sh
```

#### Windows:
```powershell
# Clonar el repositorio
git clone https://github.com/tu-usuario/AI_alcohol.git
cd AI_alcohol

# Ejecutar script de configuración automática
.\setup_environment.ps1
```

### Opción 2: Instalación Manual

#### Requisitos Previos

```bash
# Instalar Ollama (para análisis con IA)
curl -fsSL https://ollama.ai/install.sh | sh

# Descargar modelo de IA
ollama pull llama3:8b
```

#### Instalación del Proyecto

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/AI_alcohol.git
cd AI_alcohol

# Crear entorno virtual
python3 -m venv env

# Activar entorno virtual
source env/bin/activate  # Linux/macOS
# o
.\env\Scripts\Activate.ps1  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

## 💻 Uso

### Activación del Entorno

#### Linux/macOS:
```bash
# Opción 1: Activación directa
source env/bin/activate

# Opción 2: Script de activación (creado automáticamente)
./activate_env.sh
```

#### Windows:
```powershell
# Opción 1: Activación directa
.\env\Scripts\Activate.ps1

# Opción 2: Script de activación (creado automáticamente)
.\activate_env.ps1
```

### Interfaz Gráfica

```bash
# Iniciar Ollama en una terminal separada
ollama serve

# En otra terminal, ejecutar la aplicación
python main.py
```

### Procesamiento Individual

```python
from src.main import AIAlcoholProcessor

processor = AIAlcoholProcessor()
processor.process_video("ruta/al/video.mp4")
```

### Procesamiento por Lotes

```python
processor.process_folder("carpeta/con/videos/")
```

## 📁 Estructura del Proyecto

```
AI_alcohol/
├── src/                    # Código fuente
│   ├── audio_processing/   # Procesamiento de audio
│   ├── ai_analysis/        # Análisis con IA
│   ├── visualization/      # Visualización y gráficas
│   └── utils/             # Utilidades
├── data/                   # Datos
│   ├── raw/               # Datos originales
│   ├── processed/         # Datos procesados
│   └── results/           # Resultados finales
├── docs/                   # Documentación
│   ├── figures/           # Figuras y gráficas
│   └── reports/           # Reportes
├── tests/                  # Pruebas unitarias
├── examples/               # Ejemplos de uso
├── setup_environment.sh    # Script de configuración (Linux/macOS)
├── setup_environment.ps1   # Script de configuración (Windows)
└── main.py                # Punto de entrada principal
```

## 🔧 Configuración Avanzada

### Detección Automática de GPU

Los scripts de configuración detectan automáticamente:
- **GPU NVIDIA**: Instala CUDA y PyTorch con soporte GPU
- **CPU**: Instala PyTorch optimizado para CPU
- **Sistema operativo**: Adapta la instalación según la plataforma

### Variables de Entorno

```bash
# Configuración de CUDA (automática si se detecta GPU NVIDIA)
export CUDA_VISIBLE_DEVICES=0

# Configuración de Ollama
export OLLAMA_HOST=localhost:11434
```

### Configuración Manual

Si necesitas configurar manualmente, edita `config.py`:

```python
# Configuración de IA
AI_CONFIG = {
    "model": "llama3:8b",
    "ollama_url": "http://localhost:11434",
    "max_tokens": 2048,
    "temperature": 0.1
}

# Configuración de audio
AUDIO_CONFIG = {
    "sample_rate": 16000,
    "channels": 1,
    "format": "wav"
}
```

## 📈 Resultados Principales

### Análisis Estadístico (Mann-Whitney U)

| Métrica | Control vs Cirrosis | Control vs Encefalopatía | Cirrosis vs Encefalopatía |
|---------|-------------------|-------------------------|--------------------------|
| Total Palabras | p=0.0018 | p<0.0001 | p=0.0012 |
| PPM Final | p=0.0706 | p<0.0001 | p=0.0011 |
| Tiempo Final | p=0.4259 | p=0.0125 | p=0.1638 |

### Hallazgos Clínicos

- Los pacientes con **encefalopatía hepática** muestran menor fluidez verbal
- Los **controles** tienen mejor rendimiento en la prueba
- La **cirrosis** sin encefalopatía muestra rendimiento intermedio
- Las diferencias son más marcadas en el total de palabras y PPM final

## 🔬 Metodología

### Población de Estudio
- **103 pacientes** procesados
- **23 controles**
- **38 pacientes con cirrosis**
- **16 pacientes con encefalopatía**

### Análisis Técnico
- Procesamiento de audio con Whisper
- Diarización con Pyannote
- Análisis de IA con Ollama (llama3:8b)
- Análisis estadístico con Python

## 🛠️ Solución de Problemas

### Problemas Comunes

#### 1. Ollama no está corriendo
```bash
# Iniciar Ollama
ollama serve

# Verificar que esté funcionando
curl http://localhost:11434
```

#### 2. Error de CUDA
```bash
# Verificar instalación de CUDA
nvidia-smi

# Reinstalar PyTorch con CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

#### 3. Error de FFmpeg
```bash
# Verificar instalación
ffmpeg -version

# Reinstalar si es necesario
sudo apt install ffmpeg  # Ubuntu/Debian
brew install ffmpeg      # macOS
```

#### 4. Problemas de permisos
```bash
# Dar permisos de ejecución a los scripts
chmod +x setup_environment.sh
chmod +x activate_env.sh
```

### Logs y Debugging

```bash
# Ver logs detallados
python main.py --verbose

# Verificar configuración
python -c "import config; print(config.AI_CONFIG)"
```

## 📚 Referencias

- [Whisper: Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356)
- [Pyannote: Neural Building Blocks for Speaker Diarization](https://arxiv.org/abs/1911.01255)
- [Ollama: Local Large Language Models](https://ollama.ai/)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autores

- **Luken Eguiluz** - *Desarrollo inicial* - [@LukenEguiluz](https://github.com/LukenEguiluz)

## 🙏 Agradecimientos

- Equipo médico por la validación clínica
- Pacientes por su participación
- Comunidad de código abierto por las herramientas utilizadas

## 📞 Contacto

- Email: luken.eguiluz@gmail.com
- GitHub: [@LukenEguiluz](https://github.com/LukenEguiluz)
- LinkedIn: [Luken Eguiluz](https://linkedin.com/in/luken-eguiluz)

## ⚠️ Configuración de Hugging Face Token

Para usar la diarización de hablantes, necesitas un token de acceso de Hugging Face. 

1. Crea un archivo `.env` en la raíz del proyecto:

```bash
cp .env.example .env
```

2. Edita el archivo `.env` y pon tu token de Hugging Face:

```
HUGGINGFACE_TOKEN=tu_token_aqui
```

Puedes obtener tu token en: https://huggingface.co/settings/tokens

---

**Nota**: Este proyecto es para investigación médica. Los resultados deben ser interpretados por profesionales de la salud. 
