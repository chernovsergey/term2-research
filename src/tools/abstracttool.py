from abc import ABCMeta, abstractmethod


class AbstractTool():
    __metaclass__ = ABCMeta

    @abstractmethod
    def configure_data(self):
        """
        - **parameters**, **types**, **return** and **return types**::

                 :return: nothing
        """
        pass

    @abstractmethod
    def configure_run_params(self):
        """
        - **parameters**, **types**, **return** and **return types**::

                 :return: nothing
        """
        pass

    @abstractmethod
    def run(self):
        """
        - **parameters**, **types**, **return** and **return types**::

              :return: return set of filenames which are the tool output
              :rtype: set(string)
        """
        pass
