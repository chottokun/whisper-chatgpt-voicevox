from io import BytesIO
import openai
import speech_recognition as sr

r = sr.Recognizer()

from pydub import AudioSegment

r = sr.Recognizer()

def get_audio_from_mic(threshold=150):
    with sr.Microphone(sample_rate=16000) as source:
        print("なにか話してください")
        r.adjust_for_ambient_noise(source)
        while True:
            audio = r.listen(source)
            audio_segment = AudioSegment.from_wav(BytesIO(audio.get_wav_data()))
            rms = audio_segment.rms
            if rms > threshold:
                print("認識中...", rms)
                return audio
            else:
                print("音量が低すぎます。もう一度話してください。")


def voice_to_text():
    audio = get_audio_from_mic()
    audio_data = BytesIO(audio.get_wav_data())
    audio_data.name = 'from_mic.wav'
    transcript = openai.Audio.transcribe('whisper-1', audio_data)
    return transcript['text']
