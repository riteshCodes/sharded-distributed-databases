import random
import time
import json
from datetime import datetime

from locust import User, task, events
from locust.runners import LocalRunner

from main_optimized import RedisClient
import utils


def report_success(method_name, start_time):
    # response time in milliseconds
    events.request.fire(request_type='redis', name=method_name, response_time=(time.time() - start_time) * 1000,
                        response_length=0, context={}, exception=None)


def report_failure(method_name, start_time, exception):
    # response time in milliseconds
    events.request.fire(request_type='redis', name=method_name, response_time=(time.time() - start_time) * 1000,
                        response_length=0, context={}, exception=exception)


def on_quitting(environment, data, **kwargs):
    request_stats = environment.user_classes[0].user_class.request_stats
    with open("request_stats.json", "w") as outfile:
        print('HERE')
        print(request_stats.to_dict())
        json.dump(request_stats.to_dict(), outfile)


class RedisClientLoad(User):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis_client = RedisClient()
        self.mapping = utils.read_data(data_code=random.choice([1, 10, 100, 1000]))
        self.single_mapping = utils.read_data(data_code=1)
        self.multiple_mapping = utils.read_data(data_code=random.choice([10, 100, 1000]))
        # self.request_stats = RequestStats(self.environment)
        # events.request.add_listener(self.request_stats.on_request)
        # events.quitting.add_listener(on_quitting)

    @task(1)
    def get_all_task(self):
        start_time = time.time()
        # Function to test
        key_list = self.multiple_mapping.get('userID')
        try:
            response = self.redis_client.get_all(key_list=key_list)
            if isinstance(response, list):
                report_success(method_name="get_all", start_time=start_time)
            else:
                raise Exception
        except Exception as e:
            report_failure(method_name="get_all", start_time=start_time, exception=e)

    @task(1)
    def get_range_task(self):
        start_time = time.time()
        start = 0
        end = random.choice([0, 9, 99, 999])
        try:
            response = self.redis_client.get_range(start=start, end=end)
            if isinstance(response, list):
                report_success("get_range", start_time)
            else:
                raise Exception
        except Exception as e:
            report_failure("get_range", start_time, e)

    @task(1)
    def set_to_task(self):
        start_time = time.time()
        key = self.single_mapping.get('userID')[0]
        mapping = {'name': self.single_mapping.get('name')[0], 'email': self.single_mapping.get('email')[0]}
        try:
            response = self.redis_client.set_to(key=key, **mapping)
            if response == 'OK':
                report_success("set_to", start_time)
            else:
                raise Exception
        except Exception as e:
            report_failure("set_to", start_time, e)

    @task(1)
    def set_multiples_task(self):
        start_time = time.time()
        try:
            response = self.redis_client.set_multiples(key_list=self.multiple_mapping.get('userID'),
                                                       name_list=self.multiple_mapping.get('name'),
                                                       email_list=self.multiple_mapping.get('email'))
            if response == 'OK':
                report_success("set_multiples", start_time)
            else:
                raise Exception
        except Exception as e:
            report_failure("set_multiples", start_time, e)

    @task(1)
    def del_keys_task(self):
        start_time = time.time()
        key_list = self.mapping.get('userID')
        try:
            response = self.redis_client.del_keys(key_list=key_list)
            if response == 'OK':
                report_success("del_keys", start_time)
            else:
                raise Exception
        except Exception as e:
            report_failure("del_keys", start_time, e)


#  locust -f load_generator.py --users 1000 --spawn-rate 100 --run-time 5m


"""
def on_quitting(self, **kwargs):
    print(self.environment.stats.total.current_rps)
    
class RequestStats:
    def __init__(self, environment):
        # self.request_count = 0
        # self.request_timestamps = []
        self.stats_data = {}
        self.environment = environment

    def on_request(self, request_type, name, response_time, response_length, **kwargs):
        if isinstance(self.environment.runner, LocalRunner):
            self.stats_data[
                datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')] = self.environment.stats.total.current_rps

    def to_dict(self):
        # return {
        #    "request_count": self.request_count,
        #    "request_timestamps": self.request_timestamps,
        #    "rps": self.calculate_rps()
        # }
        return self.stats_data


# request_stats = RequestStats()
# events.request.add_listener(request_stats.on_request)
"""
"""
class RequestData:
    def __init__(self):
        self.data = []
        self.save_time = time.time()
        self.save_interval = 1 # Every 1 second

    def add_data(self, rps, total_rps, failures, users):
        self.data.append({
            'timestamp': int(time.time()),
            'rps': rps,
            'total_rps': total_rps,
            'failures': failures,
            'users': users
        })

#  locust -f load_generator.py --users 10 --spawn-rate 1 --run-time 5m    

request_handler = RequestData()

if __name__ == "__main__":
 
    from locust.env import Environment
    from locust.runners import LocalRunner

    env = Environment(user_classes=[RedisClientLoad], stop_timeout=60)
    env.runner = LocalRunner(env)


    def on_request(request_type, name, response_time, response_length, context, exception):
        '''
        :param request_type: Request type method used
        :param name: Path to the URL that was called (or override name if it was used in the call to the client)
        :param response_time: Time in milliseconds until exception was thrown
        :param response_length: Content-length of the response
        :param context: :ref:`User/request context <request_context>`
        :param exception: Exception instance that was thrown. None if request was successful.
       '''
        rps = env.runner.stats.total.current_rps
        total_rps = env.runner.stats.total.total_rps
        failures = env.runner.stats.total.fail_ratio
        users = env.runner.user_count

        request_handler.add_data(rps, total_rps, failures, users)


    events.request.add_listener(on_request)

    # Run the load test (set your desired parameters)
    env.runner.start(10, spawn_rate=2)
"""
