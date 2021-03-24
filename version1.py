import random

TOTAL_NUMBER_OF_CITIZENS = 10000
DAYS_BEFORE_HOSPITALIZATION = [3, 15]
RECOVERY_DAYS = [15, 45]  # Время проведенное в больнице


class Citizen:
    def __init__(self, number):
        self.number = number
        # Вероятноть ношения маски = 50%:
        if random.randint(1, 2) == 1:
            self.wearing_mask = True
        else:
            self.wearing_mask = False
        self.health_status = "healthy"  # ill
        self.antibodies = 0  # Если переболел - больше 0, заболеть не может
        self.in_hospital = False
        self.location = "work"  # shop/fun_places/public_transport/hospital

    def going_to_work(self):
        """
        Находится на работе 9 часов
        :return:
        """
        pass

    def use_public_transport(self):
        """
        Находится в общественном траснпорте от 30 минут то 1,5 часов
        :return:
        """
        pass

    def go_to_shop(self):
        """
        Находится в магазине от 10 минут до часа
        :return:
        """
        pass

    def go_to_fun_places(self):
        """
        Находится в кинотеатре, ресторане итд
        от 1 до 2 часов
        :return:
        """
        pass

    def _get_infected(self):
        """
        Заразиться
        :return:
        """
        pass

    def chance_to_infected(self):
        """
        Если в помещении больной человек, есть вероятность заразиться
        :return:
        """
        probability = 40
        self.health_status = random.choices(["healthy", "ill"], weights=[100, 100-probability])


    def run(self):
        while True:
            pass


class Building:
    """
    Базовый класс всех помещений
    """

    def __init__(self):
        self.amount_of_people = 0
        self.amount_of_sick_people = 0
        self.sick_human_in_room = 0


class Work(Building):
    """
    Базовый класс для видов работ(помещений)
    """

    def __init__(self, name_of_work: str):
        super().__init__()
        self.name_of_work = name_of_work


class Shop(Building):
    """
    Класс магазинов
    """

    def __init__(self):
        super().__init__()


class FunPlaces(Building):
    """
    Базовый класс развлекательных мест
    """

    def __init__(self):
        super().__init__()


class PublicTransport(Building):
    """
        Класс развлекательных мест
        """

    def __init__(self):
        super().__init__()
