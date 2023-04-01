import openai

def chat(SYSTEM_CONTENT: str, messages: list) -> str:

    if len(messages) > 10 * 2:
        messages.pop(1)
        messages.pop(1)

    chat_messages = [{'role': 'system', 'content': SYSTEM_CONTENT}]
    chat_messages.extend(messages)

    # print(chat_messages)

    result = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=chat_messages
    )
    response_text = result['choices'][0]['message']['content']
    return response_text
