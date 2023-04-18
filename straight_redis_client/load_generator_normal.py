import random
import sys
import time

from locust import User, task

# from main_optimized import RedisClient
from optimized_operations import RedisClient
import utils


def report_success(*, env, method_name, response_time, response):
    # response time in milliseconds
    env.events.request.fire(
        request_type='direct_client',
        name=method_name,
        response_time=response_time * 1000,  # Converting to milliseconds
        response_length=sys.getsizeof(response),
        context={},
        exception=None
    )


def report_failure(*, env, method_name, response_time, exception):
    # response time in milliseconds
    env.events.request.fire(
        request_type='direct_client',
        name=method_name,
        response_time=response_time * 1000,  # Converting to milliseconds
        response_length=0,
        context={},
        exception=exception
    )


class RedisClientLoad(User):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis_client = RedisClient()
        self.large_content = utils.read_data(data_code=1000)
        self.small_content = utils.read_data(data_code=100)

    @task(1)
    def get_single_task(self):

        # Function to test
        key_list = random.sample(list(self.small_content['userID']),
                                 1)  # Get 1 random key to set/update from the content
        start_time = time.time()
        try:
            response = self.redis_client.get_all(key_list=key_list)
            total_time = time.time() - start_time
            if isinstance(response, list):
                report_success(env=self.environment, method_name="get_single", response_time=total_time,
                               response=response)
            else:
                raise Exception
        except Exception as e:
            total_time = time.time() - start_time
            report_failure(env=self.environment, method_name="get_single", response_time=total_time, exception=e)

    @task(1)
    def get_multiples_task(self):
        # Function to test
        # key_list = random.sample(list(self.large_content.keys()), 1000)  # Get 1000 random keys from the large content
        key_list = self.large_content['userID']
        start_time = time.time()
        try:
            response = self.redis_client.get_all(key_list=key_list)
            total_time = time.time() - start_time
            if isinstance(response, list):

                report_success(env=self.environment, method_name="get_multiples", response_time=total_time,
                               response=response)
            else:
                raise Exception
        except Exception as e:
            total_time = time.time() - start_time
            report_failure(env=self.environment, method_name="get_multiples", response_time=total_time, exception=e)

    @task(1)
    def get_range_task(self):

        start = random.randint(0, 999)
        end = start + 100  # range of 100 keys

        # Function to test
        start_time = time.time()
        try:
            response = self.redis_client.get_range(start=start, end=end)
            total_time = time.time() - start_time
            if isinstance(response, list):
                report_success(env=self.environment, method_name="get_range", response_time=total_time,
                               response=response)
            else:
                raise Exception
        except Exception as e:
            total_time = time.time() - start_time
            report_failure(env=self.environment, method_name="get_range", response_time=total_time, exception=e)

    @task(1)
    def set_single_task(self):
        # Function to test
        key = random.randint(0, 999)  # Random key-generation
        mapping = {'name': 'single_test', 'email': 'single_test'}
        start_time = time.time()
        try:
            response = self.redis_client.set_to(key=key, mapping=mapping)
            total_time = time.time() - start_time
            if response == 'OK':

                report_success(env=self.environment, method_name="set_single", response_time=total_time,
                               response=response)
            else:
                raise Exception
        except Exception as e:
            total_time = time.time() - start_time
            report_failure(env=self.environment, method_name="set_single", response_time=total_time, exception=e)

    @task(2)
    def set_multiples_task(self):
        start_time = time.time()

        # Function to test
        try:
            # response = self.redis_client.set_multiples(content=self.large_content)
            response = self.redis_client.set_multiples(key_list=self.large_content['userID'],
                                                       name_list=self.large_content['name'],
                                                       email_list=self.large_content['email'])
            total_time = time.time() - start_time
            if response == 'OK':
                report_success(env=self.environment, method_name="set_multiples", response_time=total_time,
                               response=response)
            else:
                raise Exception
        except Exception as e:
            total_time = time.time() - start_time
            report_failure(env=self.environment, method_name="set_multiples", response_time=total_time, exception=e)

    @task(1)
    def del_multiples_task(self):

        # Function to test
        key_list = random.sample(range(0, 999), 100)  # Generate 100 random keys
        start_time = time.time()
        try:
            response = self.redis_client.del_keys(key_list=key_list)
            total_time = time.time() - start_time
            if response == 'OK':
                report_success(env=self.environment, method_name="del_multiples", response_time=total_time,
                               response=response)
            else:
                raise Exception
        except Exception as e:
            total_time = time.time() - start_time
            report_failure(env=self.environment, method_name="del_multiples", response_time=total_time, exception=e)

    @task(1)
    def del_single_task(self):

        # Function to test
        key_list = random.sample(range(0, 999), 1)  # Generate 1 random key
        start_time = time.time()
        try:
            response = self.redis_client.del_keys(key_list=key_list)
            total_time = time.time() - start_time
            if response == 'OK':
                report_success(env=self.environment, method_name="del_single", response_time=total_time,
                               response=response)
            else:
                raise Exception
        except Exception as e:
            total_time = time.time() - start_time
            report_failure(env=self.environment, method_name="del_single", response_time=total_time, exception=e)

#  locust -f load_generator_normal.py --csv=test_report
