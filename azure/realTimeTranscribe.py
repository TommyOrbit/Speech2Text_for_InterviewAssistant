import azure.cognitiveservices.speech as speechsdk
from config import speech_config
import time


def recognize_from_microphone_once():
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    print("請開始說話...")

    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("辨識結果：", result.text)
    else:
        print("辨識失敗：", result.reason)


def handle_result(evt):
    text = evt.result.text
    if text:
        print(text)

        # # 寫入逐字稿
        # with open("transcript.txt", "a", encoding="utf-8") as f:
        #     f.write(text + "\n")


def recognize_from_microphone():
    # 不切句 / 增加容忍靜音（直播時通常需要這樣）
    speech_config.set_property(
        speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs,
        "30000"   # 30 秒不切句
    )
    speech_config.set_property(
        speechsdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs,
        "30000"
    )

    audio_config = speechsdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    # 每一句/每一段完成時，就會呼叫這個 callback

    print("請開始說話...（Ctrl + C 停止）")

    speech_recognizer.recognized.connect(handle_result)
    speech_recognizer.start_continuous_recognition()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        speech_recognizer.stop_continuous_recognition()
        print("\n已停止")
