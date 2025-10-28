from fastapi import HTTPException
from fastapi import status


# already created error
class ObjectAlreadyCreatedError(Exception):
    detail = "Данный объект уже существует"

    def __init__(self):
        super().__init__(self.detail)


class UserAlreadyCreatedError(ObjectAlreadyCreatedError):
    def __init__(self, email: str):
        self.email = email

    def __str__(self):
        return f"Пользователь с таким email({self.email}) уже зарегистрирован"


class UserLoginIncorrect(Exception):
    message = "Неправильно введены данные для входа"

    def __init__(self):
        super().__init__(self.message)


# not found error
class ObjectNotFoundError(Exception):
    detail = "Объект не найден"

    def __init__(self, message):
        super().__init__(message)


class HotelNotFoundError(ObjectNotFoundError):
    def __init__(self, id_hotel: int):
        self.id_hotel = id_hotel

    def __str__(self):
        return f"Отель с id - {self.id_hotel} не найден"


class RoomHotelNotFoundError(ObjectNotFoundError):
    def __init__(self, id_room: int):
        self.id_room = id_room

    def __str__(self):
        return f"Комната с id - {self.id_hotel} не найдена"


class RoomHotelBooked(ObjectNotFoundError):
    def __init__(self, id_room: int):
        self.id_room = id_room

    def __str__(self):
        return f"Все комнаты номера {self.id_hotel} забронированы"


class UserNotFoundError(ObjectNotFoundError):
    def __init__(self, id_user: int):
        self.id_user = id_user

    def __str__(self):
        return "Пользователь не найден"


# data error
class DataError(Exception):
    detail = "Ошибка даты"

    def __init__(self):
        super().__init__(self.detail)


class DateFromLaterDateToError(DataError):
    def __str__(self):
        return "Дата заезда позже даты выезда"


class CustomHttpException(HTTPException):
    status = status.HTTP_400_BAD_REQUEST
    detail = "Указаны некоректные данные в запросе"

    def __init__(self):
        super().__init__(status_code=self.status, detail=self.detail)


class UserEmailAlreadyRegisterHTTPException(CustomHttpException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь с таким email уже зарегистрирован"


class UserLoginIncorrectHTTPException(CustomHttpException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Неверный email или password"


class UserNotFoundHTTPException(ObjectNotFoundError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Пользователь не найден"


class RoomHotelBookedHTTPException(ObjectNotFoundError):
    status = status.HTTP_409_CONFLICT
    detail = "Все комнаты данного номера заняты"
