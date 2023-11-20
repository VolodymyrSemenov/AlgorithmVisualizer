from abc import ABC, abstractmethod


class WindowState(ABC):
    def __init__(self, algorithm_visualizer):
        self.av = algorithm_visualizer

    @abstractmethod
    def render_screen(self):
        pass

    # @abstractmethod
    # def click(self):
    #     pass
    #
    # @abstractmethod
    # def what_is_clicked(self, position):
    #     pass
    #
    # @abstractmethod
    # def enter(self):
    #     pass
