import json
from datetime import date, timedelta
from typing import Tuple

carriers = []
packages = []
country_distance = []
output_data = { "deliveries": [] }


# Read from input file
with open("data/input.json", "r") as file:
    data = json.loads(file.read())
    carriers = data["carriers"]
    packages = data["packages"]
    country_distance = data["country_distance"]



def update_arrival_date_with_weekends(shipping_date: date, arrival_date: date) -> date:
    """
    Calculate the number of days between the shipping date and the arrival date
    Then, for each day between those dates, check if it is a saturday
    """
    nb_days_between = (arrival_date - shipping_date).days

    # Check every date between shipping and arrival
    for middle_date in (shipping_date + timedelta(days=n) for n in range(nb_days_between)):
        day_name = middle_date.strftime("%A") # Get the English name of the day
        if day_name == "Saturday":
            if not associated_carrier["saturday_deliveries"]:
                # The carrier do not deliver on saturdays and sundays, so +2
                arrival_date += timedelta(days=2)
            else:
                # The carrier delivrer on saturday, so only +1 for sunday
                arrival_date += timedelta(days=1)
    return arrival_date

def add_oversea_delays(arrival_date: date, origin: str, dest: str, threshold: int) -> Tuple[date, int]:
    """
    Calculate the delay added by oversea distance
    """
    distance = country_distance[origin][dest]
    oversea_delay = distance // threshold
    return arrival_date + timedelta(days=oversea_delay), oversea_delay


for package in packages:
    # Get the associated carrier
    associated_carrier = list(filter(lambda car: car['code'] == package['carrier'], carriers))[0]
    # Split the date to simplify further process
    splitted_shipping_date = list(map(int, package['shipping_date'].split("-")))

    # Add the carrier delays to the shipping date
    shipping_date = date(splitted_shipping_date[0], splitted_shipping_date[1], splitted_shipping_date[2])
    arrival_date = shipping_date + timedelta(days=associated_carrier['delivery_promise'] + 1)
    
    # Add the weekend delays to the arrival date
    arrival_date = update_arrival_date_with_weekends(shipping_date, arrival_date)

    # Add distance delays
    arrival_date, oversea_delay = add_oversea_delays(arrival_date,package["origin_country"], package["destination_country"], associated_carrier["oversea_delay_threshold"])    

    output_data["deliveries"].append({
        "package_id": package["id"],
        "expected_delivery": str(arrival_date),
        "oversea_delay": oversea_delay
    })

print(output_data)