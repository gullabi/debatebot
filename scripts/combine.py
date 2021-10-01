import sys
import json
from convert import convert
from utils import Srt


def main():
    f_diarization = sys.argv[1]
    f_words = sys.argv[2]

    speakers = get_diarization(f_diarization)
    words = get_words(f_words)
    sw = get_speaker_words(speakers, words)
    with open('sw.json', 'w') as out:
        json.dump(sw, out, indent=2)

def get_diarization(f_diarization):
    tracks = json.load(open(f_diarization))
    speakers = []
    for i, r in enumerate(tracks): 
        if i == 0: 
            current_speaker = r[1] 
            start = r[0][0] 
        else: 
            if r[1] != current_speaker: 
                speakers.append(((start, tracks[i-1][0][1]), current_speaker)) 
                current_speaker = r[1] 
                start = r[0][0] 
    speakers.append(((start, tracks[-1][0][1]), current_speaker))
    return speakers

def get_words(f_words):
    if f_words.endswith('json'):
        jsons = open(f_words).read()
        words = []
        for j in jsons.split('}\n'):
            if j:
                result = json.loads(j+'}')
                if result.get('result'):
                    words += result['result']
        return words
    elif f_words.endswith('srt'):
        srt = Srt(f_words)
        srt.readSrt()
        return srt.srt_dicts

def get_speaker_words(speakers, words):
    segments = []
    for (start, end), speaker in speakers:
        speaker_word_list = []
        segment = {}
        for word in words:
            if word['start'] >= start and word['end'] <= end:
                speaker_word_list.append(word['word'])
            elif word['end'] > end:
                # assuming start is still in the segment 
                speaker_word_list.append(word['word'])
                speaker_words = ' '.join(speaker_word_list)
                segment['start'] = start
                segment['end'] = end
                segment['text'] = 'S%s: '%speaker+speaker_words
                segments.append(segment)
                break
    return segments

if __name__ == "__main__":
    main()
