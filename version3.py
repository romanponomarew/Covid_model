import random
from collections import defaultdict
from pprint import pprint

import simpy
from termcolor import cprint

TOTAL_NUMBER_OF_CITIZENS = 100
DAYS_BEFORE_HOSPITALIZATION = [3, 15]
RECOVERY_DAYS = [15, 45]  # Time spent in the hospital
WEEKS = 6  # Simulation time in weeks
SIM_TIME = WEEKS * 7 * 24  # Simulation time in minutes
time_of_day = "day"  # night
count_days = 1
current_time = 0
time_now = 0
city_statisitics = defaultdict()

# TODO: The version in which we check for infections not by time, but when a new person arrives at the location
# TODO: Parameters settings on 100 person in city


class Citizen:
    def __init__(self, number, work_type, env):
        self.number = number
        self.env = env
        # The probability of wearing a mask = 50%:
        if random.randint(1, 2) == 1:
            self.wearing_mask = True
        else:
            self.wearing_mask = False
        self.health_status = "healthy"  # infected
        self.antibodies = False  # If you have been ill(True), you cannot get sick more
        self.in_hospital = False
        # self.location = "work"  # shop/fun_places/public_transport/hospital
        self.work = work_type  # office

        # Скорее всего, можно убрать
        for work_building in city_works:
            if self.work == work_building.type_name:
                self.work_building = work_building.fullness_of_people

        self.work_location = random.choice(city_works)  # Always same work for one person
        self.days_before_moving_to_hospital = 0
        self.days_staying_in_hospital = 0

        self.sleep_now = False
        self.activity_for_day = {"road_to_work": False, "work": False, "road_from_work": False, "shop": False,
                                 "road_to_home": False, "sleep": False}

    def going_to_work(self):
        """
        Stays at work 9 hours
        :return:
        """
        # print("-----------")
        #     # print(f"Person({self.number}) is at work now, simulation time-{self.env.now}")
        self.contacts_between_people(location=self.work_location)
        health_status = self.health_status
        self.work_location.people_in_building_now.append(self)
        self.work_building[health_status] += 1
        yield self.env.timeout(9)
        self.work_building[health_status] -= 1
        # print(f"Person({self.number}) finished work, simulation time-{env.now}")
        self.work_location.people_in_building_now.remove(self)
        self.activity_for_day["work"] = True
        # print("+++++++++++")

    def contacts_between_people(self, location):
        """
        If location have more than 5 person -> new person in location contacts with only 5 random person
        """
        count_of_contacts = 0
        for people in location.people_in_building_now:
            if count_of_contacts > 5:
                return
            random_person = people
            if len(location.people_in_building_now) > 5:
                random_person = random.choice(location.people_in_building_now)
                count_of_contacts += 1

            if self.health_status == "healthy":
                if random_person.health_status == "infected":
                    self.chance_to_infected(infected_man=random_person)
            elif self.health_status == "infected":
                if random_person.health_status == "healthy":
                    random_person.chance_to_infected(infected_man=self)



    def go_to_sleep(self):
        """
        Sleep for 9 часов
        :return:
        """
        # print("-----------")
        # print(f"Person({self.number}) goes to sleep, simulation time-{self.env.now}")
        self.sleep_now = True
        yield self.env.timeout(9)
        self.sleep_now = False
        # print(f"Person({self.number}) finished sleeping, simulation time-{env.now}")
        self.activity_for_day["sleep"] = True
        # print("+++++++++++")

    def use_public_transport(self):
        """
        Located in public transport from 30 minutes to 1.5 hours
        :return:
        """
        # print("-----------")
        public_transport_now = random.choice(city_transport)
        self.contacts_between_people(location=public_transport_now)
        health_status = self.health_status
        # print(f"Person({self.number}) is on public transport now, simulation time-{env.now}")
        public_transport_now.fullness_of_people[health_status] += 1
        public_transport_now.people_in_building_now.append(self)
        travel_time = random.uniform(0.5, 1.5)
        # print(f"Travel time of person({self.number}) = {travel_time}")
        yield self.env.timeout(travel_time)
        public_transport_now.fullness_of_people[health_status] -= 1
        public_transport_now.people_in_building_now.remove(self)
        # print(f"Person({self.number}) left public transport, simulation time-{env.now}")
        # print("+++++++++++")

    def go_to_shop(self):
        """
        Located in the shop from 10 minutes to 1.5 hours
        :return:
        """
        # print("-----------")
        shop_now = random.choice(city_shops)
        self.contacts_between_people(location=shop_now)
        health_status = self.health_status
        # print(f"Person({self.number}) is on shop now, simulation time-{env.now}")
        shop_now.fullness_of_people[health_status] += 1
        shop_now.people_in_building_now.append(self)
        time_for_shopping = random.uniform(0.16, 1.5)
        # print(f"Person({self.number}) spent in shop time - {time_for_shopping}")
        yield self.env.timeout(time_for_shopping)
        shop_now.fullness_of_people[health_status] -= 1
        shop_now.people_in_building_now.remove(self)
        self.activity_for_day["shop"] = True
        # print(f"Person({self.number}) left shop, simulation time-{env.now}")
        # print("+++++++++++")

    def go_to_fun_places(self):
        """
        Located in the cinema, restaurant, etc from 1 hour to 2.5 hours
        :return:
        """
        # print("-----------")
        fun_place_now = random.choice(city_fun_places)
        self.contacts_between_people(location=fun_place_now)
        # print(f"Person({self.number})in a shopping center (cinema, etc.) now, simulation time-{env.now}")
        time_for_fun = random.uniform(1, 2.5)
        health_status = self.health_status
        fun_place_now.fullness_of_people[health_status] += 1
        fun_place_now.people_in_building_now.append(self)
        # print(f"Person({self.number}) spent in a shopping center (cinema, etc.) time - {time_for_fun}")
        yield self.env.timeout(time_for_fun)
        fun_place_now.fullness_of_people[health_status] -= 1
        fun_place_now.people_in_building_now.remove(self)
        # print(f"Person({self.number}) left shopping center (cinema, etc.), simulation time-{env.now}")
        # print("+++++++++++")

    def chance_to_infected(self, infected_man):
        """
        If a sick person in the room, there is a chance of getting infection
        :return:
        """
        # print(f"Healthy person({self.number}) wearing mask? - ({self.wearing_mask})")
        # print(f"Sick person({infected_man.number}) wearing mask? - ({infected_man.wearing_mask})")
        if self.wearing_mask or infected_man.wearing_mask:
            chance = 4
            if self.wearing_mask and infected_man.wearing_mask:
                chance = 2
        else:
            chance = 7
        # print(f"Person ({self.number}) can get infected from person ({infected_man.number}) with probability = {chance}")
        probability = random.randint(0, 101)
        # self.health_status = random.choices(["healthy", "infected"], weights=[100, 100 - probability])
        if probability < chance:
            self.health_status = "infected"
            self.days_before_moving_to_hospital = random.randint(3, 15)  # Choosing the number of
            # days before hospitalization



    def run(self):
        global current_time
        while True:
            if self.in_hospital is not True:
                if self.sleep_now == False:
                    # if time_now == 7:  # Go to work and return from it
                    # start_time = self.env.now
                    # print(f"start_time(simulation time) of person№{self.number}=", start_time)
                    if not self.activity_for_day["sleep"]:
                        yield self.env.process(self.go_to_sleep())
                    if not self.activity_for_day["road_to_work"]:
                        yield self.env.process(self.use_public_transport())
                        self.activity_for_day["road_to_work"] = True
                    if not self.activity_for_day["work"]:
                        yield self.env.process(self.going_to_work())
                    if not self.activity_for_day["road_from_work"]:
                        yield self.env.process(self.use_public_transport())
                        self.activity_for_day["road_from_work"] = True

                    # end_time = self.env.now
                    # print(f"end_time(simulation time) person№({self.number})=", end_time)
                    # print(f"After returning from work on a person's watch ({self.number}) time={time_now}")
                    # if 17 <= time_now <= 19:
                    yield self.env.process(self.go_to_fun_places())
                    if random.randint(1, 2) == 1:
                        yield self.env.process(self.go_to_shop())
                    yield self.env.process(self.use_public_transport())
                    self.activity_for_day["road_to_home"] = True
                    if self.activity_for_day["road_to_home"]:
                        for activity in self.activity_for_day:
                            self.activity_for_day[str(activity)] = False

                        # print(f"After entertainment and shopping (possibly) on a person's watch({self.number}) time={time_now}")

            yield self.env.timeout(0.0001)  # In order to be able to call as a generator


class Building:
    """
    Base class of all locations
    """

    def __init__(self, type_name):
        self.fullness_of_people = {"healthy": 0, "infected": 0}
        self.amount_of_people = sum(self.fullness_of_people.values())
        self.type_name = type_name
        self.people_in_building_now = []


class Work(Building):
    """
    Base class of all work locations
    """

    def __init__(self, type_name):
        super().__init__(type_name)
        # self.name_of_work = name_of_work  #


class Shop(Building):

    def __init__(self, type_name):
        super().__init__(type_name)
        # self.name = name


class FunPlaces(Building):
    """
    Basic class of fun places
    """

    def __init__(self, type_name):
        super().__init__(type_name)
        # self.type_name = type_name  # cinema, food_court, bowling


class PublicTransport(Building):
    """
    Class of transport locations
    """

    def __init__(self, type_name):
        super().__init__(type_name)
        # self.type_of_transport = type_of_transport  # bus, metro


def people_days_to_hospital():
    """
    The function of changing the number of days before admission to the hospital of each of the infected residents
    :return:
    """
    for people in city_humans:
        if people.days_before_moving_to_hospital != 0 and people.days_before_moving_to_hospital != 1:
            people.days_before_moving_to_hospital -= 1
        if people.days_before_moving_to_hospital == 1:
            print(f"person ({people.number}) is admitted to the hospital a day №{count_days}")
            people.days_before_moving_to_hospital -= 1
            people.in_hospital = True
            people.days_staying_in_hospital = random.randint(15, 45)


def people_staying_in_hospital():
    """
        The function of changing the number of days before admission to the hospital of each of the infected residents
        :return:
    """
    for people in city_humans:
        if people.in_hospital is True:
            if people.days_staying_in_hospital != 0 and people.days_staying_in_hospital != 1:
                people.days_staying_in_hospital -= 1
            if people.days_staying_in_hospital == 1:
                print(f"Person ({people.number}) is discharged from the hospital on the day №{count_days}")
                people.days_staying_in_hospital -= 1
                people.in_hospital = False
                people.antibodies = True
                people.health_status = "healthy"


def checking_hospital():
    """
    Collection of statistics for the current day:
       .Number of inhabitants
       .Number of healthy
       .Number of patients
       .Number of people in the hospital
    """
    global city_statisitics
    city_statisitics[f"Day№{count_days}"] = {"total_people_in_city": 0, "infected": 0, "healthy": 0,
                                             "people_in_hospital": 0}
    city_statisitics[f"Day№{count_days}"]["total_people_in_city"] = len(city_humans)
    for people in city_humans:
        city_statisitics[f"Day№{count_days}"][people.health_status] += 1
        if people.in_hospital:
            city_statisitics[f"Day№{count_days}"]["people_in_hospital"] += 1
    cprint(
        f"In day №{count_days} in the city there are {city_statisitics[f'Day№{count_days}']['total_people_in_city']} people, "
        f"Among them {city_statisitics[f'Day№{count_days}']['healthy']} are healthy,"
        f"Among them {city_statisitics[f'Day№{count_days}']['infected'] - city_statisitics[f'Day№{count_days}']['people_in_hospital']} are sick,"
        f"In hospital now {city_statisitics[f'Day№{count_days}']['people_in_hospital']} people", "green")
    with open("test.txt", mode="a") as file:
        file.write(
            f"In day №{count_days} in the city there are {city_statisitics[f'Day№{count_days}']['total_people_in_city']} people, "
            f"Among them {city_statisitics[f'Day№{count_days}']['healthy']} are healthy,"
            f"Among them {city_statisitics[f'Day№{count_days}']['infected'] - city_statisitics[f'Day№{count_days}']['people_in_hospital']} are sick,"
            f"In hospital now {city_statisitics[f'Day№{count_days}']['people_in_hospital']} people" + "\n")


def calendar(env):
    global time_now
    global count_days
    cprint("=" * 25 + f"Day №1" + "=" * 25, "green")
    while True:
        if count_days == 1:
            print("Statistics in the beginning of day:")
            checking_hospital()
        print("Now 7 am of morning, simulation time=", env.now)
        time_now = 7
        while time_now < 22:
            yield env.timeout(1)
            time_now += 1
        if time_now >= 22:
            # print("Night has come, simulation time =", env.now)
            yield env.timeout(9)
            people_days_to_hospital()
            people_staying_in_hospital()
            checking_hospital()
            count_days += 1
            cprint("=" * 25 + f"Next day №{count_days}" + "=" * 25, "green")



##########################
# env = simpy.Environment()
env = simpy.rt.RealtimeEnvironment(initial_time=0, factor=0.001, strict=False)
env.process(calendar(env))

############# Work_places ###################
office_works = [Work(type_name="office") for _ in range(50)]
school_works = [Work(type_name="school") for _ in range(20)]
metro_works = [Work(type_name="metro") for _ in range(30)]
city_works = office_works + school_works + metro_works
############# Transport ###################
transport_bus = [PublicTransport(type_name="bus") for _ in range(15)]
transport_metro = [PublicTransport(type_name="metro") for _ in range(10)]
city_transport = transport_bus + transport_metro
############# Shops ###################
shop_pyaterochka = [Shop(type_name="Пятерочка") for _ in range(10)]
shop_magnit = [Shop(type_name="Магнит") for _ in range(7)]
shop_perekrestok = [Shop(type_name="Перекресток") for _ in range(5)]
city_shops = shop_magnit + shop_perekrestok + shop_pyaterochka
############# Fun places ###################
city_cinema = [FunPlaces(type_name="cinema") for _ in range(3)]
city_food_court = [FunPlaces(type_name="food_court") for _ in range(7)]
city_bowling = [FunPlaces(type_name="bowling") for _ in range(5)]
city_fun_places = city_cinema + city_food_court + city_bowling
############# All places of city ###################
all_city_places = city_fun_places + city_shops + city_works + city_transport
# print("all_city_places=", all_city_places)
############# Population ###################
city_works_string = [city_work.type_name for city_work in city_works]
city_humans = [Citizen(number=i, work_type=random.choice(city_works_string), env=env) for i in
               range(TOTAL_NUMBER_OF_CITIZENS)]
for _ in range(5):
    random_person = random.choice(city_humans)
    random_person.health_status = "infected"
    random_person.days_before_moving_to_hospital = random.randint(3, 15)
for human in city_humans:
    env.process(human.run())

############# Processes ###################

# env.process(location_checking(env))

env.run(until=SIM_TIME)
pprint(city_statisitics)
