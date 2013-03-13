#!/bin/bash


for i in *_tests.py
do
    echo "Running: $i..."
    python $i
done
