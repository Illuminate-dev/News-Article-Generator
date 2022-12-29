import os
import openai
import re
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

TEMPERATURE=1

# PROMPT CONFIG
TOPIC_MESSAGE="Write a news article about {}.\n"
NOTES_MESSAGE="The article should include the following information:\n{}\n"
CAPTION_MESSAGE="Generate two captions for the article which clearly depict a scene. Surround the captions with brackets like this: [caption here] and choose appropriate locations within the article to place them. "
REQUIREMENTS_MESSAGE="Include a title at the start surrounded by parentheses like this: (title here here). This is a lengthy article and must be at least {} words long."

IMAGE_PROMPT="An award winning professional photo with the caption of \"{}\", realistic lighting, photojournalism from The New York Times"


def create_prompt():


    topic = input("What to write about: ")
    notes = []
    while True:
        line = input("Optional notes of info to add (empty for none): ")
        if line:
            notes.append(line)
        else:
            break

    prompt = TOPIC_MESSAGE.format(topic)

    # append notes if notes is not empty
    prompt += NOTES_MESSAGE.format('\n'.join(notes)) if notes.count != 0 else "" 
        
    prompt += CAPTION_MESSAGE

    word_count = input("How many words? ")

    prompt += REQUIREMENTS_MESSAGE.format(word_count if len(word_count) != 0 else 400)

    return prompt


prompt = create_prompt()

response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=3850, temperature=TEMPERATURE)

text = response.get("choices")[0]["text"]

print(text)

text_file = open("out.txt", "w")
text_file.write(text)
text_file.close()

title = re.findall('\((.*?)\)', text)[0]
print(f'Title: {title}')

captions = re.findall('\[(.*?)\]', text)
for caption in captions:
    image = openai.Image.create(prompt=IMAGE_PROMPT.format(caption), n=1, size="1024x1024")
    print(image['data'][0]['url'])
