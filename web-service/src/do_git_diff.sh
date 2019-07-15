#!/usr/bin/env bash
# $1 - repo $2 - begin $3 - end
cd $1
git diff $2 $3 > ../diff_file.txt
cd ..

