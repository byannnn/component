#!/bin/bash

python component.py \
    --name "TestComponent" \ 
    --listen "127.0.0.1:12000" \
    --broadcast "127.0.0.1:12001" "127.0.0.1:12002" \
    &