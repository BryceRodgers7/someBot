from openai import OpenAI

client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message);
