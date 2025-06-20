# 🧠 AI Alcohol: Análisis Automatizado de Fluidez Verbal con IA

## 🎯 ¿Qué es AI Alcohol?

**AI Alcohol** es un sistema revolucionario que utiliza inteligencia artificial para analizar automáticamente la fluidez verbal en pacientes con enfermedad hepática. El proyecto procesa videos de pruebas de fluidez verbal (nombrado de animales) y extrae métricas clínicamente relevantes para evaluar la función cognitiva.

## 🔬 Contexto Clínico

La **encefalopatía hepática** es una complicación grave de la cirrosis que afecta la función cerebral. Los pacientes experimentan deterioro cognitivo que se puede detectar tempranamente mediante pruebas de fluidez verbal. Este proyecto automatiza este proceso de evaluación.

### Grupos de Estudio:
- **CONTROL**: 23 pacientes sin enfermedad hepática
- **CIRROSIS**: 38 pacientes con cirrosis sin encefalopatía  
- **ENCEFALOPATÍA**: 16 pacientes con cirrosis y encefalopatía hepática

## 🏗️ Arquitectura Técnica

### Pipeline de 6 Pasos:

1. **🎬 Conversión Video → Audio**
   - MP4 → MP3 con FFmpeg
   - Optimización para procesamiento

2. **🎧 Preprocesamiento de Audio**
   - Filtrado y normalización
   - Preparación para Whisper

3. **🗣️ Diarización con Pyannote**
   - Identificación de hablantes
   - Segmentación temporal

4. **✍️ Transcripción con Whisper**
   - Audio → Texto con marcas de tiempo
   - Alta precisión en español

5. **🦁 Análisis con IA (Ollama + llama3:8b)**
   - Detección automática de animales
   - Clasificación semántica
   - Corrección de errores de pronunciación

6. **📊 Visualización y Análisis**
   - Cálculo de métricas de fluidez
   - Generación de gráficas automáticas
   - Análisis estadístico (Mann-Whitney U)

## 📈 Resultados Clínicos Significativos

### Análisis Estadístico (p-valores):

| Métrica | Control vs Cirrosis | Control vs Encefalopatía | Cirrosis vs Encefalopatía |
|---------|-------------------|-------------------------|--------------------------|
| **Total Palabras** | p=0.0018 | **p<0.0001** | p=0.0012 |
| **PPM Final** | p=0.0706 | **p<0.0001** | p=0.0011 |
| **Tiempo Final** | p=0.4259 | p=0.0125 | p=0.1638 |

### 🎯 Hallazgos Clave:
- **Encefalopatía hepática** → Menor fluidez verbal significativa
- **Controles** → Mejor rendimiento en todas las métricas
- **Cirrosis sin encefalopatía** → Rendimiento intermedio
- Diferencias más marcadas en **total de palabras** y **PPM final**

## 🚀 Características Técnicas Destacadas

### ✨ Automatización Completa
- **Interfaz gráfica** intuitiva con Tkinter
- **Procesamiento por lotes** de múltiples videos
- **Scripts de configuración automática** para Linux/macOS/Windows

### 🧠 IA Local y Privada
- **Ollama** con modelo **llama3:8b** local
- **Sin dependencia de APIs externas**
- **Procesamiento offline** para confidencialidad médica

### 📊 Métricas Clínicas Precisas
- **PPM Promedio**: Palabras por minuto
- **PPM Final**: Fluidez al final de la prueba
- **Desviación Estándar**: Variabilidad en la fluidez
- **Clasificación Semántica**: Agrupación automática de animales

### 🔧 Detección Automática de Hardware
- **GPU NVIDIA**: Instalación automática de CUDA
- **CPU**: Optimización automática para procesamiento
- **Multiplataforma**: Linux, macOS, Windows

## 💻 Instalación Súper Simple

### ⚡ Configuración en 5 minutos:

```bash
# 1. Clonar
git clone https://github.com/LukenEguiluz/AI_alcohol.git
cd AI_alcohol

# 2. Configuración automática
./setup_environment.sh  # Linux/macOS
# o
.\setup_environment.ps1  # Windows

# 3. Activar entorno
./activate_env.sh

# 4. Iniciar Ollama
ollama serve

# 5. ¡Listo!
python main.py
```

## 🎬 Uso Extremadamente Simple

### Procesar un video:
1. Abrir aplicación: `python main.py`
2. Seleccionar archivo MP4
3. Clic en "🔁 Ejecutar todo"
4. ¡Resultados automáticos!

### Procesar múltiples videos:
1. Clic en "📁 Procesar Carpeta Completa"
2. Seleccionar carpeta con videos
3. ¡Procesamiento automático de todos!

## 📊 Salidas Automáticas

Para cada video procesado:
- **Gráfica de fluidez**: `fluidez_[video].png`
- **Métricas JSON**: `resumen_fluidez_[video].json`
- **Excel con estadísticas**: `fluidez_[video].xlsx`
- **Transcripción alineada**: `aligned_transcription.json`

## 🔬 Impacto Clínico

### Beneficios para la Medicina:
- **Detección temprana** de encefalopatía hepática
- **Evaluación objetiva** y reproducible
- **Ahorro de tiempo** para médicos
- **Análisis estandarizado** entre centros

### Aplicaciones Futuras:
- **Seguimiento longitudinal** de pacientes
- **Evaluación de tratamientos**
- **Detección de recaídas**
- **Investigación clínica**

## 🛠️ Stack Tecnológico

### Core:
- **Python 3.8+** - Lenguaje principal
- **PyTorch** - Deep Learning (GPU/CPU)
- **Whisper** - Transcripción de audio
- **Pyannote** - Diarización de hablantes

### IA y ML:
- **Ollama** - Framework de IA local
- **llama3:8b** - Modelo de lenguaje
- **NumPy/Pandas** - Análisis de datos
- **SciPy** - Estadísticas

### Audio/Video:
- **FFmpeg** - Procesamiento multimedia
- **Librosa** - Análisis de audio
- **SoundFile** - Manipulación de audio

### Visualización:
- **Matplotlib/Seaborn** - Gráficas
- **Tkinter** - Interfaz gráfica
- **OpenPyXL** - Exportación Excel

## 🎯 Casos de Uso

### Para Médicos:
- **Evaluación rutinaria** de pacientes con cirrosis
- **Detección temprana** de deterioro cognitivo
- **Seguimiento** de respuesta al tratamiento

### Para Investigadores:
- **Estudios clínicos** con análisis automatizado
- **Análisis de cohortes** grandes
- **Investigación en encefalopatía hepática**

### Para Hospitales:
- **Screening masivo** de pacientes
- **Estandarización** de evaluaciones
- **Optimización** de recursos médicos

## 🔒 Privacidad y Seguridad

- **Procesamiento 100% local** - Sin envío de datos
- **IA local** - Sin dependencia de servicios externos
- **Cumplimiento HIPAA** - Datos médicos protegidos
- **Código abierto** - Transparencia total

## 📈 Métricas del Proyecto

- **103 pacientes** procesados exitosamente
- **6 pasos** automatizados por video
- **5 minutos** de configuración inicial
- **100%** procesamiento local
- **3 grupos** clínicos analizados

## 🚀 Próximos Pasos

- [ ] **API REST** para integración hospitalaria
- [ ] **Dashboard web** para visualización
- [ ] **Móvil** para evaluaciones remotas
- [ ] **Más idiomas** (inglés, francés, etc.)
- [ ] **Otros tipos** de pruebas cognitivas

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Este proyecto puede salvar vidas:

1. **Fork** el proyecto
2. **Crea** una rama para tu feature
3. **Commit** tus cambios
4. **Push** y abre un Pull Request

## 📞 Contacto

- **GitHub**: [@LukenEguiluz](https://github.com/LukenEguiluz)
- **Email**: luken.eguiluz@gmail.com
- **LinkedIn**: [Luken Eguiluz](https://linkedin.com/in/luken-eguiluz)

## 📄 Licencia

**MIT License** - Libre para uso académico y comercial

---

## 🎉 ¿Por qué este proyecto es especial?

### 🔬 **Innovación Médica**
Primer sistema automatizado para evaluación de fluidez verbal en encefalopatía hepática

### 🧠 **IA Local**
Privacidad total con procesamiento offline - crucial para datos médicos

### ⚡ **Simplicidad**
De 0 a procesando videos en 5 minutos

### 📊 **Precisión Clínica**
Resultados estadísticamente significativos validados médicamente

### 🌍 **Impacto Global**
Potencial para mejorar la vida de millones de pacientes con cirrosis

---

**#AIMedicine #Hepatology #SpeechAnalysis #MachineLearning #OpenSource #MedicalAI #ClinicalResearch #LiverDisease #CognitiveAssessment #HealthcareTech**

---

*¿Te gusta este proyecto? ¡Dale una ⭐ en GitHub y compártelo!* 