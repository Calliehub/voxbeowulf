# voxbeowulf

Quick Python code to parse the dual-language edition of Beowulf from [Heorot.dk](https://heorot.dk/beo-ru.html)
and render the complete text several ways:
- as a single combined JSON file
- as a single combined CSV
- as separate .ASS (Advanced SubStation Alpha subtitle format) files, one file per fitt

I follow the Heorot.dk line numbering and fitt numbering.

## Pre-Requisites

Get on Python 3.12 and init a virtual env, install pip, then do:

```shell
pip install -r requirements.txt
```

## Execution

```shell
python heorot.py
```

## Copyright Stuff

The Heorot source text is copyright [Benjamin Slade](https://heorot.dk/) 2002-2020.

This work is copyright 2025 by Callie Tweney, and licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1).
