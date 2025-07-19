import pysubs2
import re


# list of fitts that have properly timed audio
TIMED_FITTS = [0]


def get_audio_url(fitt_id):
    return f"https://s3.amazonaws.com/readbeowulf/fitt_{fitt_id}.m4a"


def get_audio_lines(fitt_id):
    subs = pysubs2.load(f"data/subtitles/fitt_{fitt_id}.ass", encoding="UTF-8")
    for line in subs:
        line_number = int(re.match(r"\d*", line.name)[0])
        half_line = re.findall(r"[\D']+", line.name)[0]

        start = line.start / 1000.0       # times in .ass are in milliseconds
        end = line.end / 1000.0
        yield fitt_id, line_number, half_line, get_audio_url(fitt_id), start, end
