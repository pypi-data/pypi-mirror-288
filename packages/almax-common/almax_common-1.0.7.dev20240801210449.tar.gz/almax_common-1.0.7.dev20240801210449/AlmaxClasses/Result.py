class Payload:
    def __init__(self, data: dict | list | str, log: dict):
        self.__Data = data
        self.__Log = log

    @property
    def First(self) -> str:
        return self.Data[0] if type(self.Data) == list else "Not a list"

    @property
    def Data(self) -> dict | list:
        return self.__Data

class Result:
    def __init__(
        self,
        valid: bool,
        payload: Payload,
        message: str = "Richiesta eseguita con Successo!",
    ):

        self.__IsValid = valid;
        self.__Message = message;
        self.__Payload = payload;

    @property
    def IsValid(self) -> bool:
        return self.__IsValid;

    @property
    def Message(self) -> str:
        return self.__Message;

    @property
    def Payload(self) -> Payload:
        return self.__Payload;
