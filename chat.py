# Import openAI library
import openai

# Create a chat function which takes system content and messages as parameters 
async def chat(SYSTEM_CONTENT: str, messages: list) -> list [str, bool]:
    
    # If the length of messages is greater than 10*2, pop 1st and 2nd element from the list
    if len(messages) > 10 * 2:
        messages.pop(1)
        messages.pop(1)

    # Initialize chat messages with system content
    chat_messages = [{"role": "system", "content": SYSTEM_CONTENT}]
    chat_messages.extend(messages)

    # print(chat_messages)

    # Intialize response text variable
    response_text = ""
    
    # Use openAI to create stream for completion
    for chunk in openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_messages,
        top_p=0.2,
        max_tokens=256,
        stream=True,
    ):
        # Check if chunk exists
        if chunk:
            content = chunk.choices[0].get("delta", {}).get("content")
            is_chunk = True
            if content:
                # Append content to response text
                response_text += content
                yield content, is_chunk
    else:
        # If no chunk exists set is_chunk to False and yield response text
        is_chunk = False
        yield response_text, is_chunk

