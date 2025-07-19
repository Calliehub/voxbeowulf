from django.db import models

from . import audio


class Token(models.Model):

    fitt_id = models.IntegerField(db_index=True)
    para_id = models.IntegerField(db_index=True)
    para_first = models.BooleanField()
    non_verse = models.BooleanField()
    line_id = models.IntegerField(db_index=True)
    half_line = models.CharField(max_length=1)
    token_offset = models.IntegerField()
    caesura_code = models.CharField(max_length=1)
    pre_punc = models.CharField(max_length=2)
    text = models.CharField(max_length=16)
    post_punc = models.CharField(max_length=11)
    syntax = models.CharField(max_length=3)
    parse = models.CharField(max_length=6)
    lemma = models.CharField(max_length=17, db_index=True)
    pos = models.CharField(max_length=2)
    o = models.CharField(max_length=2)
    gloss = models.CharField(max_length=44)
    with_length = models.CharField(max_length=66)


def get_lines(start, end):
    return Token.objects.filter(line_id__range=(start, end)).order_by("pk")


def get_fitt(fitt):
    return Token.objects.filter(fitt_id=fitt).order_by("pk")


def import_tokens(filename):
    with open(filename) as f:
        c = 0
        d = 0
        for line in f:
            parts = line.strip().split("|")

            token, created = Token.objects.get_or_create(
                fitt_id = int(parts[0]),
                para_id = int(parts[1]),
                para_first = parts[2],
                non_verse = parts[3],
                line_id = int(parts[4]),
                half_line = parts[5],
                token_offset = int(parts[6]),
                defaults = dict(
                    caesura_code = parts[7],
                    pre_punc = parts[8],
                    text = parts[9],
                    post_punc = parts[10],
                    syntax = parts[11],
                    parse = parts[12],
                    lemma = parts[13],
                    pos = parts[14],
                    o = parts[15],
                    gloss = parts[16],
                    with_length = parts[17],
                )
            )

            if created:
                c += 1
            else:
                d += 1

    print(c, d)


class Audio(models.Model):

    fitt_id = models.IntegerField(db_index=True)
    line_id = models.IntegerField(db_index=True)
    half_line = models.CharField(max_length=1)

    audio_url = models.CharField(max_length=100)
    start = models.FloatField()
    end = models.FloatField()


def import_audio_data():
    c = 0
    d = 0
    for fitt_id in audio.TIMED_FITTS:
        for fitt_id, line_id, half_line, audio_url, start, end in audio.get_audio_lines(fitt_id):
            audio_data, created = Audio.objects.get_or_create(
                fitt_id = fitt_id,
                line_id = line_id,
                half_line = half_line,
                defaults = dict(
                    audio_url = audio_url,
                    start = start,
                    end = end,
                )
            )

            if created:
                c += 1
            else:
                d += 1

    print(c, d)


def get_lines_audio(start, end):
    return {
        str(audio_data["line_id"]) + audio_data["half_line"]: audio_data
        for audio_data in Audio.objects.filter(line_id__range=(start, end)).values()
    }


def get_fitt_audio(fitt):
    return {
        str(audio_data["line_id"]) + audio_data["half_line"]: audio_data
        for audio_data in Audio.objects.filter(fitt_id=fitt).values()
    }
