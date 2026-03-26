import csv
import random
from datetime import datetime, timedelta


class CsvGenerator:

    CHAINS = ["Hilton", "Marriott", "Radisson", "Accor", "Hyatt"]
    HOTELS = ["Grand Hotel", "Sea View", "Mountain Resort", "City Inn"]
    CITIES = ["Lviv", "Kyiv", "Odesa", "Dnipro"]
    ROOM_TYPES = ["Single", "Double", "Suite"]
    STATUSES = ["pending", "confirmed", "checked-in", "checked-out"]

    def __init__(self, path="hotels.csv", rows=1000):
        self.path = path
        self.rows = rows

    def _random_date(self):
        start = datetime(2024, 1, 1)
        return start + timedelta(days=random.randint(0, 365))

    def generate(self):
        with open(self.path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            writer.writerow([
                "chain_name",
                "hotel_name",
                "description",
                "email",
                "country",
                "city",
                "street",
                "number",
                "room_type",
                "capacity",
                "price",
                "room_number",
                "checkin",
                "checkout",
                "status",
                "rating",
                "comment",
                "review_date"
            ])

            for i in range(self.rows):
                chain = random.choice(self.CHAINS)
                hotel = random.choice(self.HOTELS)
                city = random.choice(self.CITIES)
                room_type = random.choice(self.ROOM_TYPES)

                checkin = self._random_date()
                checkout = checkin + timedelta(days=random.randint(1, 7))

                writer.writerow([
                    chain,
                    f"{chain} {hotel}",
                    f"{hotel} description",
                    f"info{i}@hotel.com",
                    "Ukraine",
                    city,
                    "Shevchenka",
                    random.randint(1, 100),
                    room_type,
                    random.randint(1, 4),
                    random.randint(50, 300),
                    random.randint(1, 500),
                    checkin.date(),
                    checkout.date(),
                    random.choice(self.STATUSES),
                    random.randint(1, 5),
                    "Good hotel",
                    checkin.date()
                ])


if __name__ == "__main__":
    generator = CsvGenerator(rows=1000)
    generator.generate()
    print("CSV file generated successfully")