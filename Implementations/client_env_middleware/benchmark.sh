#!/bin/sh
locust -f benchmark_clients.py --users 1000 --spawn-rate 100 --run-time 5m --stop-timeout 10s