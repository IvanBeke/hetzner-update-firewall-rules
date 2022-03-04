import json, os
import logging
import socket
from typing import List
from hcloud import Client
from hcloud.firewalls.client import FirewallRule
from dotenv import load_dotenv


logging.basicConfig(
    filename='logfile.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(levelname)s %(asctime)s - %(message)s'
)
logger = logging.getLogger()



def get_ip(hostname: str) -> str:
    ip = socket.gethostbyname(hostname)
    return ip


def create_rule(ips: List[str], port: str, description: str) -> FirewallRule:
    return FirewallRule(
        FirewallRule.DIRECTION_IN,
        FirewallRule.PROTOCOL_TCP,
        ips,
        port=port,
        description=description
    )


if __name__ == '__main__':
    load_dotenv()
    with open('./allowed.json') as allowed_file:
        allowed = json.load(allowed_file)

    with open('./rules.json') as rules_file:
        rules = json.load(rules_file)

    client = Client(os.environ.get('HETZNER_TOKEN'))
    firewall = client.firewalls.get_by_name(os.environ.get('HETZNER_FIREWALL_NAME'))
    whitelist_ips = list(map(lambda ip: f'{ip}/32', [get_ip(hostname) for hostname in allowed['hostnames']])) + allowed['ips']
    firewall_rules = list(map(lambda rule: create_rule(whitelist_ips, **rule), rules))

    try:
        firewall.set_rules(firewall_rules)
        logger.info('Todo bien')
    except BaseException as e:
        logger.error(f'Todo mal {e}')

