import json
from os import path
from pathlib import Path
import random

import matplotlib.pyplot as plt

from main import MWare


def get_file_path(*, data_code):
    return path.join(path.dirname(Path(__file__).parent), Path('synthetic_data'), Path(f'data-{data_code}-file.json'))


def synthesize_data(*, limit: int):
    # Test data
    random_ids = random.sample(range(1000, 10000), limit)  # 4-digits random number sample selection with limit
    u_ids = [*set(random_ids)]
    names = []
    emails = []
    for u in u_ids:
        names.append(f'N-:{str(u)}')
        emails.append(f'@Email-:{str(u)}')

    data = {'userID': u_ids, 'name': names, 'email': emails}

    with open(get_file_path(data_code=limit), 'w') as d_file:
        json.dump(data, d_file, indent=1)


def read_data(*, data_code: int):
    with open(get_file_path(data_code=data_code), "r") as d_file:
        return json.load(d_file)


def visualize_data_distribution(m_ware, keys_limit):
    # set to the appropriate framework for your system
    info = m_ware.key_space_inf()
    mapping = {}
    for idx, value in enumerate(info.values()):
        mapping[f'DB-{idx}'] = value

    # Plot configurations
    plt.title(f'Data Distribution Among Database-Sites')
    plt.xlabel('Database-Sites')
    plt.ylabel('Number of key-value pairs')  # milliseconds(ms), 1 second = 1000 milliseconds

    if len(mapping.keys()) == 2:
        # Set the spacing between the ticks
        plt.xlim([0, 3])
        plt.xticks([1, 2], mapping.keys())
        plt.ylim(0, keys_limit)
        plt.yticks(range(0, int(keys_limit) + 1, int(keys_limit / 10)))
        plt.plot([1, 2], mapping.values(), marker='*')
    else:
        plt.ylim(0, keys_limit / 2)
        plt.yticks(range(0, int(keys_limit / 2) + 1, int(keys_limit / 10)))
        plt.plot(mapping.keys(), mapping.values(), marker='*')

    plt.grid(True)
    plt.savefig(f'distribution-{keys_limit}.pdf', dpi=1200)
    plt.savefig(f'distribution-{keys_limit}.svg', dpi=1200)
    plt.show()


def feed_data(m_ware, data):
    m_ware.flush_all()
    m_ware.set_multiples(key_list=data['userID'], name_list=data['name'], email_list=data['email'])
    print(m_ware.key_space_inf())


if __name__ == '__main__':
    m_ware = MWare()
    feed_data(m_ware, read_data(data_code=1000))
    visualize_data_distribution(m_ware, keys_limit=1000)
