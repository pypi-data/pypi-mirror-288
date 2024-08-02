from ..mcore.dtype import T, RoList


def get_input(
    prompt: str,
    default_value: T = None,
    required: bool = False,
    choices: RoList[T] = None,
    extra: str = None,
    default_label: str = None,
    required_label: str = None,
    optional_label: str = None,
) -> T:
    """
    获取用户的输入，但是支持一些选项。
    - `required`: 是否为必须输入项，当未输入时会一直循环直到获取有效输入
    - `default_value`: 默认值，当输入为空时使用该默认值
    - `choices`: 限定取值范围
    - `extra`: 额外的提示信息
    - `default_label`: 默认值提示标签
    - `required_label`: 必须项提示标签
    - `optional_label`: 可选项提示标签
    """

    default_label = default_label or "default: "
    required_label = required_label or "required"
    optional_label = optional_label or "optional"

    info_lst = []
    if extra:
        info_lst.append(extra)
    if choices is not None:
        info_lst.append("choices: " + "|".join([str(i) for i in choices]))

    if required:
        info_lst.append(required_label)
        info_s = "(" + ", ".join(info_lst) + ")"
        _prompt = f"{prompt} {info_s}: "

        val = None
        while val is None:
            val = input(_prompt) or None

    else:
        if default_value is None:
            info_lst.append(optional_label)
        else:
            info_lst.append(f"{default_label}{default_value}")
        if len(info_lst) > 0:
            info_s = "(" + ", ".join(info_lst) + ")"
        else:
            info_s = ""
        _prompt = f"{prompt} {info_s}: "
        val = input(_prompt) or default_value

    if choices is not None and val not in choices:
        raise ValueError(f"{val} not in {choices}")

    if isinstance(default_value, bool) and not isinstance(val, bool):
        tvs = ("1", "true", "yes")
        fvs = ("0", "false", "no")
        val = val.lower()
        assert val in tvs or val in fvs, f"{val} is not a valid bool value"
        val = val in tvs

    return val


def get_input_zh(*args, **kwargs):
    """与 `get_input()` 类似，但是提示是中文的"""
    kwargs["default_label"] = "默认为 "
    kwargs["required_label"] = "必须的"
    kwargs["optional_label"] = "可选的"
    return get_input(*args, **kwargs)
