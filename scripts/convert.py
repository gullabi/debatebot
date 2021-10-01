import json
from utils import Srt, merge_cues, exportSrt, get_cue_dicts_duration

filename = 'audio_only.srt'
audioname = 'audio_only.m4a'
BODY = '<html><body><p></p> %s </body></html>'

def main():
    srt = Srt(filename)
    srt.readSrt()

    new_srt = process(srt)
    #new_srt = srt.srt_dicts

    otrans_dict = convert(new_srt)
    with open(audioname+'.otr', 'w') as out:
        json.dump(otrans_dict, out)
    exportSrt(new_srt, 'ulus_20200605.srt')

def process(srt, t_max = 50):
        #if cue duration smaller than t_max
        # merge until one step before t_max
        # append cue to new list
    new_cues = []
    total_duration = (srt.srt_dicts[0]['end'] - srt.srt_dicts[0]['start']).total_seconds()
    merged_cue = srt.srt_dicts[0]
    for cue in srt.srt_dicts[1:]:
        total_duration += (cue['end'] - cue['start']).total_seconds()
        if total_duration > t_max:
            new_cues.append(merged_cue)
            total_duration = (cue['end'] - cue['start']).total_seconds()
            merged_cue = cue
        else:
            merged_cue = merge_cues(merged_cue, cue)
    # last cue
    new_cues.append(merged_cue)
    if not cue_lists_same(new_cues, srt.srt_dicts):
        raise ValueError("cue lists are not the same")
    return new_cues

def cue_lists_same(cuelist1, cuelist2):
    duration1 = get_global_duration(cuelist1)
    duration2 = get_global_duration(cuelist2)
    text1 = get_all_text(cuelist1)
    text2 = get_all_text(cuelist2)
    if duration1 != duration2 or text1 != text2:
        print(duration1, duration2)
        print(len(text1), len(text2))
        with open('text1', 'w') as out1, open('text2', 'w') as out2:
            out1.write(text1)
            out2.write(text2)
        return False
    return True

def get_global_duration(cuelist):
    return (cuelist[-1]['end'] - cuelist[0]['start']).total_seconds()

def get_all_text(cuelist):
    full_text = ""
    for cue in cuelist:
        full_text += " %s"%cue['text']
    return full_text

def convert(srt):
    p_text = ''
    for cue in srt:
        cue['ts'] = cue['start'].total_seconds()
        cue['ts_text'] = formatted_string(cue['start'])
        p_ts = '<p><span class="timestamp" data-timestamp="{ts}">'\
               '{ts_text}</span></p>'\
               '<p>{text}<br/></p><p><br/></p>'.format(**cue)
        p_text += p_ts
    otrans_dict = {'media':audioname, 'media-time':cue['ts'], 'text':BODY%p_text}
    return otrans_dict

def formatted_string(td):
    full_string = str(td)
    cropped_string = full_string.split('.')[0]
    elements = cropped_string.split(':')
    if not elements[0] == '0':
        return cropped_string
    else:
        return ':'.join(elements[1:])

if __name__ == "__main__":
    main()
