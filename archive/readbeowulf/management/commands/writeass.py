from django.core.management.base import BaseCommand, CommandError
import pysubs2
from readbeowulf.text import get_fitt

PARAMS = {
    'original_style': 'Old English',
    'blank_template': 'data/subtitles/blank.ass',
    'output_file': "data/subtitles/fitt_{fitt_id}.ass"
}

SECONDS_PER_HALF_LINE = 2


class Command(BaseCommand):
    help = 'Writes all the fitts to .ass files, which can then be loaded into Aegisub ' \
           'to do the detailed audio timing work visually.'

    def handle(self, *args, **options):
        for fitt_id in range(0, 44):
            self.stdout.write(f"Writing .ass file for fitt {fitt_id}")
            fitt = get_fitt(fitt_id)

            # init our subtitle file based on the blank template
            subs = pysubs2.load(PARAMS['blank_template'], encoding="UTF-8")
            subs.clear()

            line_number = -1
            start_time = 0
            end_time = start_time + SECONDS_PER_HALF_LINE
            subtitle = None

            for line in fitt:
                # don't write blank tokens
                if line[3].strip() == '':
                    continue

                if line[0] != line_number or line[1] == 'b1':
                    # start new subtitle at half-line boundary
                    if subtitle is not None:
                        subs.append(subtitle)
                    subtitle = pysubs2.SSAEvent(start=pysubs2.make_time(s=start_time),
                                                end=pysubs2.make_time(s=end_time),
                                                style=PARAMS['original_style'])
                    line_number = line[0]
                    start_time += SECONDS_PER_HALF_LINE
                    end_time += SECONDS_PER_HALF_LINE
                    subtitle.name = str(line_number)
                    if line[1] == 'a1':
                         subtitle.name = subtitle.name + 'a'
                    elif line[1] == 'b1':
                        subtitle.name = subtitle.name + 'b'

                subtitle.text += line[3] + ' '

            # append the last line's subtitle too
            if subtitle is not None:
                subs.append(subtitle)

            subs.save(PARAMS['output_file'].format(fitt_id=fitt_id), encoding="UTF-8")
