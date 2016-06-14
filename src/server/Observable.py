from abc import ABCMeta, abstractmethod


class Observable(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def register_observer(self, observer):
        pass

    @abstractmethod
    def unregister_observer(self, observer):
        pass

    @abstractmethod
    def notify_all(self, obj=None):
        pass
