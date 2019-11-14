def get_headers(header_raw):
    """
    通过原生请求头获取请求头字典
    :param header_raw: {str} 浏览器请求头
    :return: {dict} headers
    """
    # print(header_raw)
    return dict(line.split(": ", 1) for line in header_raw.strip().split("\n"))


def get_cookies(cookie_raw):
    """
    通过原生cookie获取cookie字段
    :param cookie_raw: {str} 浏览器原始cookie
    :return: {dict} cookies
    """
    return dict(line.split("=", 1) for line in cookie_raw.split("; "))


def get_ts_list(ts_str):
    res = list()
    for line in ts_str.split("\n"):
        if line.startswith('#'):
            continue
        if len(line) < 4:
            continue
        res.append(line)
    return res
            