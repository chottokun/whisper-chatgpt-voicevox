import aiohttp
import asyncio
import pyaudio
import wave
import io
from time import sleep
import re
import requests
import json
from concurrent.futures import ThreadPoolExecutor

SPEAKER_ID = 46

async def post_audio_query(text: str) -> dict:
    params = {'text': text, 'speaker': SPEAKER_ID}
    async with aiohttp.ClientSession() as session:
        async with session.post('http://127.0.0.1:50021/audio_query', params=params) as res:
            return await res.json()

async def post_synthesis(audio_query_response: dict) -> bytes:
    params = {'speaker': SPEAKER_ID}
    headers = {'content-type': 'application/json'}
    audio_query_response_json = json.dumps(audio_query_response)
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'http://127.0.0.1:50021/synthesis',
            data=audio_query_response_json,
            params=params,
            headers=headers
        ) as res:
            return await res.read()

async def play_wav_async(wav_file: bytes):
    loop = asyncio.get_running_loop()

    def play():
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
        sleep(0.1)
        stream.close()
        p.terminate()

    await loop.run_in_executor(None, play)

async def text_to_voice_async(text: str, i=0):
    audio_query_response = await post_audio_query(text)
    wav = await post_synthesis(audio_query_response)
    await play_wav_async(wav)

async def text_to_wav_async(text: str, i):
    audio_query_response = await post_audio_query(text)
    wav = await post_synthesis(audio_query_response)
    return wav

def text_to_wav(text: str, i) -> bytes:
    params = {'text': text, 'speaker': SPEAKER_ID}
    res = requests.post('http://127.0.0.1:50021/audio_query', params=params)
    headers = {'content-type': 'application/json'}
    audio_query_response_json = res
    res = requests.post(
        'http://127.0.0.1:50021/synthesis',
        data=audio_query_response_json,
        params=params,
        headers=headers
    )
    return res.content


def split_text(text: str):
    return re.split("(?<=[。、「」！？?!])", text)

async def sentences_to_talk_async(text: str):
    futures = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        for i, t in enumerate(split_text(text)):
            arg = [t,i]
            futures.append(asyncio.get_running_loop().run_in_executor(executor, text_to_wav, *arg))
        results = await asyncio.gather(*futures)
        for result in results:
            await play_wav_async(result)

# async def text_to_talk_async(text: str):
#     for i, t in enumerate(split_text(text)):
#         wav_data = await text_to_wav_async(t, i)
#         await play_wav_async(wav_data)

async def text_to_talk_async(text: str):
    futures = []
    for i, t in enumerate(split_text(text)):
        future = asyncio.create_task(text_to_wav_async(t, i))
        futures.append(future)
    for future in futures:
        wav_data = await future
        await play_wav_async(wav_data)

async def main():
    # test
    print("---------")
    await text_to_voice_async("こんにちは！")
    print("---------")
    await sentences_to_talk_async("こんにちは！元気ですか？私は元気です。今日はとてもいい天気でした。そちらはどうでしたか？")
    print("---------")
    await text_to_talk_async("こんにちは！元気ですか？私は元気です。今日はとてもいい天気でした。そちらはどうでしたか？")
    print("---------")
    return

if __name__ == '__main__':
    asyncio.run(main())