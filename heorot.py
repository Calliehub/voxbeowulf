import csv
import json
import logging
import os

import pysubs2
import requests
import structlog
from bs4 import BeautifulSoup
from numbering import FITT_BOUNDARIES, LINE_NUMBER_MARKERS

SECONDS_PER_LINE = 4

ASS_PARAMS = {
    'original_style': 'Old English',
    'modern_style': 'Modern English',
    'big_number_style': 'Big Numbers',
    'all_number_style': 'All Numbers',
    'fitt_heading_style': 'Fitt Headings',
    'blank_template': 'data/blank.ass',
    'output_file': "data/subtitles/fitt_{fitt_id}.ass"
}

# Configure logging
logging.basicConfig(
    format="%(message)s",
    level=logging.INFO,
)

# Configure structlog
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Get a logger
logger = structlog.get_logger()


def fetch_and_store(url, filename):
    if not os.path.exists(filename):
        logger.warn("Fetching HTML from heorot.dk")
        response = requests.get(url)
        response.raise_for_status()  # Ensure we got a valid response

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(response.text)
            return response.text
    else:
        logger.warn("HTML is already stored locally, skipping HTTP fetch")
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()


def parse(html):
    current_line_number = 0
    soup = BeautifulSoup(html, 'html.parser')

    # Extract table or divs containing the two columns
    # Use natural 1-based numbering in the array of lines, to make lining up with the original text easier
    lines = [{"line": 0, "OE": "", "ME": ""}]

    tables = soup.find_all('table', class_='c15')

    if len(tables) > 0:
        for table in tables:
            table_rows = table.find_all('tr')
            last_oe = None

            for row in table_rows:

                note_divs = row.find_all('div')
                if len(note_divs) > 0:
                    for note_div in note_divs:
                        if note_div.get('class') != ['c35']:  # malformation at line 1066 of the Heorot HTML
                            note_div.decompose()

                columns = row.find_all('span', class_='c7')

                if len(columns) >= 2:
                    if len(columns) > 2:
                        logger.debug(f"long row found", line=current_line_number + 1, cols=columns)

                    oe_text = columns[0]
                    me_text = columns[1]

                    if oe_text == last_oe:  # skip dupes
                        continue
                    else:
                        last_oe = oe_text

                    # Remove <a> tags
                    for tag in oe_text.find_all('a'):
                        tag.unwrap()
                    for tag in me_text.find_all('a'):
                        tag.unwrap()

                    current_line_number += 1

                    lines.append({
                        "line": current_line_number,
                        "OE": oe_text.get_text(strip=False).replace("\n", " ").replace('--', ' '),
                        "ME": me_text.get_text(strip=False).replace("\n", " ").replace('--', ' ')
                    })

    return lines


def get_fitt(fitt_num, lines):
    start = FITT_BOUNDARIES[fitt_num][0]
    end = FITT_BOUNDARIES[fitt_num][1] + 1
    return lines[start:end]


def do_file(filestem, url):
    html = fetch_and_store(url, f"data/fitts/{filestem}.html")
    parsed_lines = parse(html)
    logger.info(f"parsed the file", filestem=filestem, url=url, linecount=len(parsed_lines))

    # Save to JSON file
    with open(f"data/fitts/{filestem}.json", "w", encoding="utf-8") as json_file:
        json.dump(parsed_lines, json_file, indent=4, ensure_ascii=False)

    with open(f"data/fitts/{filestem}.csv", mode="w", newline="") as file:
        fieldnames = parsed_lines[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(parsed_lines)

    write_ass(parsed_lines)


def write_ass(lines):
    for fitt_id, fitt_bounds in enumerate(FITT_BOUNDARIES):
        logger.info(f"Writing .ass file for fitt", fitt_id=fitt_id, fitt_bounds=fitt_bounds)
        if fitt_id == 24:
            continue  # there's no 24 in Beowulf

        fitt = get_fitt(fitt_id, lines)

        # init our subtitle file based on the blank template
        subs = pysubs2.load(ASS_PARAMS['blank_template'], encoding="UTF-8")
        subs.clear()
        subs.info["Fitt"] = str(fitt_id)
        subs.info["First Line"] = fitt[0]["line"]
        subs.info["Last Line"] = fitt[-1]["line"]

        line_number = -1
        start_time = 0
        end_time = start_time + SECONDS_PER_LINE
        subtitle = None

        for line in fitt:
            # Old English
            subs.append(make_sub(line['OE'], start_time, end_time, 'original_style'))
            subs.append(make_sub(line['ME'], start_time, end_time, 'modern_style'))
            subs.append(make_sub(line['line'], start_time, end_time, 'all_number_style'))
            try:
                if LINE_NUMBER_MARKERS[line['line']]:
                    subs.append(make_sub(LINE_NUMBER_MARKERS[line['line']], start_time, end_time, 'big_number_style'))
            except KeyError:
                pass  # no big number for this line

            if line['line'] == fitt_bounds[0]:
                subs.append(make_sub(fitt_bounds[2], start_time, end_time, 'fitt_heading_style'))

            # increment for next subtitle
            start_time += SECONDS_PER_LINE
            end_time += SECONDS_PER_LINE
        subs.save(ASS_PARAMS['output_file'].format(fitt_id=fitt_id), encoding="UTF-8")


def make_sub(text, start_time, end_time, style):
    subtitle = pysubs2.SSAEvent(start=pysubs2.make_time(s=start_time),
                                end=pysubs2.make_time(s=end_time),
                                style=ASS_PARAMS[style])
    subtitle.name = style
    subtitle.text = text
    return subtitle


def run():
    do_file("maintext", "https://heorot.dk/beowulf-rede-text.html")


if __name__ == "__main__":
    run()
