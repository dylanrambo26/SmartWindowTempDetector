import requests

def close_window(threshold):
    message = f'\nTemperature has reached above {threshold} degrees.\n'
    resp = requests.post(
        'https://textbelt.com/text',
        json={
            'phone': 'number',
            'message': message,
            'key': 'textBelt_API'
        }
    )
    print(resp.json())
    print(message)

def open_window(threshold):
    message = f'\nTemperature has reached below {threshold} degrees.\n'
    resp = requests.post(
        'https://textbelt.com/text',
        json={
            'phone': 'number',
            'message': message,
            'key': 'textBelt_API'
        }
    )
    print(resp.json())
    print(message)
