import os
import pandas as pd
from abc import ABC, abstractmethod


class exportClient(ABC):
    @abstractmethod
    def save_data(self) -> None:
        raise NotImplementedError("Implement Save Data Method")


class csvClient(exportClient):
    def __init__(
        self,
        file_name: str,
        directory: str,
        exclusions: list[str] = None,
    ):
        self.file_name = file_name
        self.directory = directory
        self.exclusions = exclusions if not None else []

        # Check if the directory exists; if not, create it
        self.path = os.path.join(self.directory, self.file_name)
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def save_data(
        self,
        df: pd.DataFrame,
    ):
        df = df.drop(
            self.exclusions,
            axis=1,
            errors="ignore",
        )
        df.to_csv(self.path, index=False)


class sqlClient(exportClient):
    def save_data(
        self,
        df: pd.DataFrame,
    ):
        pass
