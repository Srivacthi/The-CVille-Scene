from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "What are events that are some events that are happening soon in Charlottesville. Here's a website for reference: https://events.c-ville.com/"
        }
    ]
)

print(completion.choices[0].message.content)