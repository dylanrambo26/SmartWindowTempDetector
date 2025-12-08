import requests

# Send a text to the user to close the window given the threshold and season mode from main. Replace +Number and textbelt with proper phone number
# and API key to send the text.
def close_window(threshold, mode):
    
    # User should close the window when its hot in the summer, or close it when its cold in the winter.
    if mode == "summer":
        message = f'\nTemperature has reached above {threshold} degrees. Time to close window.\n'
    else:
        message = f'\nTemperature has reached below {threshold} degrees. Time to close window.\n'

    resp = requests.post(
        'https://textbelt.com/text',
        json={
            'phone': '+Number',
            'message': message,
            'key': 'textbelt'
        }
    )
    print(resp.json())
    print(message)

# Send a text to the user to open the window given the threshold and season mode from main. Replace +Number and textbelt with proper phone number
# and API key to send the text.
def open_window(threshold, mode):

    # User should open the window when its cold in the summer, or open it when its warm in the winter.
    if mode == "summer":
        message = f'\nTemperature has reached below {threshold} degrees. Time to open window.\n'
    else:
        message = f'\nTemperature has reached above {threshold} degrees. Time to open window.\n'
    resp = requests.post(
        'https://textbelt.com/text',
        json={
            'phone': '+Number',
            'message': message,
            'key': 'textbelt'
        }
    )
    print(resp.json())
    print(message)
