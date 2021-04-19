#!/bin/sh

ps aux | grep python | grep service.py | awk '{print "kill -9 "$2}' | bash

echo "drop database mb_users" | psql -U igor template1
echo "create database mb_users" | psql -U igor template1

.venv/bin/python service.py &

sleep 2

.venv/bin/python seed.py
