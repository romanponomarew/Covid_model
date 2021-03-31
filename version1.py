import random
import simpy
from termcolor import cprint

TOTAL_NUMBER_OF_CITIZENS = 10000
DAYS_BEFORE_HOSPITALIZATION = [3, 15]
RECOVERY_DAYS = [15, 45]  # Время проведенное в больнице
WEEKS = 1  # Simulation time in weeks
SIM_TIME = WEEKS * 7 * 24  # Simulation time in minutes
time_of_day = "day"  # night
count_days = 1
current_time = 0
time_now = 0


class Citizen:
    def __init__(self, number, work_type, env):
        self.number = number
        self.env = env
        # Вероятноть ношения маски = 50%:
        if random.randint(1, 2) == 1:
            self.wearing_mask = True
        else:
            self.wearing_mask = False
        self.health_status = "healthy"  # infected
        self.antibodies = 0  # Если переболел - больше 0, заболеть не может
        self.in_hospital = False
        self.location = "work"  # shop/fun_places/public_transport/hospital
        self.work = work_type  # office
        for work_building in city_works:
            if self.work == work_building.type_name:
                self.work_building = work_building.fullness_of_people

    def going_to_work(self):
        """
        Находится на работе 9 часов
        :return:
        """
        print("-----------")
        print(f"Человек({self.number}) сейчас на работе, время симуляции-{self.env.now}")
        self.work_building[self.health_status] += 1
        yield self.env.timeout(9)
        self.work_building[self.health_status] -= 1
        print(f"Человек({self.number}) закончил работать, время симуляции-{env.now}")
        print("+++++++++++")

    def use_public_transport(self):
        """
        Находится в общественном траснпорте от 30 минут то 1,5 часов
        :return:
        """
        print("-----------")
        public_transport_now = random.choice(city_transport)
        print(f"Человек({self.number}) сейчас в общественном транспорте, время симуляции-{env.now}")
        public_transport_now.fullness_of_people[self.health_status] += 1
        travel_time = random.uniform(0.5, 1.5)
        print(f"Время поездки человека({self.number}) = {travel_time}")
        yield self.env.timeout(travel_time)
        public_transport_now.fullness_of_people[self.health_status] -= 1
        print(f"Человек({self.number}) вышел из общественного транспорта, время симуляции-{env.now}")
        print("+++++++++++")

    def go_to_shop(self):
        """
        Находится в магазине от 10 минут до полтора часа
        :return:
        """
        print("-----------")
        shop_now = random.choice(city_shops)
        print(f"Человек({self.number}) сейчас в магазине, время-{env.now}")
        shop_now.fullness_of_people[self.health_status] += 1
        time_for_shopping = random.uniform(0.16, 1.5)
        print(f"Человек({self.number}) провел в магазине время - {time_for_shopping}")
        yield self.env.timeout(time_for_shopping)
        shop_now.fullness_of_people[self.health_status] -= 1
        print(f"Человек({self.number}) вышел из магазина, время-{env.now}")
        print("+++++++++++")

    def go_to_fun_places(self):
        """
        Находится в кинотеатре, ресторане итд
        от 1 до 2.5 часов
        :return:
        """
        print("-----------")
        fun_place_now = random.choice(city_fun_places)
        print(f"Человек({self.number}) сейчас в торговом центре(кинотеатр итд), время-{env.now}")
        time_for_fun = random.uniform(1, 2.5)
        fun_place_now.fullness_of_people[self.health_status] += 1
        print(f"Человек({self.number}) провел в торговом центре время - {time_for_fun}")
        yield self.env.timeout(time_for_fun)
        fun_place_now.fullness_of_people[self.health_status] -= 1
        print(f"Человек({self.number}) вышел из торгового центра, время-{env.now}")
        print("+++++++++++")

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
        self.health_status = random.choices(["healthy", "ill"], weights=[100, 100 - probability])

    def run(self):
        global current_time
        while True:
            if time_now == 7:  # Сьездить на работу и вернутся с нее
                start_time = self.env.now
                print(f"start_time(время симуляции) человека№{self.number}=", start_time)
                yield self.env.process(self.use_public_transport())
                yield self.env.process(self.going_to_work())
                yield self.env.process(self.use_public_transport())
                end_time = self.env.now
                print(f"end_time(время симуляции) человека№({self.number})=", end_time)
                print(f"После возвращения с работы на часах человека({self.number})={time_now} часов")
                if 17 <= time_now <= 19:
                    yield self.env.process(self.go_to_fun_places())
                    if random.randint(1, 2) == 1:
                        yield self.env.process(self.go_to_shop())
                    yield self.env.process(self.use_public_transport())

                    print(f"После развлечений и магазина(возможно) на часах человека({self.number})={time_now} часов")

            yield self.env.timeout(0.0001)  # Для того чтобы можно было вызвать как генератор


class Building:
    """
    Базовый класс всех помещений
    """

    def __init__(self, type_name):
        self.fullness_of_people = {"healthy": 0, "infected": 0}
        self.amount_of_people = sum(self.fullness_of_people.values())
        self.type_name = type_name


class Work(Building):
    """
    Базовый класс для видов работ(помещений)
    """

    def __init__(self, type_name):
        super().__init__(type_name)
        # self.name_of_work = name_of_work  #


class Shop(Building):
    """
    Класс магазинов
    """

    def __init__(self, type_name):
        super().__init__(type_name)
        # self.name = name


class FunPlaces(Building):
    """
    Базовый класс развлекательных мест
    """

    def __init__(self, type_name):
        super().__init__(type_name)
        # self.type_name = type_name  # cinema, food_court, bowling


class PublicTransport(Building):
    """
        Класс развлекательных мест
        """

    def __init__(self, type_name):
        super().__init__(type_name)
        # self.type_of_transport = type_of_transport  # bus, metro


def calendar(env):
    global time_now
    global count_days
    cprint("=" * 25 + f"День №1" + "=" * 25, "green")
    while True:
        print("Сейчас 7утра, время симуляции=", env.now)
        time_now = 7
        while time_now < 22:
            yield env.timeout(1)
            time_now += 1
        if time_now >= 22:
            print("Наступила ночь, время симуляции =", env.now)
            yield env.timeout(9)
            count_days += 1
            cprint("=" * 25 + f"Следующий день №{count_days}" + "=" * 25, "green")


def location_checking(env):
    count_checking_work = 0
    while True:
        time_for_checking = 0.33
        for location in all_city_places:
            if isinstance(location, Work):
                count_checking_work += 1
                if count_checking_work <= 20:
                    continue
                else:
                    print("Проверяем работу")
                    count_checking_work = 0
                    # Проверяем количество людей на работе каждые 2 часа
            quantity_of_people = sum(location.fullness_of_people.values())
            if quantity_of_people > 1:
                cprint("=" * 25 + f"Скопление людей({quantity_of_people}) в {location.type_name}" + "=" * 25,
                    "yellow")
                cprint("\t" + f"Среди них ({location.fullness_of_people['healthy']}) здоровых людей в {location.type_name}", "yellow")
                cprint("\t" + f"Среди них ({location.fullness_of_people['infected']}) зараженных людей в {location.type_name}",
                       "yellow")
                if location.fullness_of_people['infected'] > 0:
                    cprint(
                        "\t" + f"В локации {location.type_name} есть зараженные({location.fullness_of_people['infected']}) !!!",
                        "red")
                    # TODO: Вызвать функцию заражения здоровых людей
        yield env.timeout(time_for_checking)  # Проверяем каждые 20 минут


##########################
# env = simpy.Environment()
env = simpy.rt.RealtimeEnvironment(initial_time=0, factor=0.001, strict=False)
env.process(calendar(env))

############# Работа ###################
office = Work(type_name="office")
school = Work(type_name="school")
city_works = [office, school]
############# Транспорт ###################
bus1 = PublicTransport(type_name="bus")
bus2 = PublicTransport(type_name="bus")
metro1 = PublicTransport(type_name="metro")
metro2 = PublicTransport(type_name="metro")
city_transport = [bus1, bus2, metro1, metro2]
############# Магазины ###################
pyaterochka = Shop(type_name="Пятерочка")
magnit = Shop(type_name="Магнит")
perekrestok = Shop(type_name="Перекресток")
city_shops = [pyaterochka, magnit, perekrestok]
############# Развлекательные места ###################
# cinema, food_court, bowling
cinema = FunPlaces(type_name="cinema")
food_court = FunPlaces(type_name="food_court")
bowling = FunPlaces(type_name="bowling")
city_fun_places = [cinema, food_court, bowling]
############# Все места города ###################
all_city_places = city_fun_places + city_shops + city_works + city_transport
print("all_city_places=", all_city_places)
############# Население ###################
human1 = Citizen(number=1, work_type="school", env=env)
env.process(human1.run())
human2 = Citizen(number=2, work_type="office", env=env)
env.process(human2.run())
human3 = Citizen(number=3, work_type="office", env=env)
human3.health_status = "infected"
env.process(human3.run())
human4 = Citizen(number=4, work_type="office", env=env)
env.process(human4.run())
human5 = Citizen(number=5, work_type="office", env=env)
env.process(human5.run())
human6 = Citizen(number=6, work_type="office", env=env)
env.process(human6.run())
city_humans = [human1, human2, human3, human4, human5, human6]
############# Процессы ###################

env.process(location_checking(env))



env.run(until=SIM_TIME)
