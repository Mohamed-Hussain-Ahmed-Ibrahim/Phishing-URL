import requests

response = requests.put('http://localhost:8000/api/update_user_info/', data={
    'username': 'new_username',
    'email': 'new_email@example.com',
    'password': 'new_password',
    'old_password': 'old_password',
}, auth=('username', 'password'))

if response.status_code == 200:
    print('User information updated successfully')
else:
    print('Error:', response.text)
