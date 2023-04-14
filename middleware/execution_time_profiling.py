import json
import random
import time
import timeit
from os import path
from pathlib import Path
from main import MWare

m_ware = MWare()


def get_file_path(*, data_code):
    return path.join(path.dirname(Path(__file__)), Path('test_data'), Path(f'data-{data_code}-file.json'))


def read_data(*, data_code: int):
    with open(get_file_path(data_code=data_code), "r") as d_file:
        return json.load(d_file)


def execution_time_set(data, set_function):
    if set_function == 'single':
        key = random.sample(data['userID'], 1)[0]
        start_time = time.time()
        m_ware.set_to(key=key, name='single_name', email='single_email')
        total_time = (time.time() - start_time) * 1000
        print(f'Total execution of set_{set_function}: {total_time} ms')

    elif set_function == 'multiple':
        start_time = time.time()
        m_ware.set_multiples(key_list=data['userID'], name_list=data['name'],
                                          email_list=data['email'])
        total_time = (time.time() - start_time) * 1000
        print(f'Total execution of set_{set_function}: {total_time} ms')
    else:
        print(f'{set_function} : function not defined')


def execution_time_get(data, get_function):
    if get_function == 'single':
        key_list = random.sample(data['userID'], 1)
        start_time = time.time()
        m_ware.get_single(key_list=key_list)
        total_time = (time.time() - start_time) * 1000
        print(f'Total execution of get_{get_function}: {total_time} ms')

    elif get_function == 'multiple':
        start_time = time.time()
        m_ware.get_multiple(key_list=data['userID'])
        total_time = (time.time() - start_time) * 1000
        print(f'Total execution of get_{get_function}: {total_time} ms')

    elif get_function == 'range':
        start = random.randint(0, 999)
        end = start + 100
        start_time = time.time()
        m_ware.get_range(start=start, end=end)
        total_time = (time.time() - start_time) * 1000
        print(f'Total execution of get_{get_function}: {total_time} ms')

    else:
        print(f'{get_function} : function not defined')


def execution_time_del(data, del_function):
    if del_function == 'single':
        key_list = random.sample(data['userID'], 1)
        start_time = time.time()
        m_ware.del_single(key_list=key_list)
        total_time = (time.time() - start_time) * 1000
        print(f'Total execution of delete_{del_function}: {total_time} ms')

    elif del_function == 'multiple':
        key_list = random.sample(data['userID'], 100)
        start_time = time.time()
        m_ware.del_multiple(key_list=key_list)
        total_time = (time.time() - start_time) * 1000
        print(f'Total execution of delete_{del_function}: {total_time} ms')
    else:
        print(f'{del_function} : function not defined')


if __name__ == '__main__':
    test_data = read_data(data_code=1000)
    execution_time_set(data=test_data, set_function='single')
    execution_time_set(data=test_data, set_function='multiple')
    execution_time_get(data=test_data, get_function='single')
    execution_time_get(data=test_data, get_function='multiple')
    execution_time_get(data=test_data, get_function='range')
    execution_time_del(data=test_data, del_function='single')
    execution_time_del(data=test_data, del_function='multiple')
