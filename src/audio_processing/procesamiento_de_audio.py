import numpy as np
import soundfile as sf
import os
import subprocess
import noisereduce as nr
import librosa
from scipy.signal import butter, filtfilt, iirpeak, lfilter

def butter_bandpass(lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    return butter(order, [low, high], btype='band')

def apply_bandpass(audio_data, sample_rate, lowcut=80, highcut=5000):
    b, a = butter_bandpass(lowcut, highcut, sample_rate)
    return filtfilt(b, a, audio_data)

def normalize_audio(audio_data):
    max_val = np.max(np.abs(audio_data))
    return audio_data / max_val if max_val > 0 else audio_data

def apply_preemphasis(audio_data, coeff=0.95):
    return np.append(audio_data[0], audio_data[1:] - coeff * audio_data[:-1])

def remove_dc_offset(audio_data):
    return audio_data - np.mean(audio_data)

def convert_mp3_to_wav(mp3_path, wav_path):
    try:
        subprocess.run(["ffmpeg", "-y", "-i", mp3_path, wav_path], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return wav_path
    except Exception as e:
        print(f"❌ Error al convertir mp3 a wav: {e}")
        return None

def apply_moving_average_filter(audio_data, window_size=20):
    return np.convolve(audio_data, np.ones(window_size)/window_size, mode='same')

def apply_noise_gate(audio_data, threshold_db=-40.0):
    max_amp = np.max(np.abs(audio_data))
    threshold = max_amp * (10 ** (threshold_db / 20))
    return np.where(np.abs(audio_data) < threshold, 0.0, audio_data)

def apply_eq(audio, sr, eq_settings):
    output = audio.copy()
    for f_center, gain_db, Q in eq_settings:
        gain_linear = 10 ** (gain_db / 20)
        b, a = iirpeak(f_center / (sr / 2), Q)
        filtered = lfilter(b, a, output)
        output = output + (gain_linear - 1) * filtered
    return output

def procesamiento_de_audio(audio_file, output_dir="."):
    print(f"🔄 Procesando: {audio_file}...")

    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    if audio_file.lower().endswith(".mp3"):
        wav_file = os.path.join(output_dir, os.path.splitext(os.path.basename(audio_file))[0] + "_converted.wav")
        audio_file = convert_mp3_to_wav(audio_file, wav_file)
        if not audio_file or not os.path.exists(audio_file):
            raise ValueError("No se pudo convertir MP3 a WAV")

    audio_data, sr = librosa.load(audio_file, sr=16000, mono=True)

    audio_data = remove_dc_offset(audio_data)
    audio_data = normalize_audio(audio_data)
    audio_data = apply_bandpass(audio_data, sr)
    audio_data = apply_preemphasis(audio_data, coeff=0.95)
    audio_data = apply_noise_gate(audio_data, threshold_db=-35.0)

    noise_sample = audio_data[:int(sr * 0.5)]
    audio_data = nr.reduce_noise(y=audio_data, sr=sr, y_noise=noise_sample, prop_decrease=0.9)

    audio_data = apply_moving_average_filter(audio_data, window_size=20)

    eq_transcripcion = [
        (150, -2, 0.8),
        (250, 2, 1),
        (1000, 2, 1),
        (3000, 6, 1),
        (8000, -3, 1.5)
    ]
    audio_data = apply_eq(audio_data, sr, eq_transcripcion)
    audio_data = normalize_audio(audio_data)

    nombre_base = os.path.splitext(os.path.basename(audio_file))[0]
    output_path = os.path.join(output_dir, f"{nombre_base}_whisper_ready.wav")
    sf.write(output_path, audio_data, sr, subtype='PCM_16')

    print(f"✅ Audio listo para Whisper: '{output_path}'\n")
    return output_path










# import numpy as np
# import soundfile as sf
# from scipy.signal import butter, filtfilt
# from scipy.signal import iirpeak, iirfilter, lfilter
# import os
# import subprocess
# import noisereduce as nr

# def butter_bandpass(lowcut, highcut, fs, order=4):
#     nyq = 0.5 * fs
#     low = lowcut / nyq
#     high = highcut / nyq
#     return butter(order, [low, high], btype='band')

# def apply_bandpass(audio_data, sample_rate, lowcut=80, highcut=5000):
#     b, a = butter_bandpass(lowcut, highcut, sample_rate)
#     return filtfilt(b, a, audio_data)

# def normalize_audio(audio_data):
#     return audio_data / np.max(np.abs(audio_data))

# def apply_preemphasis(audio_data, coeff=0.97):
#     return np.append(audio_data[0], audio_data[1:] - coeff * audio_data[:-1])

# def remove_dc_offset(audio_data):
#     return audio_data - np.mean(audio_data)

# def convert_mp3_to_wav(mp3_path, wav_path):
#     try:
#         subprocess.run(["ffmpeg", "-y", "-i", mp3_path, wav_path], check=True,
#                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#         return wav_path
#     except Exception as e:
#         print(f"❌ Error al convertir mp3 a wav: {e}")
#         return None
    
# def apply_moving_average_filter(audio_data, window_size=5):
#     return np.convolve(audio_data, np.ones(window_size)/window_size, mode='same')

# def apply_noise_gate(audio_data, threshold_db=-40.0):
#     """
#     Silencia el audio por debajo de un cierto umbral en dBFS (decibelios relativos al nivel máximo).
#     """
#     # Convertimos umbral de dBFS a valor lineal
#     max_amp = np.max(np.abs(audio_data))
#     threshold = max_amp * (10 ** (threshold_db / 20))

#     # Aplicamos puerta de ruido
#     gated_audio = np.where(np.abs(audio_data) < threshold, 0.0, audio_data)
#     return gated_audio

# def apply_eq(audio, sr, eq_settings):
#     """
#     eq_settings: lista de tuplas (center_freq, gain_db, Q)
#     Ejemplo: [(200, 3, 1), (3000, 5, 1), (7000, -2, 2)]
#     """
#     output = audio.copy()
#     for f_center, gain_db, Q in eq_settings:
#         gain_linear = 10 ** (gain_db / 20)
#         b, a = iirpeak(f_center / (sr / 2), Q)
#         filtered = lfilter(b, a, output)
#         output = output + (gain_linear - 1) * filtered
#     return output

# def procesamiento_de_audio(audio_file):
#     print(f"🔄 Procesando y ecualizando audio: {audio_file}...")

#     # Convertir a WAV si es MP3
#     if audio_file.lower().endswith(".mp3"):
#         wav_file = os.path.splitext(audio_file)[0] + "_converted.wav"
#         audio_file = convert_mp3_to_wav(audio_file, wav_file)
#         if not audio_file or not os.path.exists(audio_file):
#             raise ValueError("No se pudo convertir MP3 a WAV")

#     audio_data, sample_rate = sf.read(audio_file)

#     if len(audio_data.shape) > 1:
#         audio_data = np.mean(audio_data, axis=1)

#     audio_data = remove_dc_offset(audio_data)
#     audio_data = normalize_audio(audio_data)
#     audio_data = apply_bandpass(audio_data, sample_rate)
#     audio_data = apply_preemphasis(audio_data)
#     audio_data = apply_noise_gate(audio_data, threshold_db=-40.0)  # Cambia -40 a -35 o -30 para más agresividad

#     # ruido_base puede ser una sección silenciosa al principio
#     ruido_base = audio_data[0:int(sample_rate)]  # 1 segundo

#     # audio_data = nr.reduce_noise(y=audio_data, sr=sample_rate, y_noise=ruido_base)
#     audio_data = apply_moving_average_filter(audio_data, window_size=30)

#     eq_transcripcion = [
#     (150, -2, 0.8),     # Eliminar hum
#     (250, 2, 1),        # Dar algo de cuerpo
#     (1000, 2, 1),       # Mejorar sílabas medias
#     (3000, 6, 1),       # Potenciar consonantes
#     (8000, -3, 1.5),    # Eliminar silbido de fondo
# ]


#     audio_data = apply_eq(audio_data, sample_rate, eq_transcripcion)

#     audio_data = normalize_audio(audio_data)

#     output_wav = "filtered_audio.wav"
#     sf.write(output_wav, audio_data, sample_rate, subtype='PCM_16')

#     print(f"✅ Audio ecualizado guardado en '{output_wav}'.\n")
#     return output_wav
