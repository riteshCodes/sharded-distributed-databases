import re
from os import path
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
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

    if configuration == 'direct_client':
        data_frame.to_excel(path.join(TEST_REPORT_PATH, Path('throughput'), Path(eval_type), Path(client_nr),
                                      Path('direct_client\extracted_stats.xlsx')), index=False)

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
    client_load = df_baseline['User Count'].head(10).values  # default x-axis values

    # Baseline plot
    df_baseline_rps = df_baseline['Requests/s'].head(10).values  # y-axis values
    plt.plot(client_load, df_baseline_rps, label='Baseline')

    # Middleware configurations and plot
    for c in mware_configurations:
        df = get_data_client_load(configuration=c)

        df_rps = df['Requests/s'].head(10).values  # y-axis values
        config_mware = [val for val in re.findall(r'\d+', c)][0]
        plt.plot(client_load, df_rps, label=f'M:{config_mware}')

    plt.axhline(y=80, color='brown', label='Maximum requests/sec (Middleware)')
    plt.axhline(y=152, color='gold', label='Maximum requests/sec (Baseline)')

    plt.xlabel(r'Number of Clients (Concurrent Client Load)')
    plt.ylabel('Average Requests Per Second (requests/sec)')

    ax = plt.gca()
    yticks = np.arange(0, 180, 20)
    ax.set_yticks(yticks)

    xticks = np.arange(0, 11, 1)
    ax.set_xticks(xticks)

    plt.legend(framealpha=1, bbox_to_anchor=(1, 1), loc="upper left")
    plt.grid(True)

    plt.savefig(path.join(vis_path(eval_type='Throughput'), f'throughput(rps)_10.pdf'), dpi=2400, bbox_inches="tight")
    plt.savefig(path.join(vis_path(eval_type='Throughput'), f'throughput(rps)_10.svg'), dpi=2400, bbox_inches="tight")
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

    result.to_excel(path.join(baseline_path, Path('aggregated_workload.xlsx')), index=False)

    # get first 10 rows
    result = result.head(10)

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
        result = result.head(10)

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

    # ax = plt.gca()
    # yticks = np.arange(0, 450, 50)
    # ax.set_yticks(yticks)
    ax = plt.gca()
    yticks = np.arange(0, 80, 10)
    ax.set_yticks(yticks)
    xticks = np.arange(0, 11, 1)
    ax.set_xticks(xticks)

    plt.savefig(path.join(vis_path(eval_type='Response_Time_Combined'), f'avg_response_time_NEW_10.pdf'), dpi=2400,
                bbox_inches="tight")
    plt.savefig(path.join(vis_path(eval_type='Response_Time_Combined'), f'avg_response_time_NEW_10.svg'), dpi=2400,
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

        plt.plot(df_timestamps, df_rps, label=f'M:{config_mware}')

        default_timestamps = df_timestamps

    # Base_line
    base_line = get_data(eval_type=eval_type, client_nr=client_nr, configuration='direct_client',
                         warm_up_time=warm_up_time)
    # base_line = base_line.iloc[::nth_value]

    # base_line = base_line.iloc[::nth_value]
    # base_line = base_line[base_line['Timestamp'] % nth_value == 0]
    base_line = base_line[base_line['Timestamp'] % 1 == 0]

    base_line_df = base_line.head(results_from)  # Get from 00:00 to 02:00
    df_baseline_rps = base_line_df['Requests/s'].values  # y-axis values
    print(len(df_baseline_rps))
    print(len(default_timestamps))
    assert len(df_baseline_rps) == len(default_timestamps)
    # plt.plot(df_timestamps, df_baseline_rps, label='Baseline')
    plt.plot(default_timestamps, df_baseline_rps, label='Baseline')

    # Plot configurations

    # plt.title('Average Throughput Overview')
    plt.xlabel(r'Elapsed Time (min:sec)')
    plt.ylabel('Requests Per Second (requests/sec)')

    # Limits ranges
    plt.ylim([0, 180])
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
        'single key-value pair': (round(set_single_value, 2), round(get_single_value, 2)),
        'multiple key-value pairs': (round(set_multiple_value, 2), round(get_multiple_value, 2))
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
    ax.set_xticks(x + width / 2, operations)

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

    df = base_df[base_df['Name'].isin(['set_single', 'set_multiples', 'get_single', 'get_multiples'])]

    grouped_df = df.copy()
    grouped_df['Group'] = df['Name'].str[:3]

    # Prepare the data for the grouped bar chart
    grouped_data = grouped_df.pivot_table(index='Group', columns='Name', values='Average Response Time')

    print(grouped_data)

    # Plot the grouped bar chart
    bar_width = 0.35

    fig, ax = plt.subplots()

    x_labels = grouped_data.index.values
    x = np.arange(len(x_labels))

    bars1 = ax.bar(x - bar_width / 2, grouped_data['get_single'], bar_width,
                   color='C0')
    bars2 = ax.bar(x + bar_width / 2, grouped_data['get_multiples'], bar_width,
                   color='C1')
    bars3 = ax.bar(x - bar_width / 2, grouped_data['set_single'], bar_width,
                   color='C0')
    bars4 = ax.bar(x + bar_width / 2, grouped_data['set_multiples'], bar_width,
                   color='C1')

    custom_labels = [Line2D([0], [0], color='C0', lw=4),
                    Line2D([0], [0], color='C1', lw=4)]
    ax.legend(custom_labels, ['Baseline: single key-value pair', 'Baseline: multiple key-value pairs'])

    # Add labels
    ax.set_xlabel('Operations')
    ax.set_ylabel('Average Response Time (ms)')
    # ax.set_title('Set-Get Operation Overview')
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels)


    ax = plt.gca()
    yticks = np.arange(0, 45, 2.5)
    ax.set_yticks(yticks)
    # ax.legend()

    autolabel(bars1, ax)
    autolabel(bars2, ax)
    autolabel(bars3, ax)
    autolabel(bars4, ax)

    plt.savefig(path.join(TEST_REPORT_PATH, 'set_get_baseline.pdf'), dpi=2400)
    plt.savefig(path.join(TEST_REPORT_PATH, 'set_get_baseline.svg'), dpi=2400)

    plt.show()


def autolabel(rects, ax):
    for rect in rects:
        height = round(rect.get_height(), 2)
        ax.annotate('{}'.format(height), xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


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
   
    visualize_throughput(eval_type='Elapsed_Time', client_nr='1_Client',
                         configuration=['1_DB', '2_DB', '4_DB', '6_DB'],
                         warm_up_time=10, nth_value=1, results_from=13)

    throughput_client_load(['1_DB', '2_DB', '4_DB', '6_DB'])
     
    visualize_throughput(eval_type='Elapsed_Time', client_nr='100_Client',
                         configuration=['1_DB', '2_DB', '4_DB', '6_DB'],
                         warm_up_time=35, nth_value=1, results_from=13)
    """
    # response_time_load(mware_configurations=['1_DB', '2_DB', '4_DB', '6_DB'])
    # set_get_evaluation()
    set_get_evaluation_baseline()
    # throughput_client_load(['1_DB', '2_DB', '4_DB', '6_DB'])
