#!/bin/bash

# AI Alcohol - Setup Environment Script
# Este script detecta el sistema operativo, crea un entorno virtual
# e instala CUDA si detecta una GPU NVIDIA

set -e  # Exit on any error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con colores
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${PURPLE}================================${NC}"
    echo -e "${PURPLE}  AI Alcohol - Setup Environment${NC}"
    echo -e "${PURPLE}================================${NC}"
}

# Función para detectar el sistema operativo
detect_os() {
    print_status "Detectando sistema operativo..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            OS=$NAME
            VER=$VERSION_ID
        else
            OS=$(uname -s)
            VER=$(uname -r)
        fi
        print_success "Sistema detectado: $OS $VER"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macOS"
        VER=$(sw_vers -productVersion)
        print_success "Sistema detectado: $OS $VER"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        OS="Windows"
        VER=$(uname -r)
        print_success "Sistema detectado: $OS $VER"
    else
        print_error "Sistema operativo no soportado: $OSTYPE"
        exit 1
    fi
}

# Función para verificar si Python está instalado
check_python() {
    print_status "Verificando instalación de Python..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python encontrado: $PYTHON_VERSION"
        
        # Verificar versión mínima (3.8)
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
        
        if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
            print_success "Versión de Python compatible (>= 3.8)"
        else
            print_error "Se requiere Python 3.8 o superior. Versión actual: $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python 3 no está instalado"
        print_status "Instalando Python 3..."
        install_python
    fi
}

# Función para instalar Python según el sistema operativo
install_python() {
    case $OS in
        "Ubuntu"|"Debian GNU/Linux")
            print_status "Instalando Python 3 en Ubuntu/Debian..."
            sudo apt update
            sudo apt install -y python3 python3-pip python3-venv
            ;;
        "CentOS Linux"|"Red Hat Enterprise Linux")
            print_status "Instalando Python 3 en CentOS/RHEL..."
            sudo yum install -y python3 python3-pip
            ;;
        "Fedora")
            print_status "Instalando Python 3 en Fedora..."
            sudo dnf install -y python3 python3-pip
            ;;
        "macOS")
            print_status "Instalando Python 3 en macOS..."
            if command -v brew &> /dev/null; then
                brew install python3
            else
                print_error "Homebrew no está instalado. Instale Homebrew primero:"
                print_status "/bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
                exit 1
            fi
            ;;
        *)
            print_error "No se puede instalar Python automáticamente en $OS"
            print_status "Por favor, instale Python 3.8+ manualmente"
            exit 1
            ;;
    esac
}

# Función para detectar GPU NVIDIA
detect_nvidia_gpu() {
    print_status "Detectando GPU NVIDIA..."
    
    if command -v nvidia-smi &> /dev/null; then
        GPU_INFO=$(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits | head -1)
        GPU_NAME=$(echo $GPU_INFO | cut -d',' -f1)
        GPU_MEMORY=$(echo $GPU_INFO | cut -d',' -f2)
        
        print_success "GPU NVIDIA detectada: $GPU_NAME ($GPU_MEMORY MB)"
        NVIDIA_GPU=true
    else
        print_warning "No se detectó GPU NVIDIA o nvidia-smi no está disponible"
        NVIDIA_GPU=false
    fi
}

# Función para instalar CUDA
install_cuda() {
    if [ "$NVIDIA_GPU" = true ]; then
        print_status "Instalando CUDA para GPU NVIDIA..."
        
        case $OS in
            "Ubuntu"|"Debian GNU/Linux")
                install_cuda_ubuntu
                ;;
            "CentOS Linux"|"Red Hat Enterprise Linux"|"Fedora")
                install_cuda_centos
                ;;
            "macOS")
                print_warning "CUDA no está disponible en macOS. Se usará CPU."
                ;;
            *)
                print_warning "Instalación automática de CUDA no soportada en $OS"
                print_status "Instale CUDA manualmente desde: https://developer.nvidia.com/cuda-downloads"
                ;;
        esac
    fi
}

# Función para instalar CUDA en Ubuntu/Debian
install_cuda_ubuntu() {
    print_status "Instalando CUDA en Ubuntu/Debian..."
    
    # Agregar repositorio NVIDIA
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
    sudo dpkg -i cuda-keyring_1.0-1_all.deb
    sudo apt-get update
    
    # Instalar CUDA toolkit
    sudo apt-get install -y cuda-toolkit-12-0
    
    # Configurar variables de entorno
    echo 'export PATH=/usr/local/cuda-12.0/bin:$PATH' >> ~/.bashrc
    echo 'export LD_LIBRARY_PATH=/usr/local/cuda-12.0/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
    
    # Limpiar archivo descargado
    rm cuda-keyring_1.0-1_all.deb
    
    print_success "CUDA instalado correctamente"
}

# Función para instalar CUDA en CentOS/RHEL/Fedora
install_cuda_centos() {
    print_status "Instalando CUDA en CentOS/RHEL/Fedora..."
    
    # Agregar repositorio NVIDIA
    sudo dnf config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/rhel8/x86_64/cuda-rhel8.repo
    sudo dnf clean all
    sudo dnf -y module install nvidia-driver:latest-dkms
    sudo dnf -y install cuda-toolkit
    
    # Configurar variables de entorno
    echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
    echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
    
    print_success "CUDA instalado correctamente"
}

# Función para crear entorno virtual
create_virtual_environment() {
    print_status "Creando entorno virtual..."
    
    if [ -d "env" ]; then
        print_warning "El directorio 'env' ya existe"
        read -p "¿Desea eliminarlo y crear uno nuevo? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf env
        else
            print_status "Usando entorno virtual existente"
            return
        fi
    fi
    
    python3 -m venv env
    print_success "Entorno virtual creado en 'env'"
}

# Función para activar entorno virtual e instalar dependencias
install_dependencies() {
    print_status "Activando entorno virtual e instalando dependencias..."
    
    # Activar entorno virtual
    source env/bin/activate
    
    # Actualizar pip
    pip install --upgrade pip
    
    # Instalar dependencias base
    print_status "Instalando dependencias base..."
    pip install -r requirements.txt
    
    # Instalar dependencias específicas para GPU si está disponible
    if [ "$NVIDIA_GPU" = true ]; then
        print_status "Instalando dependencias para GPU NVIDIA..."
        
        # Instalar PyTorch con soporte CUDA
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
        
        # Instalar otras dependencias optimizadas para GPU
        pip install cupy-cuda11x  # Para operaciones GPU con NumPy
    else
        print_status "Instalando PyTorch para CPU..."
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
    fi
    
    print_success "Dependencias instaladas correctamente"
}

# Función para verificar instalación de Ollama
check_ollama() {
    print_status "Verificando instalación de Ollama..."
    
    if command -v ollama &> /dev/null; then
        print_success "Ollama ya está instalado"
        
        # Verificar si el modelo está descargado
        if ollama list | grep -q "llama3:8b"; then
            print_success "Modelo llama3:8b ya está descargado"
        else
            print_status "Descargando modelo llama3:8b..."
            ollama pull llama3:8b
        fi
    else
        print_status "Instalando Ollama..."
        curl -fsSL https://ollama.ai/install.sh | sh
        
        # Descargar modelo después de la instalación
        print_status "Descargando modelo llama3:8b..."
        ollama pull llama3:8b
    fi
}

# Función para verificar FFmpeg
check_ffmpeg() {
    print_status "Verificando instalación de FFmpeg..."
    
    if command -v ffmpeg &> /dev/null; then
        print_success "FFmpeg ya está instalado"
    else
        print_status "Instalando FFmpeg..."
        case $OS in
            "Ubuntu"|"Debian GNU/Linux")
                sudo apt install -y ffmpeg
                ;;
            "CentOS Linux"|"Red Hat Enterprise Linux"|"Fedora")
                sudo dnf install -y ffmpeg
                ;;
            "macOS")
                if command -v brew &> /dev/null; then
                    brew install ffmpeg
                else
                    print_error "Homebrew no está instalado. Instale FFmpeg manualmente."
                fi
                ;;
            *)
                print_warning "Instale FFmpeg manualmente para su sistema: $OS"
                ;;
        esac
    fi
}

# Función para crear script de activación
create_activation_script() {
    print_status "Creando script de activación..."
    
    cat > activate_env.sh << 'EOF'
#!/bin/bash
# Script para activar el entorno virtual de AI Alcohol

echo "Activando entorno virtual de AI Alcohol..."
source env/bin/activate

# Configurar variables de entorno para CUDA si está disponible
if command -v nvidia-smi &> /dev/null; then
    export CUDA_VISIBLE_DEVICES=0
    echo "GPU NVIDIA detectada - CUDA habilitado"
else
    echo "Usando CPU para procesamiento"
fi

# Verificar que Ollama esté corriendo
if ! curl -s http://localhost:11434 > /dev/null; then
    echo "⚠️  Ollama no está corriendo. Ejecute 'ollama serve' en otra terminal"
fi

echo "Entorno activado. Ejecute 'python main.py' para iniciar la aplicación."
EOF

    chmod +x activate_env.sh
    print_success "Script de activación creado: activate_env.sh"
}

# Función para mostrar resumen final
show_summary() {
    print_header
    print_success "Configuración completada exitosamente!"
    echo
    echo -e "${CYAN}Resumen de la instalación:${NC}"
    echo -e "  • Sistema operativo: $OS $VER"
    echo -e "  • Python: $(python3 --version)"
    echo -e "  • Entorno virtual: env/"
    echo -e "  • GPU NVIDIA: $([ "$NVIDIA_GPU" = true ] && echo "Sí" || echo "No")"
    echo -e "  • CUDA: $([ "$NVIDIA_GPU" = true ] && echo "Instalado" || echo "No requerido")"
    echo -e "  • Ollama: Instalado"
    echo -e "  • FFmpeg: Instalado"
    echo
    echo -e "${CYAN}Próximos pasos:${NC}"
    echo -e "  1. Active el entorno virtual: ${GREEN}source env/bin/activate${NC}"
    echo -e "  2. O use el script de activación: ${GREEN}./activate_env.sh${NC}"
    echo -e "  3. Inicie Ollama: ${GREEN}ollama serve${NC}"
    echo -e "  4. Ejecute la aplicación: ${GREEN}python main.py${NC}"
    echo
    print_success "¡Listo para usar AI Alcohol!"
}

# Función principal
main() {
    print_header
    
    # Detectar sistema operativo
    detect_os
    
    # Verificar Python
    check_python
    
    # Detectar GPU NVIDIA
    detect_nvidia_gpu
    
    # Instalar CUDA si es necesario
    install_cuda
    
    # Verificar FFmpeg
    check_ffmpeg
    
    # Crear entorno virtual
    create_virtual_environment
    
    # Instalar dependencias
    install_dependencies
    
    # Verificar Ollama
    check_ollama
    
    # Crear script de activación
    create_activation_script
    
    # Mostrar resumen
    show_summary
}

# Ejecutar función principal
main "$@" 