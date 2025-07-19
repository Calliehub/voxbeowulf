# readbeowulf

A student-oriented reading environment for Bēowulf
with integrated Old English language learning tools.



## import data

```
./manage.py shell -c "from readbeowulf.models import import_tokens; import_tokens('data/brunetti-length.txt')"
./manage.py shell -c "from readbeowulf.models import import_audio_data; import_audio_data()"
```
