import requests

if __name__ == '__main__':
    counter_new_api = 0
    counter_old_api = 0

    counter_email = 22222

    for i in range(100):
        url = f'http://127.0.0.1:5000/lima,peru?userId={counter_email}@gmail.com'
        r_api = requests.get(url)
        jsonData = r_api.json()
        if jsonData['new-api']:
            counter_new_api += 1
        else:
            counter_old_api += 1

        counter_email += 1
        print("Request:", i, "New API:", counter_new_api, "Old API:", counter_old_api)
