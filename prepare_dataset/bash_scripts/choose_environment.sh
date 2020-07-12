#!/usr/bin/env bash

read -p "Are you running the project locally or on cluster? enter 'L' for locally or 'C' for cluster: "  input

if [[ $input == [Ll] || $input == [cC] ]];
    then echo $input
else
    echo 'no'
fi

