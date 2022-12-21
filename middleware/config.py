import redis


class Connection:
    pools = []

    def __init__(self, *, client_id: int, port_nr: list = None, site_count: int = 1, db_id: int = 0):
        global pool
        pool = redis.ConnectionPool(host='localhost', port=port_nr, db=db_id, decode_responses=True)
        self.redis_db = redis.StrictRedis(
            connection_pool=self.pool)
        self.client_id = client_id
        self.db_id = db_id
        self.site_count = site_count
