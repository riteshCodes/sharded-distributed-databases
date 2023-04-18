import re
from os import path
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Path to profiling data
TEST_REPORT_PATH = path.join(path.dirname(Path(__file__)), Path('test_reports'))


def get_file_path(*, configuration: str, client_folder: str):
    return path.join(TEST_REPORT_PATH, Path(client_folder), Path(configuration), Path('test_report_stats_history.csv'))


def save_file_to(*, client_folder: str, configuration: str):
    return path.join(TEST_REPORT_PATH, Path(client_folder), Path(configuration),
                     Path('extracted_stats.xlsx'))


def saver(configuration):
    if configuration == 'direct_client':
        report_path = path.join(TEST_REPORT_PATH, Path('throughput/Increasing_Clients/direct_client/'),
                                Path('extracted_stats.xlsx'))
    else:
        report_path = path.join(TEST_REPORT_PATH, Path('throughput/Increasing_Clients/client-env/'),
                                Path(configuration),
                                Path('extracted_stats.xlsx'))
    return report_path


def vis_path(eval_type):
    return path.join(TEST_REPORT_PATH, Path('Visualization'), Path(eval_type))


def workload_path(*, configuration):
    """
    Path containing workload with User Counts (Clients), Average Response Time and Average Throughput
    :param configuration: for middleware
    :return:
    """
    if configuration == 'direct_client':
        report_path = path.join(TEST_REPORT_PATH, Path('throughput/Increasing_Clients/direct_client/'),
                                Path('workload.xlsx'))
    else:
        report_path = path.join(path.dirname(Path(__file__)), Path('response_time_increasing_clients/'),
                                Path(configuration),
                                Path('aggregated_workload.xlsx'))
    return report_path


def get_data(*, eval_type, client_nr, configuration, header_value=0, with_columns=None, warm_up_time):
    if with_columns is None:
        with_columns = ['Timestamp', 'Requests/s', 'User Count', 'Total Average Response Time']

    # report_path = get_file_path(configuration=configuration, client_folder=client_nr)

    if configuration == 'direct_client':
        report_path = path.join(TEST_REPORT_PATH, Path('throughput'), Path(eval_type), Path(client_nr),
                                Path('direct_client'),
                                Path('test_report_stats_history.csv'))
    else:
        report_path = path.join(TEST_REPORT_PATH, Path('throughput'), Path(eval_type), Path(client_nr),
                                Path('client-env'),
                                Path(configuration), Path('test_report_stats_history.csv'))

    data_frame = pd.read_csv(report_path, header=header_value,
                             usecols=with_columns).dropna()

    # Only needed for filtering 0 values
    # data_frame = data_frame.loc[(data_frame['Requests/s'] != 0) & (data_frame['User Count'] != 0)]
    data_frame = data_frame.loc[(data_frame['User Count'] != 0)]

    data_frame = data_frame.drop(data_frame.iloc[:warm_up_time].index)

    # Store extracted data
    # data_frame.to_excel(save_file_to(client_folder=client_nr, configuration=configuration), index=False)
    # data_frame.to_excel(saver(configuration), index=False)
    # data_frame.to_excel(saver(configuration=configuration), index=False)

    return data_frame


def get_data_client_load(*, configuration, header_value=0, with_columns=None):
    if with_columns is None:
        with_columns = ['Requests/s', 'User Count', 'Total Average Response Time']

    if configuration == 'direct_client':
        report_path = path.join(TEST_REPORT_PATH, Path('throughput'),
                                Path('Increasing_Clients/direct_client'),
                                Path('test_report_stats_history.csv'))

    else:
        report_path = path.join(TEST_REPORT_PATH, Path('throughput/Increasing_Clients'),
                                Path('client-env'),
                                Path(configuration), Path('test_report_stats_history.csv'))

    data_frame = pd.read_csv(report_path, header=header_value,
                             usecols=with_columns).dropna()

    data_frame = data_frame.loc[(data_frame['User Count'] != 0)]

    # result = data_frame.groupby('User Count')['Requests/s'].mean().reset_index()

    result = data_frame.groupby('User Count')[['Requests/s', 'Total Average Response Time']].mean().reset_index()

    result.to_excel(workload_path(configuration=configuration), index=False)

    return result


def throughput_client_load(mware_configurations):
    df_baseline = get_data_client_load(configuration='direct_client')
    client_load = df_baseline['User Count'].values  # default x-axis values

    # Baseline plot
    df_baseline_rps = df_baseline['Requests/s'].values  # y-axis values
    plt.plot(client_load, df_baseline_rps, label='Baseline')

    # Middleware configurations and plot
    for c in mware_configurations:
        df = get_data_client_load(configuration=c)

        df_rps = df['Requests/s'].values  # y-axis values
        config_mware = [val for val in re.findall(r'\d+', c)][0]
        plt.plot(client_load, df_rps, label=f'M:{config_mware}')

    plt.xlabel(r'Number of Clients (Concurrent Client Load)')
    plt.ylabel('Average Requests Per Second (requests/sec)')

    plt.legend(framealpha=1, bbox_to_anchor=(1, 1), loc="upper left")
    plt.grid(True)

    plt.savefig(path.join(vis_path(eval_type='Throughput'), f'throughput(rps).pdf'), dpi=2400, bbox_inches="tight")
    plt.savefig(path.join(vis_path(eval_type='Throughput'), f'throughput(rps).svg'), dpi=2400, bbox_inches="tight")
    plt.show()


def response_time_load(mware_configurations=None, comparion=False):
    """

    df_baseline = pd.read_excel(workload_path(configuration='direct_client'), header=0, usecols=with_columns).dropna()

    client_load = df_baseline['User Count'].values  # default x-axis values
    # Baseline plot
    df_baseline_rps = df_baseline['Total Average Response Time'].values  # y-axis values
    plt.plot(client_load, df_baseline_rps, label='Baseline')
    """
    with_columns = ['Requests/s', 'User Count', 'Total Average Response Time']

    baseline_path = path.join(path.dirname(Path(__file__)), Path('response_time_increasing_clients'),
                              Path('direct_client'))
    df_baseline = pd.read_csv(path.join(baseline_path, Path('test_report_stats_history.csv')), header=0,
                              usecols=with_columns).dropna()

    # df_baseline = pd.read_csv(path.join(baseline_path, Path('aggregated_workload.csv')), header=0,usecols=with_columns).dropna()

    df_baseline = df_baseline.loc[(df_baseline['User Count'] != 0)]
    # df = df.drop(data_frame.iloc[:warm_up_time].index)

    result = df_baseline.groupby('User Count')[['Requests/s', 'Total Average Response Time']].mean().reset_index()

    # result.to_excel(path.join(baseline_path, Path('aggregated_workload.xlsx')), index=False)

    # get first 10 rows
    result = result.head(5)

    client_load = result['User Count'].values  # default x-axis values
    # Baseline plot
    df_baseline_rt = result['Total Average Response Time'].values  # y-axis values
    plt.plot(client_load, df_baseline_rt, label='Baseline')

    # Middleware configurations and plot
    for c in mware_configurations:
        report_path = path.join(path.dirname(Path(__file__)), Path('response_time_increasing_clients'), Path(c),
                                Path('test_report_stats_history.csv'))
        df = pd.read_csv(report_path, header=0, usecols=with_columns).dropna()

        df = df.loc[(df['User Count'] != 0)]
        # df = df.drop(data_frame.iloc[:warm_up_time].index)

        result = df.groupby('User Count')[['Requests/s', 'Total Average Response Time']].mean().reset_index()

        # result.to_excel(workload_path(configuration=c), index=False)

        # get first 10 rows
        result = result.head(5)

        # df = pd.read_excel(workload_path(configuration=c), header=0, usecols=with_columns).dropna()
        # client_load = result['User Count'].values  # default x-axis values
        df_avg_rt = result['Total Average Response Time'].values  # y-axis values
        config_mware = [val for val in re.findall(r'\d+', c)][0]
        plt.plot(client_load, df_avg_rt, label=f'M:{config_mware}')

    # Plot configurations
    plt.xlabel(r'Number of Clients (Concurrent Client Load)')
    plt.ylabel('Average Response Time (ms)')
    plt.legend(framealpha=1, bbox_to_anchor=(1, 1), loc="upper left")
    plt.grid(True)

    ax = plt.gca()
    yticks = np.arange(0, 450, 50)
    ax.set_yticks(yticks)

    plt.savefig(path.join(vis_path(eval_type='Response_Time_Combined'), f'avg_response_time_zoomed_5.pdf'), dpi=2400,
                bbox_inches="tight")
    plt.savefig(path.join(vis_path(eval_type='Response_Time_Combined'), f'avg_response_time_zoomed_5.svg'), dpi=2400,
                bbox_inches="tight")
    plt.show()


def visualize_throughput(*, eval_type, client_nr, configuration, warm_up_time, nth_value, results_from):
    default_timestamps = None

    for c in configuration:
        df = get_data(eval_type=eval_type, client_nr=client_nr, configuration=c, warm_up_time=warm_up_time)

        start_time = df['Timestamp'].values[0]
        df.loc[:, 'Timestamp'] = df['Timestamp'].apply(lambda t: t - start_time)

        # Get always nth rows from the data, example: every 5 seconds, 10 seconds etc.
        # df = df.iloc[::nth_value]
        df = df[df['Timestamp'] % nth_value == 0]

        # df.loc[:, 'Timestamp'] = df['Timestamp'].apply(lambda t: '{:02d}:{:02d}'.format(*divmod(t, 60)))

        stats_df = df.head(results_from)  # Get from 00:00 to 02:00
        # df_timestamps = stats_df['Timestamp'].values  # x-axis values
        df_timestamps = ['{:02d}:{:02d}'.format(*divmod(t, 60)) for t in range(0, 61, 5)]

        df_rps = stats_df['Requests/s'].values  # y-axis values

        config_mware = [val for val in re.findall(r'\d+', c)][0]

        """
        if config_mware == '4':
            df_timestamps = df_timestamps[:-1]
            df_rps = df_rps[:-1]
        """
        plt.plot(df_timestamps, df_rps, label=f'M:{config_mware}')

        default_timestamps = df_timestamps

    # Base_line
    base_line = get_data(eval_type=eval_type, client_nr=client_nr, configuration='direct_client',
                         warm_up_time=warm_up_time)
    # base_line = base_line.iloc[::nth_value]

    # base_line = base_line.iloc[::nth_value]
    base_line = base_line[base_line['Timestamp'] % nth_value == 0]

    base_line_df = base_line.head(results_from)  # Get from 00:00 to 02:00
    df_baseline_rps = base_line_df['Requests/s'].values  # y-axis values
    # plt.plot(df_timestamps, df_baseline_rps, label='Baseline')
    plt.plot(default_timestamps, df_baseline_rps, label='Baseline')

    # Plot configurations

    # plt.title('Average Throughput Overview')
    plt.xlabel(r'Elapsed Time (min:sec)')
    plt.ylabel('Requests Per Second (requests/sec)')

    # Limits ranges
    # plt.ylim([0, 500])
    # plt.gca().set_ylim(top=400)

    plt.xticks(rotation=60)
    plt.tick_params(axis='x', which='major')  # 8 default
    plt.subplots_adjust(bottom=0.18)
    plt.legend(framealpha=1, bbox_to_anchor=(1, 1), loc="upper left")
    plt.grid(True)

    plt.savefig(path.join(TEST_REPORT_PATH, f'throughput(rps)_{client_nr}.pdf'), dpi=2400, bbox_inches="tight")
    plt.savefig(path.join(TEST_REPORT_PATH, f'throughput(rps)_{client_nr}.svg'), dpi=2400, bbox_inches="tight")
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


def set_get_evaluation(client_load='1_Client'):
    report_path_baseline = path.join(path.dirname(Path(__file__)), Path('test_reports/throughput/Elapsed_Time'),
                                     Path(client_load), Path('client-env/1_DB/'),
                                     Path('aggregated.csv'))
    base_df = pd.read_csv(report_path_baseline, header=0, usecols=['Name', 'Average Response Time'])

    # df = base_df[base_df['Name'].isin(['set_single', 'set_multiples', 'get_single', 'get_multiples'])]

    df = base_df[base_df['Name'].isin(
        ['/CommunicationService/setSingle', '/CommunicationService/setMultiple', '/CommunicationService/getSingle',
         '/CommunicationService/getMultiple'])]
    print(df)

    # Extract values
    set_single_value = df[df['Name'] == '/CommunicationService/setSingle']['Average Response Time'].values[0]
    get_single_value = df[df['Name'] == '/CommunicationService/getSingle']['Average Response Time'].values[0]
    set_multiple_value = df[df['Name'] == '/CommunicationService/setMultiple']['Average Response Time'].values[0]
    get_multiple_value = df[df['Name'] == '/CommunicationService/getMultiple']['Average Response Time'].values[0]

    operations = ('set', 'get')
    data = {
        'single key-value pair': (round(set_single_value, 4), round(get_single_value, 4)),
        'multiple key-value pairs': (round(set_multiple_value, 4), round(get_multiple_value, 4))
    }

    x = np.arange(len(operations))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots()

    for attribute, measurement in data.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average Response Time (ms)')
    ax.set_xlabel('Operations')
    ax.set_xticks(x + width, operations)

    ax = plt.gca()
    yticks = np.arange(0, 75, 5)
    ax.set_yticks(yticks)
    ax.legend()

    plt.savefig(path.join(TEST_REPORT_PATH, 'set_get_1_Client_M-1.pdf'), dpi=2400)
    plt.savefig(path.join(TEST_REPORT_PATH, 'set_get_1_Client_M-1.svg'), dpi=2400)

    plt.show()


def set_get_evaluation_baseline(client_load='1_Client'):
    report_path_baseline = path.join(path.dirname(Path(__file__)), Path('test_reports/throughput/Elapsed_Time'),
                                     Path(client_load), Path('direct_client'),
                                     Path('aggregated.csv'))
    base_df = pd.read_csv(report_path_baseline, header=0, usecols=['Name', 'Average Response Time'])

    single_df = base_df[base_df['Name'].isin(['set_single', 'get_single'])]

    multiples_df = base_df[base_df['Name'].isin(['set_multiples', 'get_multiples'])]

    print(single_df.values)
    print(multiples_df.values)

    single_get_set = [7.7534715334574384, 1.748488499568059]
    multiple_get_set = [5248.124063014984, 6683.577720935528] # get, set

    # Create the figure and subplots
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

    ax1.bar(['get_single', 'set_single'], single_get_set, label='single key-value pair', width = 0.4, color='C0')
    ax1.legend()

    ax2.bar(['get_multiples', 'set_multiples'], multiple_get_set, label='multiple key-value pairs', width = 0.4, color= 'C1')
    ax2.legend(loc="upper right")


    ax1.set(ylabel='Average Response Time Per Operation (milliseconds)')


    plt.tight_layout()


    plt.savefig(path.join(TEST_REPORT_PATH, 'get_set.pdf'), dpi=2400)
    plt.savefig(path.join(TEST_REPORT_PATH, 'get_set.svg'), dpi=2400)

    plt.show()


"""
    print(df)

    grouped_df = df.copy()
    grouped_df['Group'] = df['Name'].str[:3]

    grouped_data = grouped_df.groupby('Group')

    for key, item in grouped_data:
        print(grouped_data.get_group(key), "\n\n")


    # Create a bar plot
    fig, ax = plt.subplots()

    # Set bar width and positions
    bar_width = 0.35
    positions = [0, 1]
    x_labels = ['set', 'get']

    # Plot bars for each group
    for index, (group, group_data) in enumerate(grouped_data):
        ax.bar([p + index * bar_width for p in positions], group_data['Average Response Time'], width=bar_width,
               label=group)

    # Set labels, title, and legend
    ax.set_xticks([p + bar_width / 2 for p in positions])
    ax.set_xticklabels(x_labels)
    ax.set_xlabel('Operation Type')
    ax.set_ylabel('Average Response Time')
    ax.set_title('Average Response Time (Set/Get) 1 Client')
    ax.legend(df['Name'])

    # Show the plot
    plt.show()
"""

if __name__ == '__main__':
    """
    visualize_throughput(client_nr='client_stable_1',
                         configuration=['client_mware_1_db', 'client_mware_2_db',
                                        'client_mware_4_db', 'client_mware_6_db'],
                         warm_up_time=0, nth_value=5, results_from=24)
    

    visualize_response_time(client_nr='client_stable_1',
                            configuration=['client_mware_1_db', 'client_mware_2_db',
                                           'client_mware_4_db', 'client_mware_6_db'],
                            warm_up_time=10, nth_value=5, results_from=24)
    
    visualize_throughput(client_nr='100_Client',
                         configuration=['1_DB', '2_DB', '4_DB', '6_DB'],
                         warm_up_time=10, nth_value=5, results_from=13)
    
    visualize_throughput_client_load(mware_configurations=['1_DB', '2_DB', '4_DB', '6_DB'])
 
    response_time_load(mware_configurations=['1_DB', '2_DB', '4_DB', '6_DB'])

    
    visualize_throughput(eval_type='Elapsed_Time', client_nr='1_Client',
                         configuration=['1_DB', '2_DB', '4_DB', '6_DB'],
                         warm_up_time=10, nth_value=5, results_from=13)
    """

    # set_get_evaluation()
    set_get_evaluation_baseline()
