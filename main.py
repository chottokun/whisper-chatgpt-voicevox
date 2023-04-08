import asyncio
import openai
from chat import chat
from whisper import voice_to_text
from voicevox import text_to_voice_async, text_to_voice_async
from conf import APIKEY, EXIT_PHRASE, SYSTEM_CONTENT
import re
#
openai.api_key = APIKEY
if EXIT_PHRASE =="" : EXIT_PHRASE = 'exit'
if SYSTEM_CONTENT =="" : SYSTEM_CONTENT = 'You are a helpful assistant.'

# Closing word.
SYSTEM_CONTENT += f'終了やストップなどの会話を終了する内容で話しかけられた場合は{EXIT_PHRASE}とだけ必ず返答するものとします。'

async def main():
    messages = []
    exit_flag = False
    while not exit_flag:
        text = voice_to_text()
        print(text)

        # print(text)
        if len(text) < 4 : continue

        messages.append(
            {"role": "user", "content": text}
        )

        is_chunk = True
        chunk_response = ""
        while is_chunk:
            async for response, is_chunk in chat(SYSTEM_CONTENT, messages):
                if not is_chunk: break
                chunk_response += response
                if re.search("[。、「」！？?!.]", response):
                    await text_to_voice_async(chunk_response)
                    chunk_response = ""


        if EXIT_PHRASE in response:
            exit_flag = True
            response = 'またね！'

        messages.append(
            {"role": "assistant", "content": response}
        )
        
        print(f'User   : {text}')
        print(f'ChatGPT: {response}')
        # text_to_voice_async(response)


if __name__ == '__main__':
    asyncio.run(main())
