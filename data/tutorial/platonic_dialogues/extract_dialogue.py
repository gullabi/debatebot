import re
import os
import json

from nltk.tokenize import sent_tokenize

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
def join_sentences(sentences, length=200):
  new_sentences = []
  current_length = 0
  current_no = 0
  current_sentence = ''
  for sentence in sentences:
    current_length += len(sentence)
    current_no += 1
    if current_length > length:
      if current_sentence:
        new_sentences.append(current_sentence)
        current_length = 0
        current_no = 0
        current_sentence = ''
      else:
        #print('WARNING: sentence too long:%i'%len(sentence))
        current_sentence = ' '.join((current_sentence, sentence[:200]))
    else:
      current_sentence = ' '.join((current_sentence, sentence))
    new_sentences.append(current_sentence)
  return new_sentences

def tokenize(dialogues):
  new_dialogues = []
  for speaker, speech in dialogues:
    if len(speech) > 200:
      sentences = sent_tokenize(speech)
      joined_sentences = join_sentences(sentences)
      print(len(sentences), len(joined_sentences))      
      #print(speaker, speech)
      print(sentences)
      print(joined_sentences)
      for sentence in joined_sentences:
        new_dialogues.append((speaker, sentence))
    else:
        new_dialogues.append((speaker, speech))
  return new_dialogues

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
