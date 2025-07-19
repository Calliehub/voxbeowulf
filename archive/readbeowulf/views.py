from django.shortcuts import render, redirect

from account.decorators import login_required

from . import models


MAX_FITT = 43
MAX_LINE = 3182

@login_required
def read_lines(request, start, end):
    audio_behavior = get_and_persist_audio_behavior(request)
    redirect_chunk_type = request.GET.get("chunk_type")
    redirect_chunk_id = request.GET.get("chunk_id")
    try:
        if redirect_chunk_type == "fitt":
            if 0 <= int(redirect_chunk_id) <= MAX_FITT:
                return redirect("read_fitt", int(redirect_chunk_id))
        elif redirect_chunk_type == "lines":
            if "-" in redirect_chunk_id:
                s, e = redirect_chunk_id.split("-")
                return redirect("read_lines", int(s), int(e))
            else:
                return redirect("read_lines", int(redirect_chunk_id), int(redirect_chunk_id))
    except:
        # got error so just go back to original page
        return redirect("read_lines", start, end)

    size = end - start + 1
    if start > 1:
        prev = (max(1, start - size), max(1, start - 1), min(MAX_LINE, start + 1))
    else:
        prev = None
    if end < 3182:
        next = (max(1, end - 1), min(MAX_LINE, end + 1), min(MAX_LINE, end + size))
    else:
        next = None

    return render(request, "read.html", {
        "chunk_type": "lines",
        "scope": f"Lines {start}–{end}" if end != start else f"Line {start}",
        "token_data": models.get_lines(start, end),
        "audio_data": models.get_lines_audio(start, end),
        "prev": prev,
        "next": next,
        "start": start,
        "end": end,
        "audio_behavior": audio_behavior,
    })


@login_required
def read_fitt(request, fitt):
    audio_behavior = get_and_persist_audio_behavior(request)
    redirect_chunk_type = request.GET.get("chunk_type")
    redirect_chunk_id = request.GET.get("chunk_id")
    try:
        if redirect_chunk_type == "fitt":
            if 0 <= int(redirect_chunk_id) <= MAX_FITT:
                return redirect("read_fitt", int(redirect_chunk_id))
        elif redirect_chunk_type == "lines":
            if "-" in redirect_chunk_id:
                s, e = redirect_chunk_id.split("-")
                return redirect("read_lines", int(s), int(e))
            else:
                return redirect("read_lines", int(redirect_chunk_id), int(redirect_chunk_id))
    except:
        # got error so just go back to original page
        return redirect("read_fitt", fitt)


    if fitt == 30:
        prev = 28
    elif fitt == 31:
        prev = 29
    elif fitt > 0:
        prev = max(0, fitt - 1)
    else:
        prev = None
    if fitt == 29:
        next = 31
    elif fitt < MAX_FITT:
        next = min(MAX_FITT, fitt + 1)
    else:
        next = None

    if fitt == 0:
        scope = "Prologue"
    elif fitt in [29, 30]:
        scope = "Fitt 29/30"
    else:
        scope = f"Fitt {fitt}"

    return render(request, "read.html", {
        "chunk_type": "fitt",
        "scope": scope,
        "token_data": models.get_fitt(fitt),
        "audio_data": models.get_fitt_audio(fitt),
        "prev": prev,
        "next": next,
        "start": fitt,
        "end": fitt,
        "audio_behavior": audio_behavior,
    })


@login_required
def vocab_lines(request, start, end):

    redirect_chunk_type = request.GET.get("chunk_type")
    redirect_chunk_id = request.GET.get("chunk_id")
    try:
        if redirect_chunk_type == "fitt":
            if 0 <= int(redirect_chunk_id) <= MAX_FITT:
                return redirect("vocab_fitt", int(redirect_chunk_id))
        elif redirect_chunk_type == "lines":
            if "-" in redirect_chunk_id:
                s, e = redirect_chunk_id.split("-")
                return redirect("vocab_lines", int(s), int(e))
            else:
                return redirect("vocab_lines", int(redirect_chunk_id), int(redirect_chunk_id))
    except:
        # got error so just go back to original page
        return redirect("vocab_lines", start, end)

    return render(request, "vocab.html", {
        "chunk_type": "lines",
        "scope": f"Lines {start}–{end}" if end != start else f"Line {start}",
        "token_data": models.get_lines(start, end).order_by("lemma", "pos", "gloss", "line_id"),
        "start": start,
        "end": end,
    })


@login_required
def vocab_fitt(request, fitt):

    redirect_chunk_type = request.GET.get("chunk_type")
    redirect_chunk_id = request.GET.get("chunk_id")
    try:
        if redirect_chunk_type == "fitt":
            if 0 <= int(redirect_chunk_id) <= MAX_FITT:
                return redirect("vocab_fitt", int(redirect_chunk_id))
        elif redirect_chunk_type == "lines":
            if "-" in redirect_chunk_id:
                s, e = redirect_chunk_id.split("-")
                return redirect("vocab_lines", int(s), int(e))
            else:
                return redirect("vocab_lines", int(redirect_chunk_id), int(redirect_chunk_id))
    except:
        # got error so just go back to original page
        return redirect("vocab_fitt", fitt)


    if fitt == 0:
        scope = "Prologue"
    elif fitt in [29, 30]:
        scope = "Fitt 29/30"
    else:
        scope = f"Fitt {fitt}"

    return render(request, "vocab.html", {
        "chunk_type": "fitt",
        "scope": scope,
        "token_data": models.get_fitt(fitt).order_by("lemma", "pos", "gloss", "line_id"),
        "start": fitt,
        "end": fitt,
    })


def lemma(request, lemma):

    return render(request, "lemma.html", {
        "lemma": lemma,
        "token_data": models.Token.objects.filter(lemma=lemma).order_by("pos", "parse", "o", "text", "gloss"),
    })


def home(request):
    if not request.user.is_authenticated:
        return render(request, "homepage.html")
    else:
        return redirect("read_lines", 1, 11)


def get_and_persist_audio_behavior(request):
     try:
         audio_behavior = request.session["audio_behavior"]
     except KeyError:
         audio_behavior = "continuous"
     if request.GET.get("audio_behavior") is not None:
         audio_behavior = request.GET.get("audio_behavior")

      # persist in session
     request.session["audio_behavior"] = audio_behavior
     return audio_behavior
