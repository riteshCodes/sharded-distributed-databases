import re
from os import path
from pathlib import Path
from datetime import datetime, timedelta


def generate_summary(*, log_path, fct_list):
    # Read the log file
    with open(log_path, 'r') as file:
        log_lines = file.readlines()

    for fct in fct_list:
        # Filter the logs for given functions
        fct_logs = [line for line in log_lines if fct in line]
        timestamps = [datetime.strptime(line.split(" - ")[0], "%d-%B-%y %H:%M:%S") for line in log_lines if fct in line]

        # Write the filtered logs to separate files
        # with open(f'{fct}.log', 'w') as log_file:
        #    log_file.writelines(fct_logs)
        """
        # Find the first and last minute
        warm_up = min(timestamps)
        start_time = max([ts for ts in timestamps if ts <= warm_up + timedelta(minutes=2)])
        end_time = max([ts for ts in timestamps if ts <= start_time + timedelta(minutes=2)])

        print('-----------------------------------------------------')
        print(f'Warming up from: {warm_up}')
        print(f'Evaluation start-time : {start_time}')
        print(f'Evaluation end-time : {end_time} \n')

        # Total runtime = 3 minutes (including warm-up time and cool-down time)
        # Total evaluation runtime = 2 Minutes
        """
        # Logs for evaluation
        # filtered_logs = [line for line, ts in zip(fct_logs, timestamps) if start_time <= ts <= end_time]

        filtered_logs = fct_logs
        total_fct_times = 0
        # Save filtered logs in a file
        with open(f'{fct}.log', 'w') as log_file:
            log_file.writelines(filtered_logs)

        # Extract the response times using a regular expression
        fct_times = [float(re.findall(r":(\d+\.\d+)", line)[0]) for line in filtered_logs]
        fct_iter = len(fct_times)
        total_fct_times = sum(fct_times)

        # Calculate the average response times in milliseconds
        avg_response_time = (total_fct_times / fct_iter) * 1000

        print(f'Average response time for {fct} function (milliseconds): {avg_response_time}')
        print(f'Total requests: {fct_iter}\n')
        print(f'Total response time for {fct} function: {total_fct_times * 1000}')
        print('-----------------------------------------------------')


def get_file_path(*, log_from, mware_config, client_load):
    return path.join(path.dirname(Path(__file__)), Path('middleware_logs'), Path(mware_config),
                     Path(client_load), Path(f'middleware_{log_from}.log'))


if __name__ == '__main__':
    """
    log_file_path = get_file_path(log_from='03-April')
    res_fct_1, fct_iter_1 = generate_summary(log_path=log_file_path, fct='set_to')

    res_fct_2, fct_iter_2 = generate_summary(log_path=log_file_path, fct='set_multiples')

    print(f'Total average response time {res_fct_1+res_fct_2}')
    print(f'Total requests {fct_iter_1+fct_iter_2}')




    log_file_path = get_file_path(log_from='03-April')
    res_fct_1, fct_iter_1 = generate_summary(log_path=log_file_path, fct='get_all')


    log_file_path = get_file_path(log_from='03-April')
    res_fct_1, fct_iter_1 = generate_summary(log_path=log_file_path, fct='get_range')

    

    log_file_path = get_file_path(log_from='08-April', mware_config='1_DB', client_load='1_Client')
    generate_summary(log_path=log_file_path,
                     fct_list=['set_to', 'set_multiples', 'del_keys', 'get_all', 'get_range'])
    
    """
    test = '09-April'
    log_file_path = get_file_path(log_from=test, mware_config='6_DB', client_load='1_Client')
    if test == '08-April':
        generate_summary(log_path=log_file_path,
                         fct_list=['set_to', 'set_multiples', 'del_keys', 'get_all', 'get_range'])
    else:
        generate_summary(log_path=log_file_path,
                         fct_list=['set_to', 'set_multiples', 'del_single', 'del_multiple', 'get_single',
                                   'get_multiple', 'get_range'])
