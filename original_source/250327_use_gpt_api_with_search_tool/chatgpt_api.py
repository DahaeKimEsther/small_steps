from openai import OpenAI
import os
os.environ["OPENAI_API_KEY"] = ''
client = OpenAI()

completion = client.chat.completions.create(
                    model="gpt-4o-search-preview",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": f"현재 러시아 우크라이나 전쟁 실황에 대해 말해줘"}
                    ]
                )
                
answer = completion.choices[0].message
print(answer)
