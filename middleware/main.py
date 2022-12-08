import redis


class Middy:
    site_size = 1  # default number of sites (single site)
    redis_instances = 1  # default number of redis instance

    def __init__(self, *client_id):
        self.client_id = client_id

    def connect_db(self):
        pass

    def set_site(self, *site_size):
        self.site_size = site_size


if __name__ == '__main__':
    test = Middy(0)
    print(test.client_id)
