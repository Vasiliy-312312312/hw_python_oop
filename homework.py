from dataclasses import dataclass


@dataclass(init=True)
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str  # имя класса тренировки
    duration: float  # длительность тренировки в ч
    distance: float  # дистанция в км
    speed: float  # средняя скорость в км\ч
    calories: float  # количество затраченных килокалорий

    def get_message(self) -> str:
        """Возвращает сообщение с данными о тренировке."""
        return (f'Тип тренировки: {self.training_type}; Длительность: '
                f'{self.duration:.3f} ч.; Дистанция: {self.distance:.3f} '
                f'км; Ср. скорость: {self.speed:.3f} км/ч; Потрачено '
                f'ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    MIN_IN_1_HOUR: int = 60  # Константа для перевода длительности из ч в мин
    LEN_STEP: float = 0.65  # расстояние в м за один шаг
    M_IN_KM: int = 1000  # константа для перевода значений из м в км

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        """Создаёт объект класса Training."""
        self.action = action  # количество совершённых действий
        self.duration = duration  # длительность тренировки в ч
        self.weight = weight  # вес спортсмена
        self.training_type = self.__class__.__name__  # тип тренировки на
        # основе названия класса

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""  # в км\ч
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Определите get_spent_calories в %s.' % (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.training_type,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_2) * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_IN_1_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        """Создаёт объект класса SportsWalking(Training)."""
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CALORIE_1 * self.weight + (self.get_mean_speed()
                ** 2 // self.height) * self.COEFF_CALORIE_2 * self.weight)
                * (self.duration * self.MIN_IN_1_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""

    # Перепоределяем в связи с новым значением
    LEN_STEP: float = 1.38  # Расстояние в м за один гребок
    COEFF_CALORIE_1: float = 1.1
    COEFF_CALORIE_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        """Создаёт объект класса Swimming(Training)."""
        super().__init__(action, duration, weight)
        self.length_pool = length_pool  # длина бассейна в м
        self.count_pool = count_pool  # количетсво раз проплыва бассейна

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)  # в км\ч

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.COEFF_CALORIE_1)
                * self.COEFF_CALORIE_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_training_type = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in dict_training_type:
        return dict_training_type[workout_type](*data)
    else:
        raise AttributeError('Датчики передали неизвестный вид тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
