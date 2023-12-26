from abc import ABC, abstractmethod
from my_right_hand.models import EmailMessage


class EmailRetriever(ABC):
    @abstractmethod
    def authenticate(self) -> None:
        pass

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def retrieve(self, start_date: str, end_date: str) -> list[EmailMessage]:
        pass
