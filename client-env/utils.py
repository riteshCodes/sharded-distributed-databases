from os import path
from pathlib import Path
import random

import json


def get_file_path(*, data_code):
    return path.join(path.dirname(Path(__file__)), Path('test_data'), Path(f'data-{data_code}-file.json'))


def synthesize_data(*, limit: int):
    # Test data
    random_ids = random.sample(range(1000, 10000), limit)  # 4-digits random number sample selection with limit
    u_ids = [*set(random_ids)]
    # u_ids = []
    names = []
    emails = []
    for u in u_ids:
        names.append(f'N-:{str(u)}')
        emails.append(f'@Email-:{str(u)}')

    data = {'userID': u_ids, 'name': names, 'email': emails}

    with open(get_file_path(data_code=limit), 'w') as d_file:
        json.dump(data, d_file, indent=1)


def read_data(*, data_code: int):
    # synthesize_data(limit=data_code)
    with open(get_file_path(data_code=data_code), "r") as d_file:
        return json.load(d_file)


if __name__ == '__main__':
    # pass
    # print(read_data(data_code=1))
    synthesize_data(limit=1)
    synthesize_data(limit=10)
    synthesize_data(limit=100)
    synthesize_data(limit=1000)