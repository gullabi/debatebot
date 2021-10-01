import re
import os
import json

DOT = re.compile('(?<=\s)([A-Z][A-Za-z]+)\.([\S\s]*?)(?=\s\s[A-Z][A-Za-z]+\.)')
COLON = re.compile('(?<=\s)([A-Z][A-Za-z]+):([\S\s]*?)(?=\s\s[A-Z][A-Za-z]+:)')

def main():
    dialogues = []
    for filename in os.listdir():
        dialog = dict()
        if filename.endswith('.txt'):
            print(filename)
            dialog['name'] = filename.replace('.txt', '')
            dialog['text'] = get_dialogues(filename)
            print('with %i cues'%len(dialog['text']))
            dialogues.append(dialog)

    with open('platonic.json', 'w') as out:
        json.dump(dialogues, out, indent = 2)

def get_dialogues(filename):
    content = open(filename).read()
    dot = DOT.findall(content)
    colon = COLON.findall(content)
    if len(dot) > len(colon):
        return dot
    else:
        return colon

if __name__ == "__main__":
    main()
