#!/usr/bin/env bash
# $1 - repo $2 - branch $3 - begin $4 - end
cd $1
git diff $2 $3 > ../diff_file.txt
cd ..

