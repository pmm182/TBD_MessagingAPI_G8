import requests

if __name__ == '__main__':
    response = requests.get('http://localhost:5000/rooms_by_user?username=test')
    print(response.json())
    print(response.status_code)
