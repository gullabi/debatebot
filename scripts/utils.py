import re
import os
import pickle
import logging

from datetime import datetime, timedelta
from math import floor

ts = '\d\d:\d\d:\d\d.\d+|\d\d:\d\d:\d+'
cue_clean = '<.+>'
token_clean = '\.|,|:|;|!|\?|"|\.\.\.|\(|\)|-|–|-#| - |’|‘|¿|¡| · | \' |'

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))

class Srt(object):
    def __init__(self,filename):
        self.filename = filename
        self.start = None
        self.srt_dicts = []

    def readSrt(self):
        self.find_first()
        with  open(self.filename, 'r+') as f:
            full = f.read()
            if full.find('\r') == -1:
                self.cue_seperator = '\n\n'
                self.delimiter = '\n'
            else:
                cue_seperator = '\r\n\r\n'
                self.self.delimiter = '\r\n'
            if self.start == -1:
                raise ValueError('the first cue not found. '
                                 'are you sure the file %s has srt format?'\
                                 %self.filename)
        srt_lines = full[self.start:].split(self.cue_seperator)
        self.get_srt_dicts(srt_lines)

    def find_first(self):
        with open(self.filename, 'r+') as f:
            full = f.read()
        #match = re.search('(?<=\s\s).*\s.*\s-->',full)
        match = re.search('\d\s.*\s-->',full)
        if not match:
            self.start = -1
        else:
            self.start = match.start()
            print(self.start)

    def get_srt_dicts(self,srt_lines):
        for srt in srt_lines:
            if srt:
                self.srt_dicts.append(self.get_srt_dict(srt))
     
    def get_srt_dict(self,srt_line):
        srt_elements = srt_line.split(self.delimiter)
        m = re.search('({0}) --> ({0})'.format(ts),srt_elements[1])
        start_td,end_td = [string2timedelta(m.group(i+1)) for i in range(2)]

        text = re.sub('<[^>]*>','',srt_elements[2])
        if start_td > end_td:
            msg = "cue start is later than end: %s --> %s\n"\
                  "for line %s"%(str(start_td),str(end_td),srt_elements[1])
            logging.error(msg)
            raise ValueError(msg)
        return {'start':start_td.total_seconds(),
                'end':end_td.total_seconds(), 'word':text}
       
    def outputSentences(self,outname):
        with open(outname,'w') as out:
            for cue in self.srt_dicts:
                if not cue['text'].startswith('#'):
                    out.write('{0}\n'.format(re.sub('(\(.+\))','',cue['text'])))

    def outputWords(self,outname):
        with open(outname,'w') as out:
            for cue in self.srt_dicts:
                if not cue['text'].startswith('#'):
                    for word in cue['text'].split():
                        if not word.startswith('('):
                            out.write('{0}\n'.format(word))

    @property
    def duration(self):
        if not self.srt_dicts:
            return None
        else:
            return (self.srt_dicts[-1]['end']).total_seconds()

def string2timedelta(time_string):
        time_array = [float(t.replace(',','.')) for t in time_string.split(':')]
        return timedelta(hours = time_array[0], \
                              minutes = time_array[1], seconds = time_array[2])

def exportSrt(cue_dicts, outname):
    with open(outname, 'w') as f:
        for i, cue in enumerate(cue_dicts):
            line = i+1
            start = timedelta2srt(cue['start'])
            end = timedelta2srt(cue['end'])
            text = cue['text']
            f.write('%s\n'%line)
            f.write('%s --> %s\n'%(start,end))
            f.write('%s\n\n'%text)

def export_srt_from_cues(cues, outname):
    with open(outname, 'w') as f:
        for i, cue in enumerate(cues):
            line = i+1
            start = timedelta2srt(cue.start)
            end = timedelta2srt(cue.end)
            f.write('%s\n'%line)
            f.write(('%s --> %s\n'%(start,end)).replace('.',','))
            f.write('%s\n\n'%cue.text)

def timedelta2srt(td):
    '''
    inputs timedelta outputs srt formatted string
    '''
    if type(td) == timedelta:
        total_seconds = td.total_seconds()
    elif type(td) == float or type(td) == int:
        total_seconds = td
    else:
        msg = "total seconds has unknown type:", type(td)
        logging.error(msg)
        raise TypeError(msg)

    if total_seconds < 0:
        msg = "total seconds cannot be negative: %f"%total_seconds
        logging.error(msg)
        raise ValueError(msg)
    elif total_seconds > 86400:
        msg = "total seconds cannot be larger than a day: %f"%total_seconds
        logging.error(msg)
        raise ValueError(msg)
    else:
        hours = floor(total_seconds/60./60.)
        mod_hours = total_seconds%(60.*60.)
        minutes = floor(mod_hours/60.)
        seconds = mod_hours%60.
        return ('%02d:%02d:%06.3f'%(hours, minutes, seconds))

def get_cue_dict_lists_duration(cue_dict_lists):
    '''
    gets the total duration of a list of list of cue dicts
    '''
    total_duration = timedelta(seconds=0)
    for cue_dicts in cue_dict_lists:
        total_duration += get_cue_dicts_duration(cue_dicts)
    return total_duration

def get_cue_dicts_duration(cue_dicts):
    total_duration = timedelta(seconds=0)
    for cue in cue_dicts:
        total_duration += cue['end'] - cue['start']
    return total_duration

def merge_cues(cue1, cue2):
    if cue2['start'] > cue1['start']:
        first_cue = cue1
        second_cue = cue2
    else:
        first_cue = cue2
        second_cue = cue1
    if (second_cue['start']-first_cue['end']).total_seconds() > 2:
        print('WARNING: cues might not be consecutive', first_cue, second_cue)
    new_cue = {'start': first_cue['start'],
               'end': second_cue['end'],
               'text': ' '.join([first_cue['text'],second_cue['text']])}
    return new_cue
