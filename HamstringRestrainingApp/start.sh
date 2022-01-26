#!/bin/bash

python3 -u /code/transactionserver.py &
gunicorn -b 0.0.0.0:5000 wsgi:app &

# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?