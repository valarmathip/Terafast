#!/bin/bash

echo "Starting httpd service"

service salt-minion start

/etc/init.d/httpd start; tail -f /var/log/httpd/access_log
