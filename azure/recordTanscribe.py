import azure.cognitiveservices.speech as speechsdk
from config import speech_config


def recognize_from_file(audio_file):
    audio_input = speechsdk.AudioConfig(filename=audio_file)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_input
    )

    print(f"正在辨識音檔：{audio_file}")
    result = recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("辨識結果：", result.text)
    else:
        print("辨識失敗：", result.reason)
