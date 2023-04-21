ALL_NODES = ["redis://:sharding-ddms@10.0.2.81:6379/0", "redis://:sharding-ddms@10.0.2.82:6379/0",
             "redis://:sharding-ddms@10.0.2.83:6379/0", "redis://:sharding-ddms@10.0.2.84:6379/0",
             "redis://:sharding-ddms@10.0.2.85:6379/0", "redis://:sharding-ddms@10.0.2.86:6379/0"]
DB_NODES = ALL_NODES[:4]
VIRTUAL_NODES = 36
# Uniform distribution of keys depends upon the number of virtual nodes (directly proportional)
# But the number of virtual nodes has also negative impact upon the response time (due to computational overhead
# of searching keys and their respective nodes
