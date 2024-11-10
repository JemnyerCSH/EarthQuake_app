import requests

def send_alert():
    response = requests.get('http://127.0.0.1:5001/earthquake_notifications')
    print(response.json())

if __name__ == "__main__":
    send_alert()