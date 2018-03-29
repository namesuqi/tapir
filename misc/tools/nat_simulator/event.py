# coding=utf-8
# author: Sun XiaoLei
# 事件触发，观察者模型
# 用于篡改数据包的功能，现在版本的穿透测试用例无此功能，可忽略本文件


class Event(object):
    _observers = {}
    _event_subjects = []

    def __init__(self, subject, event_param):
        self.subject = subject
        self.param = event_param

    @classmethod
    def register(cls, event_subject, observer):
        if event_subject not in cls._event_subjects:
            cls._event_subjects.append(event_subject)
            cls._observers[event_subject] = []
        if observer not in cls._observers[event_subject]:
            cls._observers[event_subject].append(observer)

    @classmethod
    def unregister(cls, event_subject, observer):
        if event_subject not in cls._event_subjects:
            return None
        if observer in cls._observers[event_subject]:
            cls._observers.remove(observer)
        if len(cls._observers[event_subject]) == 0:
            del cls._observers[event_subject]
            cls._event_subjects.remove(event_subject)

    @classmethod
    def notify(cls, subject, event_param):
        if subject not in cls._event_subjects:
            return None
        event = Event(subject, event_param)
        for observer in cls._observers[subject]:
            observer(event)
