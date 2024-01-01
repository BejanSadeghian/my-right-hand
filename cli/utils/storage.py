import os
from pathlib import Path
import pandas as pd
from datetime import datetime


class Storage:
    def __init__(
        self,
        directory: str,
        filename: str = "persist.pkl",
    ):
        self.directory = Path(directory)
        self.filename = filename
        self.file_path = self.directory / self.filename
        self.data = None

    def create_storage(self) -> None:
        if not self.file_path.exists():
            print(f"Creating file at {self.file_path}")
            self.data = pd.DataFrame(columns=["id"])
            self.data.to_pickle(self.file_path)

    def load(self) -> None:
        self.data = pd.read_pickle(self.file_path)

    def add(self, data: pd.DataFrame) -> None:
        assert self.data is not None, "You must call load() first"
        # Avoid adding new records if the ID is already present
        data = data[~data["id"].isin(self.data["id"])]
        if data.shape[0] != 0:
            data["created"] = datetime.utcnow()
            data = pd.concat([self.data, data])
            data.to_pickle(self.file_path)
            self.load()
        else:
            print("No additions made to file.")

    def search(self, id_list: list[str]) -> pd.DataFrame:
        assert self.data is not None, "You must call load() first"
        return self.data[self.data["id"].isin(id_list)]

    def already_present(self, id_list: list[str]) -> list[bool]:
        assert self.data is not None, "You must call load() first"
        return [id not in self.data["id"].values for id in id_list]

    def delete(self):
        if self.file_path.exists():
            confirmation = input(
                (
                    "Are you sure you want to delete your persisted data? "
                    "Type 'yes' to confirm: "
                )
            )
            if confirmation.lower() == "yes":
                os.remove(self.file_path)
            else:
                print("File deletion cancelled.")
                raise Exception("File deletion was cancelled by the user.")
        else:
            print("No file to delete, are.")
