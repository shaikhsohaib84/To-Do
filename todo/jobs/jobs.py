import requests 

def schedule_notification():
    url = f' http://127.0.0.1:8000/task-notification/'
    response = requests.get(url)
    if not response.status_code == 200:
        return False
    data = response.json()
    print('*'*20)
    print(data)
    print('*'*20)