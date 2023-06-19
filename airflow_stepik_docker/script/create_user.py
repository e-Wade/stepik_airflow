from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser

print('Creating user!!!!!!!!!!!!!!!!!!!!!!!!!!')
user = PasswordUser(models.User())
user.username = 'admin'
user.email = 'new_user_email@example.com'
user.password = '12345'
session = settings.Session()
session.add(user)
session.commit()
session.close()
print('User created!!!!!!!!!!!!!!!!!!!!!!!!!!')