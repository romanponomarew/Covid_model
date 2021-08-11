import json

input_parameters = {
    "number_of_citizen": 10000,
    "simulating_days": 100,
    "number_of_infected_people": 5,
    "days_before_hospitalization": [3, 15],
    "recovery_days": [15, 45],
    "travel_time": [0.5, 1.5],
    "shopping_time": [0.16, 1.5],
    "fun_time": [1, 2.5],
    "chance_to_infected_one_mask": 3,
    "chance_to_infected_two_mask": 1.5,
    "chance_to_infected_zero_mask": 4,
    "number_of_offices": 4000,
    "number_of_schools": 2000,
    "number_of_metro_works": 2000,
    "number_of_bus": 1500,
    "number_of_metro_wagons": 4000,
    "number_of_shop_pyaterochka": 350,
    "number_of_shop_magnit": 250,
    "number_of_shop_perekrestok": 200,
    "number_of_cinemas": 150,
    "number_of_food_courts": 230,
    "number_of_bowling": 150,
}

with open("data_file.json", "w") as write_file:
    json.dump(input_parameters, write_file)
