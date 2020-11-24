import sys
import requests

fullcommand = {}

while True:
    print(f'Enter Command [Client]: ')

    command = str(input())
    fullcommand["cmd"] = command

    splitcmd = command.split()

    if command.lower() == 'exit':
        sys.exit(0)
    if 'GET' in splitcmd:
        resp = requests.get('http://localhost:8080', params=fullcommand)
    elif 'HEAD' in splitcmd:
        resp = requests.head('http://localhost:8080')        
    else:
        resp = requests.get('http://localhost:8080', params=fullcommand)

    print(f'Response from [Server]: ')
    if 'HEAD' in splitcmd:
        print(resp.headers)
    print(f'{resp.content.decode("utf-8")}\n')
