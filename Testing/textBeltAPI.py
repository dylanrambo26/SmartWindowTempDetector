import requests


def close_window(threshold):
    message = f'\nTemperature has reached above {threshold} degrees. Time to close window and turn on AC. \n'
    # resp = requests.post('https://textbelt.com/text', {
    #     'phone': 'PHONE_NUMBER_HERE',
    #     'message': message,
    #     'key': 'textbelt_test', #Append _test to not affect quota
    # })
    # print(resp.json())
    print(message)

def open_window(threshold):
    message = f'\nTemperature has reached below {threshold} degrees. Time to open window and turn off AC. \n'
    # resp = requests.post('https://textbelt.com/text', {
    #     'phone': 'PHONE_NUMBER_HERE',
    #     'message': message,
    #     'key': 'textbelt_test', #Append _test to not affect quota
    # })
    # print(resp.json)
    print(message)

