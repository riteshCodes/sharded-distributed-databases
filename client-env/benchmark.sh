#!/bin/sh
locust -f benchmark_clients.py --users 100 --spawn-rate 1 --run-time 120 --stop-timeout 10s