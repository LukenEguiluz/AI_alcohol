import torch
import json
import os
import numpy as np
import soundfile as sf
import gc
import re
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

WHISPER_MODEL_PATH = "openai/whisper-large-v3"

def reconstruir_words(segmento):
    start = segmento["start_time"]
    end = segmento["end_time"]
    texto = segmento.get("transcript", "").strip().lower()
    palabras = re.findall(r'\b\w+\b', texto)
    num_palabras = len(palabras)

    if num_palabras == 0 or end <= start:
        return []

    duracion_total = end - start
    duracion_palabra = duracion_total / num_palabras

    words = []
    for i, palabra in enumerate(palabras):
        word_start = start + i * duracion_palabra
        words.append({
            "word": palabra,
            "start": round(word_start, 2)
        })

    return words

def transcripcion_de_audio(audio_path, diarization_results, output_dir="."):
    print("🔄 Ejecutando transcripción con Whisper (large-v3) en español...")

    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        WHISPER_MODEL_PATH,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        low_cpu_mem_usage=True
    ).to(device)

    processor = AutoProcessor.from_pretrained(WHISPER_MODEL_PATH)
    whisper_pipeline = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        return_timestamps="word",
        chunk_length_s=30,
        stride_length_s=5,
        batch_size=2,
        device=0 if torch.cuda.is_available() else -1
    )

    audio_data, sample_rate = sf.read(audio_path)
    if len(audio_data.shape) > 1:
        audio_data = np.mean(audio_data, axis=1)

    transcriptions = []
    for i, segment in enumerate(diarization_results):
        start_sample = int(segment["start_time"] * sample_rate)
        end_sample = int(segment["end_time"] * sample_rate)
        segment_audio = audio_data[start_sample:end_sample]

        if len(segment_audio) == 0:
            transcriptions.append({"text": "", "chunks": []})
            continue

        result = whisper_pipeline(
            {"raw": segment_audio, "sampling_rate": sample_rate},
            generate_kwargs={"language": "<|es|>"}
        )
        transcriptions.append(result)

        if i % 3 == 0:
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()

    for i, segment in enumerate(diarization_results):
        segment_start = segment["start_time"]
        segment["transcript"] = transcriptions[i]["text"].lower()
        segment["words"] = []

        for chunk in transcriptions[i].get("chunks", []):
            timestamp = chunk.get("timestamp", [None, None])
            if timestamp[0] is not None:
                segment["words"].append({
                    "word": chunk["text"].strip().lower(),
                    "start": round(segment_start + timestamp[0], 2)
                })
            else:
                print(f"⚠️ Palabra sin tiempo de inicio omitida: '{chunk['text']}'")

    for segment in diarization_results:
        texto = segment.get("transcript", "")
        words = segment.get("words", [])
        palabras_texto = re.findall(r'\b\w+\b', texto)

        if not words or len(words) < len(palabras_texto):
            print(f"🔧 Reconstruyendo palabras para el segmento {segment['start_time']:.2f}–{segment['end_time']:.2f}")
            segment["words"] = reconstruir_words(segment)

    aligned_path = os.path.join(output_dir, "aligned_transcription.json")
    with open(aligned_path, "w", encoding="utf-8") as f:
        json.dump(diarization_results, f, ensure_ascii=False, indent=4)

    print(f"✅ Transcripción completada y guardada en '{aligned_path}'.")

    palabras_con_tiempos = []
    for segmento in diarization_results:
        for word in segmento.get("words", []):
            palabras_con_tiempos.append({
                "word": word["word"],
                "start": word["start"]
            })

    tiempos_path = os.path.join(output_dir, "palabras_con_tiempos.json")
    with open(tiempos_path, "w", encoding="utf-8") as f:
        json.dump(palabras_con_tiempos, f, indent=2, ensure_ascii=False)

    print(f"📄 Archivo '{tiempos_path}' generado con todas las palabras y sus tiempos de inicio.")

    return diarization_results
