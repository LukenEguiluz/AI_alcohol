# 🚀 Guía de Inicio Rápido - AI Alcohol

## ⚡ Configuración en 5 minutos

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/AI_alcohol.git
cd AI_alcohol
```

### 2. Ejecutar configuración automática

#### Linux/macOS:
```bash
./setup_environment.sh
```

#### Windows:
```powershell
.\setup_environment.ps1
```

### 3. Activar el entorno
```bash
# Linux/macOS
./activate_env.sh

# Windows
.\activate_env.ps1
```

### 4. Iniciar Ollama
```bash
# En una nueva terminal
ollama serve
```

### 5. Ejecutar la aplicación
```bash
python main.py
```

## 🎯 ¿Qué hace el script automático?

✅ **Detecta tu sistema operativo** (Linux, macOS, Windows)  
✅ **Verifica Python 3.8+** e instala si es necesario  
✅ **Detecta GPU NVIDIA** automáticamente  
✅ **Instala CUDA** si hay GPU NVIDIA disponible  
✅ **Crea entorno virtual** con todas las dependencias  
✅ **Instala PyTorch** (GPU o CPU según disponibilidad)  
✅ **Instala Ollama** y descarga el modelo llama3:8b  
✅ **Instala FFmpeg** para procesamiento de audio/video  
✅ **Crea scripts de activación** personalizados  

## 🔧 Configuración Manual (Si el script falla)

### Requisitos mínimos:
- Python 3.8 o superior
- 8GB RAM mínimo (16GB recomendado)
- 10GB espacio libre en disco
- GPU NVIDIA (opcional, para aceleración)

### Instalación paso a paso:

```bash
# 1. Crear entorno virtual
python3 -m venv env

# 2. Activar entorno
source env/bin/activate  # Linux/macOS
# o
.\env\Scripts\Activate.ps1  # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Instalar Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 5. Descargar modelo
ollama pull llama3:8b
```

## 🎬 Primer uso

### Procesar un video individual:
1. Abre la aplicación: `python main.py`
2. Haz clic en "Seleccionar Archivo"
3. Elige un video MP4
4. Haz clic en "🔁 Ejecutar todo"
5. Espera a que termine el procesamiento
6. Revisa los resultados en la carpeta `data/results/`

### Procesar múltiples videos:
1. Haz clic en "📁 Procesar Carpeta Completa"
2. Selecciona la carpeta con los videos
3. El script procesará todos automáticamente

## 📊 Ver resultados

Los resultados se guardan en:
- **Gráficas**: `data/results/[video_name]/fluidez_[video_name].png`
- **Métricas**: `data/results/[video_name]/resumen_fluidez_[video_name].json`
- **Estadísticas**: `data/results/[video_name]/fluidez_[video_name].xlsx`

## 🆘 Solución rápida de problemas

### Error: "Ollama no está corriendo"
```bash
# Terminal 1: Iniciar Ollama
ollama serve

# Terminal 2: Ejecutar aplicación
python main.py
```

### Error: "CUDA no disponible"
```bash
# Verificar GPU
nvidia-smi

# Si no hay GPU, usar CPU automáticamente
# El script ya detecta esto automáticamente
```

### Error: "FFmpeg no encontrado"
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
choco install ffmpeg
```

### Error: "Permisos denegados"
```bash
# Dar permisos de ejecución
chmod +x setup_environment.sh
chmod +x activate_env.sh
```

## 📈 Métricas que obtienes

Para cada video procesado:
- **PPM Promedio**: Palabras por minuto
- **PPM Final**: Fluidez al final de la prueba
- **Desviación Estándar**: Variabilidad en la fluidez
- **Total de Palabras**: Número de animales mencionados
- **Tiempo Total**: Duración de la prueba
- **Clasificación Semántica**: Agrupación de animales

## 🎯 Ejemplo de uso completo

```bash
# 1. Configurar todo automáticamente
./setup_environment.sh

# 2. Activar entorno
./activate_env.sh

# 3. Iniciar Ollama (nueva terminal)
ollama serve

# 4. Procesar video
python main.py
# - Seleccionar archivo: video_paciente.mp4
# - Ejecutar todo
# - Esperar procesamiento

# 5. Ver resultados
ls data/results/video_paciente/
# - fluidez_video_paciente.png (gráfica)
# - resumen_fluidez_video_paciente.json (métricas)
# - fluidez_video_paciente.xlsx (Excel)
```

## 🔍 Verificar instalación

```bash
# Verificar Python
python --version

# Verificar PyTorch
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import torch; print(f'CUDA disponible: {torch.cuda.is_available()}')"

# Verificar Ollama
ollama list

# Verificar FFmpeg
ffmpeg -version
```

## 📞 ¿Necesitas ayuda?

1. **Revisa los logs** en la terminal
2. **Verifica la documentación** en `docs/`
3. **Ejecuta las pruebas**: `python tests/test_basic_functionality.py`
4. **Abre un issue** en GitHub

---

**¡Listo! Ya puedes empezar a analizar fluidez verbal con IA.** 🎉 