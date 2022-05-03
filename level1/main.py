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


for package in packages:
    # Get the associated carrier
    # In a real scenario this code can break because we must check if the carrier really exist
    # For the test, we'll assume it will always exist
    associated_carrier = list(filter(lambda car: car['code'] == package['carrier'], carriers))[0]
    
    # Split the date to simplify further process
    splitted_shipping_date = list(map(int, package['shipping_date'].split("-")))

    # Add the carrier delays to the shipping date
    arrival_date = date(splitted_shipping_date[0], splitted_shipping_date[1], splitted_shipping_date[2]) + timedelta(days=associated_carrier['delivery_promise'] + 1)

    output_data["deliveries"].append({
        "package_id": package["id"],
        "expected_delivery": str(arrival_date)
    })

print(output_data)