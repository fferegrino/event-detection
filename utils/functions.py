import datetime


def ms_str(timestamp, fmt='%Y-%m-%d %H:%M:%S'):
    """
    Takes a timestamp in milliseconds and returns a human-readable string represented by the format provided
    :param timestamp:
    :param fmt:
    :return:
    """
    return datetime.datetime.fromtimestamp(timestamp / 1e3).strftime(fmt)
