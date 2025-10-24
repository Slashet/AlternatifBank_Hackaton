import os
import json
from openai import AzureOpenAI

def process_text(text: str) -> str:
    endpoint = "https://team2-1171-resource.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2025-01-01-preview"
    api_key = "3Wqli0vxyAxJckg6bilWgDF6G6o9IrPhKxyIjcAOI74kCAnLuxJlJQQJ99BJACfhMk5XJ3w3AAAAACOGjcdi"  # API anahtarı
    deployment = "gpt-4o"
    
    # OpenAI istemcisini başlat
    client = AzureOpenAI(
        api_key=api_key,
        azure_endpoint=endpoint,
        api_version="2025-01-01-preview"
    )

    try:
        with open("backend/Text/chat_prompt.json", "r", encoding="utf-8") as f:
            messages = json.load(f)
    except FileNotFoundError:
        messages = [{
            "role": "system",
            "content": [{"type": "text", "text": "You are an AI assistant that helps people find information."}]
        }]

    messages.append({
        "role": "user",
        "content": [{"type": "text", "text": text}]
    })

    # AI'dan yanıt al
    completion = client.chat.completions.create(
        model=deployment,
        messages=messages,
        max_tokens=6553,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False
    )

    response = completion.choices[0].message.content

    # AI yanıtını geçmişe ekle
    messages.append({
        "role": "assistant",
        "content": [{"type": "text", "text": response}]
    })

    # Güncellenmiş geçmişi kaydet
    with open("backend/Text/chat_prompt.json", "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

    return response

if __name__ == "__main__":
    # Test için örnek kullanım
    user_input = "merhaba"
    output = process_text(user_input)
    print(f"AI Yanıtı: {output}")