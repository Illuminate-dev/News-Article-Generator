import os
import openai
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# PROMPT CONFIG
TOPIC_MESSAGE="Write a news article about {}."
NOTES_MESSAGE="The article should include the following information:\n{}"
CAPTION_MESSAGE="Generate two captions for the article which clearly depict a scene. Surround the captions with brackets and choose appropriate locations within the article to place them."
REQUIREMENTS_MESSAGE="Include a title at the start surrounded by parentheses. This is a lengthy article and must be at least {} words long."


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

response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=2048)  

print(response.get('choices')[0]['text'])

text_file = open("out.txt", "w")
text_file.write(response.get('choices')[0]["text"])
text_file.close()