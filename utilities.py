"""XOR obfuscation helpers shared by the Chatbook client.

The server uses the same single-byte XOR with key 'K'. This is an
educational stand-in for encryption, not a security mechanism.
"""


def xor(a, b):
    return a ^ b


def cifrar(palabra):
    """Toggle XOR obfuscation. Applying twice restores the original."""
    if palabra is None:
        return ""
    llave = "K"
    result = []
    for letra in palabra:
        result.append(chr(xor(ord(letra), ord(llave))))
    return "".join(result)


def split_names(payload):
    if not payload:
        return []
    return [part.strip() for part in payload.split("|") if part.strip()]


def format_chat_html(raw, current_user):
    import html

    if not raw or raw.strip() in ("", "Null"):
        return (
            '<p style="color:#6b7280;text-align:center;margin-top:48px;">'
            "No messages yet. Say hello!</p>"
        )

    chunks = []
    for line in raw.replace("\r\n", "\n").split("\n"):
        line = line.strip()
        if not line:
            continue
        if "->" in line:
            author, text = line.split("->", 1)
        else:
            author, text = "", line
        author = author.strip()
        text = html.escape(text.strip())
        author_html = html.escape(author)
        mine = author == current_user
        align = "right" if mine else "left"
        bg = "#5b5ce2" if mine else "#ecebff"
        fg = "#ffffff" if mine else "#1c1c28"
        name_color = "#d7d6ff" if mine else "#5b5ce2"
        bubble = (
            f'<table cellspacing="0" cellpadding="8" bgcolor="{bg}">'
            f"<tr><td>"
            f'<span style="color:{name_color}; font-size:11px; font-weight:bold;">{author_html}</span>'
            f"<br/>"
            f'<span style="color:{fg}; font-size:13px;">{text}</span>'
            f"</td></tr></table>"
        )
        chunks.append(
            f'<table width="100%" cellspacing="0" cellpadding="4"><tr>'
            f'<td align="{align}">{bubble}</td>'
            f"</tr></table>"
        )
    return "".join(chunks) or (
        '<p style="color:#6b7280;text-align:center;margin-top:48px;">'
        "No messages yet. Say hello!</p>"
    )
