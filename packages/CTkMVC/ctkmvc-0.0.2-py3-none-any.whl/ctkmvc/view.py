from customtkinter import CTk
from typing import TYPE_CHECKING
from abc import ABC

from .interface import ModelObserver
from .model import ObservableModel

if TYPE_CHECKING:
    from controller import Controller


class View(CTk, ModelObserver):

    '''Base class for views'''

    def __init__(self, controller: 'Controller', model: ObservableModel):

        super().__init__()

        self._controller = controller
        self._model = model

        self._model.add_observer(self)