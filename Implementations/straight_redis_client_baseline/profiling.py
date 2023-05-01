from os import path
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# Path to profiling data
FILE_PATH = path.join(path.dirname(Path(__file__)), Path('test_report'), Path('stats_history.xlsx'))
TEST_REPORT_PATH = path.join(path.dirname(Path(__file__)), Path('test_report'))


def get_data_from_excel(*, with_sheet_name: str, header_value=0,
                        with_columns=None, warm_up_time):
    if with_columns is None:
        with_columns = ['Timestamp', 'Requests/s', 'User Count', 'Total Average Response Time']
    data_frame = pd.read_excel(FILE_PATH, header=header_value, sheet_name=with_sheet_name,
                               usecols=with_columns).dropna()
    data_frame = data_frame.loc[(data_frame['Requests/s'] != 0) & (data_frame['User Count'] != 0)]
    data_frame = data_frame.drop(data_frame.iloc[:warm_up_time].index)
    data_frame.to_excel(path.join(TEST_REPORT_PATH, 'extracted_stats.xlsx'), index=False)
    return data_frame


def visualize_throughput():
    df = get_data_from_excel(with_sheet_name='stats_history', warm_up_time=10)
    df = df.iloc[::5]

    start_time = df['Timestamp'].values[0]
    df.loc[:, 'Timestamp'] = df['Timestamp'].apply(lambda t: '{:02d}:{:02d}'.format(*divmod(int(t - start_time), 60)))

    fig, axs = plt.subplots()

    stats_df = df.head(25)  # Get from 00:00 to 02:00
    df_timestamps = stats_df['Timestamp'].values  # x-axis values
    df_rps = stats_df['Requests/s'].values  # y-axis values

    plt.plot(df_timestamps, df_rps, label='Baseline')

    plt.title('Throughput Overview')
    plt.xlabel(r'Elapsed Time (min:sec)')
    plt.ylabel('Requests Per Second (requests/sec)')

    plt.xticks(rotation=60)
    plt.tick_params(axis='x', which='major', labelsize=8)
    plt.subplots_adjust(bottom=0.15)

    plt.legend(framealpha=1)
    plt.grid(True)
    plt.savefig(f'assets/throughput(rps).pdf', dpi=2400)
    plt.savefig(f'assets/throughput(rps).svg', dpi=2400)
    plt.show()


def visualize_response_time():
    df = get_data_from_excel(with_sheet_name='stats_history', warm_up_time=10)
    # df = df.iloc[::5]

    fig, axs = plt.subplots()

    # stats_df = df.head(25)  # Get from 00:00 to 02:00
    df_user_counts = df['User Count'].values  # x-axis values
    df_response_time = df['Total Average Response Time'].values  # y-axis values

    print(df_user_counts)

    plt.plot(df_user_counts, df_response_time, label='Baseline', marker='*')

    # plt.title('Average Response Time Overview')
    plt.xlabel(r'Number of clients')
    plt.ylabel('Average Response Time (ms)')

    # plt.xticks(rotation=60)
    # plt.tick_params(axis='x', which='major', labelsize=8)
    # plt.subplots_adjust(bottom=0.15)

    plt.legend(framealpha=1)
    plt.grid(True)
    plt.savefig(f'assets/response_time.pdf', dpi=2400)
    plt.savefig(f'assets/response_time.svg', dpi=2400)
    plt.show()


if __name__ == '__main__':
    # visualize_throughput()
    visualize_response_time()
