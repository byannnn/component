#!/bin/bash

python component.py \
    --name TestComponent \
    --listen tcp://127.0.0.1:12000 \
    --broadcast tcp://127.0.0.1:12001 tcp://127.0.0.1:12002 \
    &