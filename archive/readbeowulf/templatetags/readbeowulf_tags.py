from django.template.defaulttags import register


@register.filter
def get_audio_start(d, token):
    return d.get(str(token.line_id) + token.half_line, {}).get("start", "")


@register.filter
def get_audio_end(d, token):
    return d.get(str(token.line_id) + token.half_line, {}).get("end", "")
