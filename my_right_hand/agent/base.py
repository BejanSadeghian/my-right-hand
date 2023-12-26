from abc import ABC, abstractmethod
from my_right_hand.models import EmailMessage, EmailReview


class LanguageModule(ABC):
    @abstractmethod
    def review(self, email: EmailMessage) -> EmailReview:
        pass
