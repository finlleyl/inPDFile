from fastapi import HTTPException, status


class PdfException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(PdfException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(PdfException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неправильная почта или пароль"


class TokenNotFoundException(PdfException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен не найден"


class TokenIncorrectFormatException(PdfException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(PdfException):
    status_code = status.HTTP_401_UNAUTHORIZED


class ConfirmationDoesNotExistException(PdfException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Подтверждения не существует"


class ConfirmationAlreadyUsed(PdfException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Подтверждение уже было использовано"


class ConfirmationExpiredException(PdfException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Подтверждение уже просрочено"


class FileNotPDFException(PdfException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Файл не является pdf"


class ConfirmationEmailNotSentException(PdfException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Ошибка при отправке письма подтверждения"
