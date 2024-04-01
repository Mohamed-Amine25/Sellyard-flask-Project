import time
from faker import Faker
fake = Faker()

x=0
while x < 10:
    print(fake.user_name())
    print(fake.password())
    print(fake.email())
    print(fake.first_name())
    print(fake.last_name())
    print("\n")
    time.sleep(1)  # Wait for 1 second before generating the next set of fake data
