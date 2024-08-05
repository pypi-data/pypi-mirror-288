import re, xuse


def load_from_file(fp: str):
    data = {}
    if xuse.not_exists(fp):
        return data
    for line in xuse.read_text(fp).strip().split("\n"):
        a = line.split("=", 1)
        k = a[0].strip()
        v = a[1].strip()
        if m := re.match(r"^['\"](.*)['\"]$", v):
            v = m.group(1)
        data[k] = v
    return data


def load(project_dir: str, env=".env"):
    data = {}
    srcfile = xuse.join(project_dir, env)
    xuse.di.assign(data, load_from_file(srcfile))
    xuse.di.assign(data, load_from_file(srcfile + ".local"))
    return data
