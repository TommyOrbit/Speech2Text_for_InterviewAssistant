import sounddevice as sd
import numpy as np
import whisper
import queue
import threading
import time
import tempfile
import os
import config

print("載入 Whisper 模型中…")
model = whisper.load_model(config.MODEL_NAME)
print("Whisper 模型載入完成！")

audio_queue = queue.Queue()

def audio_callback(indata, frames, time_info, status):
    """錄音時不斷呼叫，把音訊塞到 Queue 中"""
    if status:
        print(f"[錄音狀態]{status}")
    audio_queue.put(indata.copy())

def record_audio():
    """不斷錄音"""
    with sd.InputStream(
        samplerate=config.SAMPLE_RATE,
        channels=1,
        dtype="int16",
        callback=audio_callback
    ):
        while True:
            time.sleep(0.1)

def transcribe_worker():
    """每 BLOCK_SECONDS 秒從 Queue 取一段音，執行 Whisper"""
    audio_buffer = []

    while True:
        try:
            block = audio_queue.get(timeout=1)
            audio_buffer.append(block)

            # 若累積足夠時間
            if len(audio_buffer) * (len(block) / config.SAMPLE_RATE) >= config.BLOCK_SECONDS:

                # 轉為 numpy array
                audio_np = np.concatenate(audio_buffer, axis=0)
                audio_buffer = []  # reset buffer

                # 暫存檔案
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                    wav_path = tmp.name

                # 存成 WAV
                import soundfile as sf
                sf.write(wav_path, audio_np, config.SAMPLE_RATE)

                # Whisper 轉錄
                # print("\n[Whisper 辨識中…]")
                result = model.transcribe(
                    wav_path,
                    language=config.LANGUAGE,
                    prompt=config.PROMPT,
                    fp16=False
                )

                print(result["text"].strip())

                # 移除暫存音檔
                os.remove(wav_path)

        except queue.Empty:
            pass

def recognize_from_microphone():

    print(" 開始錄音（Ctrl + C 結束）")

    # 開啟兩個 Thread：錄音 / 轉錄
    threading.Thread(target=record_audio, daemon=True).start()
    threading.Thread(target=transcribe_worker, daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n停止錄音。")
