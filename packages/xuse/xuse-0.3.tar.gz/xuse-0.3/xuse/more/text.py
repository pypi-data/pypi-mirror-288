from xuse.mcore.dtype import RoStrList, List, SSDict, Tuple


def text_to_olist(text: str, titles: RoStrList = None) -> Tuple[RoStrList, List[SSDict]]:
    """将 docker ps 等命令的结果解析为字典数组"""

    title_s, *lines = text.split("\n")

    if titles is None:
        # infer
        titles = [s.strip() for s in title_s.split("  ") if s.strip() != ""]

    a = [title_s.index(k) for k in titles]
    n = len(titles)

    olist = []
    for line in lines:
        if len(line) > 0:
            d = {}
            for i in range(n):
                k = titles[i]
                if i < n - 1:
                    d[k] = line[a[i] : a[i + 1]].rstrip()
                else:
                    d[k] = line[a[i] :].rstrip()
            olist.append(d)

    return olist, titles
