from abc import ABCMeta, abstractmethod


class AbstractTool(metaclass=ABCMeta):
    @abstractmethod
    def set_input(self):
        """
        - **parameters**, **types**, **return** and **return types**::

                 :return: nothing
        """
        pass

    @abstractmethod
    def configure(self):
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
