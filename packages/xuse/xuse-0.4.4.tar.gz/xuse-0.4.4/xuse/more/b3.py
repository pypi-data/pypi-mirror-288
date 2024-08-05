import re, xuse


def read_text(fp: str, b3data):
    text = xuse.read_text(fp)
    for k, v in b3data.items():
        text = text.replace("{{{%s}}}" % k, v)
    return text


def convert(fp: str, b3data, mode=None):
    assert fp.endswith(".b3")
    dest = xuse.splitext(fp)[0]
    text = read_text(fp, b3data)
    xuse.write_text(text, dest, mode=mode)
    return dest
