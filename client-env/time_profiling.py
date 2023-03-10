from os import path
from pathlib import Path

from time import perf_counter
import timeit
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from openpyxl import load_workbook

# Path to profiling data
FILE_PATH = path.join(path.dirname(Path(__file__).parent), Path('client-env/profiling/client_profiling.xlsx'))
# Set display options pandas
pd.options.display.float_format = '{:.10E}'.format


def get_data_from_excel(*, with_sheet_name: str, header_value=5,
                        with_columns=None):
    if with_columns is None:
        with_columns = ['Execution_Time(seconds)', 'Wall_Time(seconds)']
    data_frame = pd.read_excel(FILE_PATH, header=header_value, sheet_name=with_sheet_name, usecols=with_columns)
    return data_frame.dropna()


def visualize_data(*, measurements=None):
    # Data configurations
    default_x_ticks = np.arange(5)
    keys_range = np.power(10, default_x_ticks)

    # Store latency data in a Pandas DataFrame
    # data = {'keys': keys_range,'latency': measurements}
    # df = pd.DataFrame(data)

    df = get_data_from_excel(with_sheet_name='test_connection')

    # Plot configurations
    fig, axs = plt.subplots()
    for col in df.columns:
        plt.plot(default_x_ticks, df[col], marker='*', label=col)
    plt.xticks(default_x_ticks, keys_range)

    plt.xlabel('Number of key-value pairs (Throughput)')
    plt.ylabel('Latency (seconds)')  # milliseconds(ms), 1 second = 1000 milliseconds
    plt.title('Total Latency: ')
    plt.legend(framealpha=1)
    plt.grid(True)
    plt.show()


def write_to_excel_wall_time(*, sheet_name: str, start_row: int = 7, data):
    df = pd.DataFrame({'Wall_Time(seconds)': data})
    wb = load_workbook(FILE_PATH)
    ws = wb[sheet_name]

    for index, row in df.iterrows():
        cell = 'C%d' % (index + start_row)
        ws[cell] = row[0]

    wb.save(FILE_PATH)


def write_to_excel_exec_time(*, sheet_name: str, start_row: int = 7, data):
    df = pd.DataFrame({'Execution_Time(seconds)': data})
    wb = load_workbook(FILE_PATH)
    ws = wb[sheet_name]

    for index, row in df.iterrows():
        cell = 'B%d' % (index + start_row)
        ws[cell] = row[0]

    wb.save(FILE_PATH)


if __name__ == '__main__':
    # test = np.array([99, 999, 999, 9])
    # write_to_excel_wall_time(sheet_name='test_connection', data=test)
    visualize_data()

    # print(get_latency_data(with_sheet_name='set'))
    # test = np.array(get_latency_data(with_sheet_name='set')['Wall_Time(seconds)'])
    # visualize_data(latency=test)
