#!/usr/bin/env bash

read -p "Please enter a threshold value in range [0,1] (e.g. 0.6): "  input

if [[ $input == [01]\.[0-9] || $input == [01]\.[0-9] ]];
    then echo $input
else
    echo 'no'
fi