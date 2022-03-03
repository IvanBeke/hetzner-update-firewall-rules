import json, socket

def get_ip(hostname: str) -> str:
    ip = socket.gethostbyname(hostname)
    return ip


if __name__ == '__main__':
    with open('hostnames.json') as hosts_file:
        hostnames = json.load(hosts_file)

    for hostname in hostnames:
        print(f'The IP for host {hostname} is {get_ip(hostname)}')
