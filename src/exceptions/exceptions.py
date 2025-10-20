from datetime import date


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


# data error
class DataError(Exception):
    detail = "Ошибка даты"

    def __init__(self):
        super().__init__(self.detail)


class DateFromLaterDateToError(DataError):
    def __str__(self):
        return "Дата заезда позже даты выезда"
