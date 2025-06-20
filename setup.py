"""
Setup script for AI Alcohol project.

This script installs the AI Alcohol package and its dependencies.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
with open(this_directory / "requirements.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            requirements.append(line)

setup(
    name="ai-alcohol",
    version="1.0.0",
    author="AI Alcohol Team",
    author_email="contact@aialcohol.com",
    description="Sistema de análisis de fluidez verbal en pacientes con enfermedad hepática",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tu-usuario/AI_alcohol",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Topic :: Multimedia :: Video :: Analysis",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
            "myst-parser>=0.15",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-alcohol=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.yaml", "*.yml"],
    },
    keywords=[
        "medical",
        "healthcare",
        "speech-analysis",
        "fluency",
        "hepatic-encephalopathy",
        "cirrhosis",
        "ai",
        "whisper",
        "ollama",
        "audio-processing",
    ],
    project_urls={
        "Bug Reports": "https://github.com/tu-usuario/AI_alcohol/issues",
        "Source": "https://github.com/tu-usuario/AI_alcohol",
        "Documentation": "https://github.com/tu-usuario/AI_alcohol/docs",
    },
) 