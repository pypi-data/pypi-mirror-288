from abc import ABCMeta, abstractmethod


class Storage(metaclass=ABCMeta):
    @abstractmethod
    def save(self, data: dict) -> None:
        """
        情報を保存する
        """

    @abstractmethod
    def load(self) -> dict | None:
        """
        情報を取得する
        """
