from abc import ABC, abstractmethod

import pandas as pd

from dropbase.helpers.dataframe import to_dtable

pd.DataFrame.to_dtable = to_dtable


class TableABC(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get(self, state, context, store):
        return context, store

    def update(self, state, context, store):
        return context, store

    def add(self, state, context, store):
        return context, store

    def delete(self, state, context, store):
        return context, store

    def row_change(self, state, context, store):
        return context, store
