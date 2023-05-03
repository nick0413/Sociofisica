import openai as gpt

gpt.api_key="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"

conectado=""

resultado=gpt.Completion.create(engine="text-davinci-003",prompt=conectado,n=1,max_tokens=4000)


print(resultado.choices[0].text)