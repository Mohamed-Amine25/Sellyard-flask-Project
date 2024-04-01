




form_data = {
    'username': ('username', fake.user_name()),
    'password': ('password', fake.password()),
    'email': ('email', fake.email()),
    'firstname': ('firstname', fake.first_name()),
    'lastname': ('lastname', fake.last_name()),
    }
response = requests.post(url, files=form_data, headers=headers)