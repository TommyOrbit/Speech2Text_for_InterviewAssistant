import whisper
import config

def recognize_from_file():
    audio = config.audio_list[0]
    model = whisper.load_model(config.MODEL_NAME)
    result = model.transcribe(audio, language=config.LANGUAGE, prompt=config.PROMPT)
    print(result["text"].strip())
