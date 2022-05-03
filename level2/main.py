import json
from datetime import date, timedelta

carriers = []
packages = []
output_data = { "deliveries": [] }

# Read from input file
with open("data/input.json", "r") as file:
    data = json.loads(file.read())
    carriers = data["carriers"]
    packages = data["packages"]



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


for package in packages:
    associated_carrier = list(filter(lambda car: car['code'] == package['carrier'], carriers))[0]
    splitted_shipping_date = list(map(int, package['shipping_date'].split("-")))

    shipping_date = date(splitted_shipping_date[0], splitted_shipping_date[1], splitted_shipping_date[2])
    arrival_date = shipping_date + timedelta(days=associated_carrier['delivery_promise'] + 1)
    arrival_date = update_arrival_date_with_weekends(shipping_date, arrival_date)

    output_data["deliveries"].append({
        "package_id": package["id"],
        "expected_delivery": str(arrival_date)
    })

print(output_data)