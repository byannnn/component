#!/bin/bash
echo "Killing Processes:"
DBCONNECTOR_PIDS=$(pgrep -f 'TestComponent') # Get all dbconnector processes PID
if [ "${#DBCONNECTOR_PIDS}" -eq 0 ]; then
    echo "No processes found."
else
    for j in $DBCONNECTOR_PIDS
    do
        COMMAND=$(ps -p $j -o args=)
        echo "Killing $j - $COMMAND"
        kill $j
    done
fi 
