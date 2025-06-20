# AI Alcohol - Setup Environment Script for Windows
# Este script detecta el sistema operativo, crea un entorno virtual
# e instala CUDA si detecta una GPU NVIDIA en Windows

param(
    [switch]$Force,
    [switch]$SkipCUDA
)

# Función para escribir mensajes con colores
function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Write-Header {
    Write-Host "=================================" -ForegroundColor Magenta
    Write-Host "  AI Alcohol - Setup Environment" -ForegroundColor Magenta
    Write-Host "=================================" -ForegroundColor Magenta
}

# Función para detectar el sistema operativo
function Detect-OS {
    Write-Status "Detectando sistema operativo..."
    
    $os = Get-WmiObject -Class Win32_OperatingSystem
    $osName = $os.Caption
    $osVersion = $os.Version
    
    Write-Success "Sistema detectado: $osName $osVersion"
    return @{
        Name = $osName
        Version = $osVersion
    }
}

# Función para verificar si Python está instalado
function Test-Python {
    Write-Status "Verificando instalación de Python..."
    
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Python encontrado: $pythonVersion"
            
            # Verificar versión mínima (3.8)
            $versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
            if ($versionMatch) {
                $major = [int]$matches[1]
                $minor = [int]$matches[2]
                
                if ($major -eq 3 -and $minor -ge 8) {
                    Write-Success "Versión de Python compatible (>= 3.8)"
                    return $true
                } else {
                    Write-Error "Se requiere Python 3.8 o superior. Versión actual: $pythonVersion"
                    return $false
                }
            }
        }
    } catch {
        Write-Error "Python no está instalado o no está en el PATH"
        return $false
    }
}

# Función para instalar Python en Windows
function Install-Python {
    Write-Status "Instalando Python en Windows..."
    
    $pythonUrl = "https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe"
    $installerPath = "$env:TEMP\python-installer.exe"
    
    try {
        Write-Status "Descargando Python..."
        Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath
        
        Write-Status "Instalando Python..."
        Start-Process -FilePath $installerPath -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1" -Wait
        
        # Refrescar variables de entorno
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        Write-Success "Python instalado correctamente"
        return $true
    } catch {
        Write-Error "Error al instalar Python: $($_.Exception.Message)"
        return $false
    } finally {
        if (Test-Path $installerPath) {
            Remove-Item $installerPath -Force
        }
    }
}

# Función para detectar GPU NVIDIA
function Test-NvidiaGPU {
    Write-Status "Detectando GPU NVIDIA..."
    
    try {
        $gpu = Get-WmiObject -Class Win32_VideoController | Where-Object { $_.Name -like "*NVIDIA*" }
        if ($gpu) {
            $gpuName = $gpu.Name
            $gpuMemory = [math]::Round($gpu.AdapterRAM / 1MB, 0)
            Write-Success "GPU NVIDIA detectada: $gpuName ($gpuMemory MB)"
            return $true
        } else {
            Write-Warning "No se detectó GPU NVIDIA"
            return $false
        }
    } catch {
        Write-Warning "No se pudo detectar GPU NVIDIA"
        return $false
    }
}

# Función para instalar CUDA en Windows
function Install-CUDA {
    param([bool]$HasNvidiaGPU)
    
    if (-not $HasNvidiaGPU -or $SkipCUDA) {
        Write-Warning "Saltando instalación de CUDA"
        return
    }
    
    Write-Status "Instalando CUDA para GPU NVIDIA..."
    
    $cudaUrl = "https://developer.download.nvidia.com/compute/cuda/12.0.0/local_installers/cuda_12.0.0_525.60.13_windows.exe"
    $installerPath = "$env:TEMP\cuda-installer.exe"
    
    try {
        Write-Status "Descargando CUDA..."
        Invoke-WebRequest -Uri $cudaUrl -OutFile $installerPath
        
        Write-Status "Instalando CUDA..."
        Start-Process -FilePath $installerPath -ArgumentList "-s" -Wait
        
        Write-Success "CUDA instalado correctamente"
    } catch {
        Write-Error "Error al instalar CUDA: $($_.Exception.Message)"
        Write-Status "Instale CUDA manualmente desde: https://developer.nvidia.com/cuda-downloads"
    } finally {
        if (Test-Path $installerPath) {
            Remove-Item $installerPath -Force
        }
    }
}

# Función para crear entorno virtual
function New-VirtualEnvironment {
    Write-Status "Creando entorno virtual..."
    
    if (Test-Path "env") {
        if ($Force) {
            Write-Status "Eliminando entorno virtual existente..."
            Remove-Item -Recurse -Force "env"
        } else {
            $response = Read-Host "El directorio 'env' ya existe. ¿Desea eliminarlo y crear uno nuevo? (y/N)"
            if ($response -eq "y" -or $response -eq "Y") {
                Remove-Item -Recurse -Force "env"
            } else {
                Write-Status "Usando entorno virtual existente"
                return
            }
        }
    }
    
    python -m venv env
    Write-Success "Entorno virtual creado en 'env'"
}

# Función para instalar dependencias
function Install-Dependencies {
    param([bool]$HasNvidiaGPU)
    
    Write-Status "Activando entorno virtual e instalando dependencias..."
    
    # Activar entorno virtual
    & ".\env\Scripts\Activate.ps1"
    
    # Actualizar pip
    python -m pip install --upgrade pip
    
    # Instalar dependencias base
    Write-Status "Instalando dependencias base..."
    pip install -r requirements.txt
    
    # Instalar dependencias específicas para GPU si está disponible
    if ($HasNvidiaGPU -and -not $SkipCUDA) {
        Write-Status "Instalando dependencias para GPU NVIDIA..."
        
        # Instalar PyTorch con soporte CUDA
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    } else {
        Write-Status "Instalando PyTorch para CPU..."
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
    }
    
    Write-Success "Dependencias instaladas correctamente"
}

# Función para verificar instalación de Ollama
function Test-Ollama {
    Write-Status "Verificando instalación de Ollama..."
    
    try {
        $ollamaVersion = ollama --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Ollama ya está instalado: $ollamaVersion"
            
            # Verificar si el modelo está descargado
            $modelList = ollama list 2>&1
            if ($modelList -match "llama3:8b") {
                Write-Success "Modelo llama3:8b ya está descargado"
            } else {
                Write-Status "Descargando modelo llama3:8b..."
                ollama pull llama3:8b
            }
        }
    } catch {
        Write-Status "Instalando Ollama..."
        
        # Descargar e instalar Ollama para Windows
        $ollamaUrl = "https://github.com/ollama/ollama/releases/latest/download/ollama-windows-amd64.exe"
        $ollamaPath = "$env:LOCALAPPDATA\Programs\ollama\ollama.exe"
        
        try {
            New-Item -ItemType Directory -Force -Path "$env:LOCALAPPDATA\Programs\ollama"
            Invoke-WebRequest -Uri $ollamaUrl -OutFile $ollamaPath
            
            # Agregar al PATH
            $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
            if ($currentPath -notlike "*ollama*") {
                [Environment]::SetEnvironmentVariable("Path", "$currentPath;$env:LOCALAPPDATA\Programs\ollama", "User")
                $env:Path += ";$env:LOCALAPPDATA\Programs\ollama"
            }
            
            Write-Status "Descargando modelo llama3:8b..."
            & $ollamaPath pull llama3:8b
            
            Write-Success "Ollama instalado correctamente"
        } catch {
            Write-Error "Error al instalar Ollama: $($_.Exception.Message)"
        }
    }
}

# Función para verificar FFmpeg
function Test-FFmpeg {
    Write-Status "Verificando instalación de FFmpeg..."
    
    try {
        $ffmpegVersion = ffmpeg -version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "FFmpeg ya está instalado"
        }
    } catch {
        Write-Status "Instalando FFmpeg..."
        
        # Instalar FFmpeg usando Chocolatey o descarga directa
        if (Get-Command choco -ErrorAction SilentlyContinue) {
            choco install ffmpeg -y
        } else {
            Write-Warning "Chocolatey no está instalado. Instale FFmpeg manualmente desde: https://ffmpeg.org/download.html"
        }
    }
}

# Función para crear script de activación
function New-ActivationScript {
    Write-Status "Creando script de activación..."
    
    $activationScript = @"
# Script para activar el entorno virtual de AI Alcohol en Windows

Write-Host "Activando entorno virtual de AI Alcohol..." -ForegroundColor Green
& ".\env\Scripts\Activate.ps1"

# Configurar variables de entorno para CUDA si está disponible
if (Get-WmiObject -Class Win32_VideoController | Where-Object { `$_.Name -like "*NVIDIA*" }) {
    `$env:CUDA_VISIBLE_DEVICES = "0"
    Write-Host "GPU NVIDIA detectada - CUDA habilitado" -ForegroundColor Green
} else {
    Write-Host "Usando CPU para procesamiento" -ForegroundColor Yellow
}

# Verificar que Ollama esté corriendo
try {
    `$response = Invoke-WebRequest -Uri "http://localhost:11434" -TimeoutSec 5 -ErrorAction Stop
} catch {
    Write-Host "⚠️  Ollama no está corriendo. Ejecute 'ollama serve' en otra terminal" -ForegroundColor Yellow
}

Write-Host "Entorno activado. Ejecute 'python main.py' para iniciar la aplicación." -ForegroundColor Green
"@

    $activationScript | Out-File -FilePath "activate_env.ps1" -Encoding UTF8
    Write-Success "Script de activación creado: activate_env.ps1"
}

# Función para mostrar resumen final
function Show-Summary {
    param([hashtable]$OSInfo, [bool]$HasNvidiaGPU)
    
    Write-Header
    Write-Success "Configuración completada exitosamente!"
    Write-Host ""
    Write-Host "Resumen de la instalación:" -ForegroundColor Cyan
    Write-Host "  • Sistema operativo: $($OSInfo.Name) $($OSInfo.Version)"
    Write-Host "  • Python: $(python --version)"
    Write-Host "  • Entorno virtual: env/"
    Write-Host "  • GPU NVIDIA: $(if ($HasNvidiaGPU) { 'Sí' } else { 'No' })"
    Write-Host "  • CUDA: $(if ($HasNvidiaGPU -and -not $SkipCUDA) { 'Instalado' } else { 'No requerido' })"
    Write-Host "  • Ollama: Instalado"
    Write-Host "  • FFmpeg: Instalado"
    Write-Host ""
    Write-Host "Próximos pasos:" -ForegroundColor Cyan
    Write-Host "  1. Active el entorno virtual: .\env\Scripts\Activate.ps1" -ForegroundColor Green
    Write-Host "  2. O use el script de activación: .\activate_env.ps1" -ForegroundColor Green
    Write-Host "  3. Inicie Ollama: ollama serve" -ForegroundColor Green
    Write-Host "  4. Ejecute la aplicación: python main.py" -ForegroundColor Green
    Write-Host ""
    Write-Success "¡Listo para usar AI Alcohol!"
}

# Función principal
function Main {
    Write-Header
    
    # Detectar sistema operativo
    $osInfo = Detect-OS
    
    # Verificar Python
    if (-not (Test-Python)) {
        if (-not (Install-Python)) {
            Write-Error "No se pudo instalar Python. Instálelo manualmente desde: https://www.python.org/downloads/"
            exit 1
        }
    }
    
    # Detectar GPU NVIDIA
    $hasNvidiaGPU = Test-NvidiaGPU
    
    # Instalar CUDA si es necesario
    Install-CUDA -HasNvidiaGPU $hasNvidiaGPU
    
    # Verificar FFmpeg
    Test-FFmpeg
    
    # Crear entorno virtual
    New-VirtualEnvironment
    
    # Instalar dependencias
    Install-Dependencies -HasNvidiaGPU $hasNvidiaGPU
    
    # Verificar Ollama
    Test-Ollama
    
    # Crear script de activación
    New-ActivationScript
    
    # Mostrar resumen
    Show-Summary -OSInfo $osInfo -HasNvidiaGPU $hasNvidiaGPU
}

# Ejecutar función principal
Main 