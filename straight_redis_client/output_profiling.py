from os import path
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np
import pandas as pd
from openpyxl import load_workbook

# Path to profiling data
FILE_PATH = path.join(path.dirname(Path(__file__)), Path('profiling/redis_client_profiling.xlsx'))
# Set display options pandas
pd.options.display.float_format = '{:.10E}'.format


def get_data_from_excel(*, with_sheet_name: str, header_value=5,
                        with_columns=None):
    if with_columns is None:
        with_columns = ['Execution_Time(seconds)', 'Wall_Time(seconds)']
    data_frame = pd.read_excel(FILE_PATH, header=header_value, sheet_name=with_sheet_name, usecols=with_columns)
    return data_frame.dropna()


def visualize_data(*, function, sheet_name, with_columns):
    # Data configurations
    default_x_ticks = np.arange(4)
    keys_range = np.power(10, default_x_ticks)

    # Store latency data in a Pandas DataFrame
    # data = {'keys': keys_range,'latency': measurements}
    # df = pd.DataFrame(data)

    df = get_data_from_excel(with_sheet_name=sheet_name, with_columns=with_columns)

    # Plot configurations
    fig, axs = plt.subplots()
    for col in df.columns:
        plt.plot(default_x_ticks, df[col], marker='*', label=function)
    plt.xticks(default_x_ticks, keys_range)

    x_label = 'Number of key-value pairs'  # default x label
    function_label = function.split()[0].lower()
    if function_label == 'ping':
        x_label = 'Number of ping requests (string message)'

    plt.xlabel(x_label)

    formatter = ticker.ScalarFormatter(useMathText=True)  # scientific notation
    formatter.set_scientific(True)
    formatter.set_powerlimits((0, 0))
    axs.yaxis.set_major_formatter(formatter)
    plt.ylabel('Average Response Time (seconds)')  # milliseconds(ms), 1 second = 1000 milliseconds
    # plt.title(f'Total Latency: {function}')
    plt.legend(framealpha=1)
    plt.grid(True)
    plt.savefig(f'assets/{function}.svg', dpi=1200)
    plt.savefig(f'assets/{function}.pdf', dpi=1200)
    plt.show()


def visualize_data_combined_operations(*, with_columns):
    # Data configurations
    default_x_ticks = np.arange(4)
    keys_range = np.power(10, default_x_ticks)

    # Plot configurations
    fig, axs = plt.subplots()

    profiling_file = pd.ExcelFile(FILE_PATH)

    # Iterate through each worksheet
    for sheet in profiling_file.sheet_names:
        if sheet.split()[0] == 'Ping':
            continue
        df = get_data_from_excel(with_sheet_name=sheet, with_columns=with_columns)
        for col in df.columns:
            plt.plot(default_x_ticks, df[col], marker='*', label=sheet)

    plt.xticks(default_x_ticks, keys_range)

    plt.xlabel('Number of key-value pairs')
    formatter = ticker.ScalarFormatter(useMathText=True)  # scientific notation
    formatter.set_scientific(True)
    formatter.set_powerlimits((-1, 4))
    axs.yaxis.set_major_formatter(formatter)
    plt.ylabel('Average Response Time (seconds)')

    plt.title(f'Average Response Time Per Given Key-Value Pairs (Without Middleware)')
    plt.legend(framealpha=1)
    plt.grid(True)

    plt.savefig(f'assets/combined_visualization_no_middleware_{with_columns[0].split()[0]}.svg', dpi=1200)
    plt.savefig(f'assets/combined_visualization_no_middleware_{with_columns[0].split()[0]}.pdf', dpi=1200)
    plt.show()


if __name__ == '__main__':
    # visualize_data_combined_operations(with_columns=['Wall_Time_Optimized(seconds)'])   # optimized operations

    visualize_data_combined_operations(with_columns=['Response_Time_Optimized (seconds)'])
    """
     visualize_data_combined_operations(with_columns=['Response_Time (seconds)'])  # not optimized
    # Combined visualization
    visualize_data(function='Ping (String) Request', sheet_name='Ping Message', with_columns=['Wall_Time(seconds)'])
    visualize_data(function='Set Function', sheet_name='Set Function',
                   with_columns=['Wall_Time_Optimized(seconds)', 'Wall_Time(seconds)'])
    visualize_data(function='Get Function', sheet_name='Get Function',
                   with_columns=['Wall_Time_Optimized(seconds)', 'Wall_Time(seconds)'])
    visualize_data(function='Get Range Function', sheet_name='Get-Range Function',
                   with_columns=['Wall_Time_Optimized(seconds)', 'Wall_Time(seconds)'])
    visualize_data(function='Delete Function', sheet_name='Delete Function',
                   with_columns=['Wall_Time_Optimized(seconds)', 'Wall_Time(seconds)'])
   
    # Sequential operation visualization
    visualize_data(function='Ping (String) Request', sheet_name='Ping Message',
                   with_columns=['Response_Time (seconds)'])
    visualize_data(function='Set Function (Sequential)', sheet_name='Set Function',
                   with_columns=['Response_Time (seconds)'])
    visualize_data(function='Get Function (Sequential)', sheet_name='Get Function',
                   with_columns=['Response_Time (seconds)'])
    visualize_data(function='Get Range Function (Sequential)', sheet_name='Get-Range Function',
                   with_columns=['Response_Time (seconds)'])
    visualize_data(function='Delete Function (Sequential)', sheet_name='Delete Function',
                   with_columns=['Response_Time (seconds)'])
     """
    # Optimized operation visualization
    visualize_data(function='Set Function', sheet_name='Set Function',
                   with_columns=['Response_Time_Optimized (seconds)'])
    visualize_data(function='Get Function', sheet_name='Get Function',
                   with_columns=['Response_Time_Optimized (seconds)'])
    visualize_data(function='Get Range Function', sheet_name='Get-Range Function',
                   with_columns=['Response_Time_Optimized (seconds)'])
    visualize_data(function='Delete Function', sheet_name='Delete Function',
                   with_columns=['Response_Time_Optimized (seconds)'])
