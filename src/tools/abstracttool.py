from abc import ABCMeta, abstractmethod


class AbstractTool():
    __metaclass__ = ABCMeta

    @abstractmethod
    def configure_data(self):
        pass

    @abstractmethod
    def configure_run_params(self):
        pass

    @abstractmethod
    def run(self):
        pass
