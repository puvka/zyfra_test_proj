from abc import ABC, abstractmethod


class UseCase(ABC):
    def run(self):
        self.validate()
        return self.execute()

    def validate(self):
        pass

    @abstractmethod
    def execute(self):
        pass
