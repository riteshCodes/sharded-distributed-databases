import re
from os import path
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# Path to profiling data
TEST_REPORT_PATH = path.join(path.dirname(Path(__file__)), Path('test_reports'))


def get_file_path(*, configuration: str, client_folder: str):
    return path.join(TEST_REPORT_PATH, Path(client_folder), Path(configuration), Path('test_report_stats_history.csv'))


def save_file_to(*, client_folder: str, configuration: str):
    return path.join(TEST_REPORT_PATH, Path(client_folder), Path(configuration),
                     Path('extracted_stats.xlsx'))


def get_data(*, client_nr, configuration, header_value=0, with_columns=None, warm_up_time):
    if with_columns is None:
        with_columns = ['Timestamp', 'Requests/s', 'User Count', 'Total Average Response Time']

    report_path = get_file_path(configuration=configuration, client_folder=client_nr)

    data_frame = pd.read_csv(report_path, header=header_value,
                             usecols=with_columns).dropna()

    # Only needed for filtering 0 values
    # data_frame = data_frame.loc[(data_frame['Requests/s'] != 0) & (data_frame['User Count'] != 0)]
    data_frame = data_frame.loc[(data_frame['User Count'] != 0)]

    data_frame = data_frame.drop(data_frame.iloc[:warm_up_time].index)

    # Store extracted data
    data_frame.to_excel(save_file_to(client_folder=client_nr, configuration=configuration), index=False)

    return data_frame


def visualize_throughput(*, client_nr, configuration, warm_up_time, nth_value, results_from):
    default_timestamps = None

    for c in configuration:
        df = get_data(client_nr=client_nr, configuration=c, warm_up_time=warm_up_time)

        start_time = df['Timestamp'].values[0]
        df.loc[:, 'Timestamp'] = df['Timestamp'].apply(lambda t: t - start_time)

        # Get always nth rows from the data, example: every 5 seconds, 10 seconds etc.
        df = df[df['Timestamp'] % nth_value == 0]

        df.loc[:, 'Timestamp'] = df['Timestamp'].apply(lambda t: '{:02d}:{:02d}'.format(*divmod(t, 60)))

        stats_df = df.head(results_from)  # Get from 00:00 to 02:00
        df_timestamps = stats_df['Timestamp'].values  # x-axis values
        df_rps = stats_df['Requests/s'].values  # y-axis values

        config_mware = [val for val in re.findall(r'\d+', c)][0]
        plt.plot(df_timestamps, df_rps, label=f'M:{config_mware}')

        default_timestamps = df_timestamps

    # Base_line
    base_line = get_data(client_nr=client_nr, configuration='direct_client', warm_up_time=warm_up_time)
    # base_line = base_line.iloc[::nth_value]

    base_line = base_line[base_line['Timestamp'] % nth_value == 0]

    base_line_df = base_line.head(results_from)  # Get from 00:00 to 02:00
    df_baseline_rps = base_line_df['Requests/s'].values  # y-axis values
    # plt.plot(df_timestamps, df_baseline_rps, label='Baseline')
    plt.plot(default_timestamps, df_baseline_rps, label='Baseline')

    # Plot configurations
    plt.title('Throughput Overview [1 Client]')
    plt.xlabel(r'Elapsed Time (min:sec)')
    plt.ylabel('Requests Per Second (requests/sec)')

    # Limits ranges
    plt.ylim([0, 500])
    # plt.gca().set_ylim(top=400)

    plt.xticks(rotation=60)
    plt.tick_params(axis='x', which='major', labelsize=8)
    plt.subplots_adjust(bottom=0.15)

    plt.legend(framealpha=1, loc="upper right")
    plt.grid(True)
    plt.savefig(path.join(TEST_REPORT_PATH, Path(client_nr), 'throughput(rps).pdf'), dpi=2400)
    plt.savefig(path.join(TEST_REPORT_PATH, Path(client_nr), 'throughput(rps).svg'), dpi=2400)
    plt.show()


def visualize_response_time(*, client_nr, configuration, warm_up_time, nth_value, results_from):
    default_timestamps = None

    for c in configuration:
        df = get_data(client_nr=client_nr, configuration=c, warm_up_time=warm_up_time)

        start_time = df['Timestamp'].values[0]
        df.loc[:, 'Timestamp'] = df['Timestamp'].apply(lambda t: t - start_time)

        # Get always nth rows from the data, example: every 5 seconds, 10 seconds etc.
        df = df[df['Timestamp'] % nth_value == 0]

        df.loc[:, 'Timestamp'] = df['Timestamp'].apply(lambda t: '{:02d}:{:02d}'.format(*divmod(t, 60)))

        stats_df = df.head(results_from)  # Get from 00:00 to 02:00
        df_timestamps = stats_df['Timestamp'].values  # x-axis values
        df_response_time = stats_df['Total Average Response Time'].values  # y-axis values

        config_mware = [val for val in re.findall(r'\d+', c)][0]
        plt.plot(df_timestamps, df_response_time, label=f'M:{config_mware}')

        default_timestamps = df_timestamps

    # Base_line
    base_line = get_data(client_nr=client_nr, configuration='direct_client', warm_up_time=warm_up_time)
    # base_line = base_line.iloc[::nth_value]

    base_line = base_line[base_line['Timestamp'] % nth_value == 0]

    base_line_df = base_line.head(results_from)  # Get from 00:00 to 02:00
    df_baseline_response_time = base_line_df['Total Average Response Time'].values  # y-axis values
    # plt.plot(df_timestamps, df_baseline_rps, label='Baseline')
    plt.plot(default_timestamps, df_baseline_response_time, label='Baseline')

    # Plot configurations
    plt.title('Response Time Overview [1 Client]')
    plt.xlabel(r'Elapsed Time (min:sec)')
    plt.ylabel('Response Time Per Operation (milliseconds)')

    # Limits ranges
    plt.ylim([0, 14])
    # plt.gca().set_ylim(top=400)

    plt.xticks(rotation=60)
    plt.tick_params(axis='x', which='major', labelsize=8)
    plt.subplots_adjust(bottom=0.15)

    plt.legend(framealpha=1, loc="upper right")
    plt.grid(True)

    plt.savefig(path.join(TEST_REPORT_PATH, Path(client_nr), 'response_time.pdf'), dpi=2400)
    plt.savefig(path.join(TEST_REPORT_PATH, Path(client_nr), 'response_time.pdf'), dpi=2400)
    plt.show()


if __name__ == '__main__':
    """
    visualize_throughput(client_nr='client_stable_1',
                         configuration=['client_mware_1_db', 'client_mware_2_db',
                                        'client_mware_4_db', 'client_mware_6_db'],
                         warm_up_time=0, nth_value=5, results_from=24)
    """

    visualize_response_time(client_nr='client_stable_1',
                            configuration=['client_mware_1_db', 'client_mware_2_db',
                                           'client_mware_4_db', 'client_mware_6_db'],
                            warm_up_time=10, nth_value=5, results_from=24)
