class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        """Создаёт экземпляр класса InfoMessage."""
        self.training_type = training_type  # имя класса тренировки
        self.duration = duration  # длительность тренировки в ч
        self.distance = distance  # дистанция в км
        self.speed = speed  # средняя скорость в км\ч
        self.calories = calories  # количество затраченных килокалорий

    def get_message(self) -> str:
        """Возвращает сообщение с данными о тренировке."""
        return ((f'Тип тренировки: {self.training_type}; Длительность: ')
                + (f'{self.duration:.3f} ч.; Дистанция: {self.distance:.3f} ')
                + (f'км; Ср. скорость: {self.speed:.3f} км/ч; Потрачено ')
                + (f'ккал: {self.calories:.3f}.'))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65  # расстояние в м за один шаг
    M_IN_KM: int = 1000  # константа для перевода значений из м в км

    action: int
    duration: float
    weight: float
    training_type: str
    InfoMessage: InfoMessage

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
        pass

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

    MIN_IN_HOUR: int = 60  # Константа для перевода длительности из ч в мин

    coeff_calorie_1: int
    coeff_calorie_2: int

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        self.coeff_calorie_1 = 18
        self.coeff_calorie_2 = 20
        return ((self.coeff_calorie_1 * self.get_mean_speed()
                - self.coeff_calorie_2) * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    MIN_IN_HOUR: int = 60  # Константа для перевода длительности из ч в мин

    action: int
    duration: float
    weight: float
    height: float
    coeff_calorie_1: float
    coeff_calorie_2: float

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
        self.coeff_calorie_1 = 0.035
        self.coeff_calorie_2 = 0.029
        return ((self.coeff_calorie_1 * self.weight + (self.get_mean_speed()
                ** 2 // self.height) * self.coeff_calorie_2 * self.weight)
                * (self.duration * self.MIN_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38  # расстояние в м за один гребок

    length_pool: float
    count_pool: int
    coeff_calorie_1: float
    coeff_calorie_2: int
    height: float

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
        self.coeff_calorie_1 = 1.1
        self.coeff_calorie_2 = 2
        return ((self.get_mean_speed() + self.coeff_calorie_1)
                * self.coeff_calorie_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_training_type = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    for abr in dict_training_type:
        if workout_type == abr:
            return dict_training_type[abr](*data)


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
