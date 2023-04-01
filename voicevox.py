import requests
import json
import pyaudio
import wave
import io
from time import sleep
import re
from concurrent.futures import ThreadPoolExecutor

def post_audio_query(text: str) -> dict:
    params = {'text': text, 'speaker': 3}
    res = requests.post('http://127.0.0.1:50021/audio_query', params=params)
    return res.json()

def post_synthesis(audio_query_response: dict) -> bytes:
    params = {'speaker': 1}
    headers = {'content-type': 'application/json'}
    audio_query_response_json = json.dumps(audio_query_response)
    res = requests.post(
        'http://127.0.0.1:50021/synthesis',
        data=audio_query_response_json,
        params=params,
        headers=headers
    )
    return res.content

def play_wav(wav_file: bytes):
    wr: wave.Wave_read = wave.open(io.BytesIO(wav_file))
    p = pyaudio.PyAudio()
    format=p.get_format_from_width(wr.getsampwidth())
    channels=wr.getnchannels()
    rate=wr.getframerate()
    output=True
    stream = p.open(
        format=format,
        channels=channels,
        rate=rate,
        output=output
    )
    chunk = 1024
    data = wr.readframes(chunk)
    while len(data) > 0:
        stream.write(data)
        data = wr.readframes(chunk)
    # sleep(0.5)
    stream.close()
    p.terminate()

    return format, channels, rate

def text_to_voice(text: str, i=0):
    res = post_audio_query(text)
    wav = post_synthesis(res)
    play_wav(wav)
    return

def text_to_wav(text: str, i):
    res = post_audio_query(text)
    wav = post_synthesis(res)
    return wav

def split_text(text: str):
    return re.split("(?<=[。、「」])", text)

def sentencs_to_talk(text: str):
    futures = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        for i, t in enumerate(split_text(text)):
            print(t)
            arg = [t,i]
            futures.append(executor.submit(text_to_wav, *arg))
        for future in futures:
            # print(future.result())
            play_wav(future.result())

if __name__ == '__main__':
    # test
    text_to_voice("こんにちは！")

    # https://dic.pixiv.net/a/%E3%81%9A%E3%82%93%E3%81%A0%E3%82%82%E3%82%93 より
    text = "白とライトグリーンのずんだ餅をイメージしたメインカラーに、同じくずんだ餅を彷彿とさせる丸っこい頭、特徴的な大きな耳は鞘入りの枝豆をかたどったデザインとなっている。"
    text+= "「○○なのだー」というように語尾に「なのだー」を付けて喋るのが特徴。"
    text+= "一人称は「ボク」。小説版でしばしば「彼女」と呼ばれており、公式でも一応女の子とされているが、二次創作では男の子(娘)キャラとして扱われることもある（なお公式は二次創作の性別については縛らない姿勢を取っている）。"
    sentencs_to_talk(text)


