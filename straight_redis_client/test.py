from main import RedisClient

test = RedisClient()
# test.flush_all()
print(test.key_space_inf())