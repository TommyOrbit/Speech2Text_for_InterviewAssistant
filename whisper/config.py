import glob

# ====== 設定 ======
SAMPLE_RATE = 16000              # Whisper 推薦頻率
BLOCK_SECONDS = 3                # 每段錄音長度（秒）
MODEL_NAME = "medium"            # 選 tiny/base/small/medium/large-v3
LANGUAGE = "zh"                  # 強制使用中文
PROMPT = "請轉錄以下繁體中文內容："   # 提示加強

audio_directory = "../audio-samples/"
audio_list = glob.glob(audio_directory + "*.wav")
