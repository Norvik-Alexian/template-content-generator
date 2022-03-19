import os
import config
import openai

from dotenv import load_dotenv

load_dotenv()
OPEN_API_GPT_SECRET_KEY = os.getenv('OPEN_API_GPT_SECRET_KEY')

if not OPEN_API_GPT_SECRET_KEY:
    raise EnvironmentError('You should set OPEN_API_GPT_SECRET_KEY in your environment variable in .env file')


def generate_content(keywords: list):
    openai.api_key = OPEN_API_GPT_SECRET_KEY
    keywords = ' '.join(keywords)
    model = openai.Completion.create(
        engine='text-davinci-001',
        prompt=f'Keywords: {keywords}\nwrite long content about the content:',
        temperature=0.6,
        max_tokens=600,
        top_p=1.,
        frequency_penalty=0.2,
        presence_penalty=0.
    )
    generated_content = model['choices'][0]['text']

    return generated_content, model


def prettify(content: str, finish_reason: str):
    if finish_reason == 'length':
        ending_punctuations = config.ENDING_PUNCTUATIONS
        any_finished_sentence = any([mark in content for mark in ending_punctuations])
        if any_finished_sentence:
            reversed_content = content[::-1]
            last_finished_sentence = len(content) - 1 - min([
                reversed_content.index(mark) for mark in ending_punctuations if mark in content
            ])
            content = content[: last_finished_sentence + 1]

    content = config.space_remover.sub(' ', content)

    return content


def about_us_content():
    generated_content, model = generate_content(config.KEYWORDS)
    content = generated_content.strip()
    finish_reason = model['choices'][0]['finish_reason']

    return prettify(content, finish_reason)
