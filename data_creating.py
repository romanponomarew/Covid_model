import json
import random
from pprint import pprint

TOTAL_NUMBER_OF_CITIZENS = 10000
TOTAL_NUMBER_OF_WORKS = 5000


city_statistics = dict()
city_statistics["day"] = 0

for person in range(1, TOTAL_NUMBER_OF_CITIZENS):
    city_statistics[str(person)] = \
        {
        "health_status": "healthy",
        "antibodies": False,
        "in_hospital": False,
        "wearing_mask": True,
        "work_location": random.randint(1, TOTAL_NUMBER_OF_WORKS),
        "days_before_moving_to_hospital": 0,
        "days_staying_in_hospital": 0,
         }

for _ in range(5):
    ill_person = str(random.randint(1, TOTAL_NUMBER_OF_CITIZENS))
    city_statistics[ill_person]["health_status"] = "infected"


count = 0
for person in city_statistics:
    if person != "day":
        if city_statistics[person]["health_status"] == "infected":
            count += 1
print(count)


with open("population_data.json", "w", encoding="utf-8", ) as file:
  json.dump(city_statistics, file, ensure_ascii=False)
