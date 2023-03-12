
## Study and evaluation of sharding in distributed databases

This project is an implementation of a distributed database system using sharding technique, aiming to improve performance and scalability. The implementation consists of three main components: client-env, middleware, and staight-redis-client, all implemented in Python 3.10.

### Components:

#### 1. client-env

This folder contains a client implementation that connects to the middleware and uses its API to perform operations on a Redis key-value store as a database. The client can set, get, and delete single or multiple key-value pairs from the database. The communication between the client and middleware is done using gRPC protocol, with the message format defined using Protocol Buffers.

#### 2. middleware

This folder contains the implementation of the middleware layer, which is responsible for sharding and orchestrating multiple distributed Redis key-value stores, enabling a system of distributed databases. The middleware uses a consistent hash sharding approach to partition the keys among multiple Redis database instances. The middleware provides an API that allows the client to set, get, and delete key-value pairs in the distributed database. The middleware layer communicates with the client using the gRPC protocol, while communicating with the Redis key-value stores using the Redis-py Python interface.

#### 3. staight-redis-client

This folder contains a direct implementation of a client that connects to a single Redis key-value store without using the middleware. This straightforward client implementation uses the Redis-py Python interface to communicate with the Redis key-value store for performing operations like set, get, and delete single or multiple key-value pairs from the database. 

---

### Time Profiling:

The implementation includes time profiling for each component, allowing for performance evaluation and comparison between the different implementations. The profiling is done using Python's built-in `timeit` module.

---

###  Installation:

`pip install -r requirements.txt` 

The project also requires Protocol Buffers and gRPC to be installed.

-   Protocol Buffers: `pip install protobuf` 
-   gRPC: <br>
	`pip install grpcio` <br>
	`pip install grpcio-tools` <br>