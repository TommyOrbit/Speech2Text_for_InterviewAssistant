import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk


# 載入 .env
load_dotenv()

speech_key = os.getenv("AZURE_SPEECH_KEY")
service_region = os.getenv("AZURE_SPEECH_REGION")

if not speech_key or not service_region:
    raise ValueError("請確認 .env 中已設定 AZURE_SPEECH_KEY 與 AZURE_SPEECH_REGION")

# 建立 Speech 設定
speech_config = speechsdk.SpeechConfig(
    subscription=speech_key,
    region=service_region
)

speech_config.speech_recognition_language = "zh-TW"

