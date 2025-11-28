from realTimeTranscribe import recognize_from_microphone
from recordTanscribe import recognize_from_file
import glob

audio_directory = "../audio-samples/"
audio_list = glob.glob(audio_directory + "*.wav")

if __name__ == "__main__":
    # 即時語音辨識
    recognize_from_microphone()

    # # 音檔語音辨識
    # audio_file = audio_list[0]
    # recognize_from_file(audio_file)
