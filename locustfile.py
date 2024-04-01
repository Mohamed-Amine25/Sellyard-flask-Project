from locust import HttpUser, between, task
from faker import Faker
import requests
fake = Faker()



class RegistrationUser(HttpUser):
    wait_time = between(1, 5)  # Simulates a wait of 1 to 5 seconds between tasks
    
    @task
    def submit_form(self):

        url = f"{self.host}/registration"  # Using the host attribute of HttpUser for flexibility
        headers = {
            "Authorization": "Basic Og==",
            "Content-Type": "multipart/form-data"
        # "Content-Type": "multipart/form-data" is not needed; requests will set it when using files=
        }
        form_data = {
            'username': fake.user_name(),
            'password': fake.password(),
            'email': fake.ascii_email(),
            'firstname': fake.first_name(),
            'lastname': fake.last_name(),
        }
        # Access the registration form
        self.client.get("/registration", headers=headers)

        response = requests.post(url, data=form_data, headers=headers)
        
        # # Submit the registration form
        # self.client.post("/registration", files=form_data, headers=headers)