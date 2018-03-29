# coding=utf-8
# author: zengyuetian


def md5(text):
    import hashlib
    m = hashlib.md5()
    m.update(text)
    return m.hexdigest()
