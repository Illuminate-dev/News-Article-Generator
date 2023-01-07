from main import create_custom_prompt, generate, CUSTOM_MODEL
from test import main as test

while True:
    prompt = create_custom_prompt()
    text = ""
    while True:
        text, x, y, z = generate(prompt, CUSTOM_MODEL, False)
        if input("Regenerate? ") == "no":
            break
    text = text.replace("END", '')
    where = input("Past/Current? ")
    name = input("Name? ")
    with open(f'/home/henry/Pictures/ScienceFair/tests/{where}/{name}-gen-2.txt', 'w') as f:
        f.write(text)
    test(f'/home/henry/Pictures/ScienceFair/tests/{where}/{name}-gen-2.txt', f'/home/henry/Pictures/ScienceFair/tests/{where}/{name}-data-NYT.txt')
    