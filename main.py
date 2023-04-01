import openai
from chat import chat
from whisper import voice_to_text
from voicevox import text_to_voice, sentencs_to_talk
from conf import APIKEY, EXIT_PHRASE, SYSTEM_CONTENT

#
openai.api_key = APIKEY
if EXIT_PHRASE =="" : EXIT_PHRASE = 'exit'
if SYSTEM_CONTENT =="" : SYSTEM_CONTENT = 'You are a helpful assistant.'

# Closing word.
SYSTEM_CONTENT += f'終了やストップなどの会話を終了する内容で話しかけられた場合は{EXIT_PHRASE}とだけ必ず返答するものとします。'

def main():
    messages = []
    exit_flag = False
    while not exit_flag:
        text = voice_to_text()
        messages.append(
            {'role': 'user', 'content': text}
        )
        response = chat(SYSTEM_CONTENT, messages)

        if EXIT_PHRASE in response:
            exit_flag = True
            response = 'またね！'

        messages.append(
            {'role': 'assistant', 'content': response}
        )

        print(f'User   : {text}')
        print(f'ChatGPT: {response}')
        sentencs_to_talk(response)


if __name__ == '__main__':
    main()
