#!/usr/bin/env bash

ps -ef | grep -E '/usr/bin/python3 /usr/local/bin/jupyterhub' | grep -v grep