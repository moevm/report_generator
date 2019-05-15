#!/usr/bin/env bash
# $1 - repo
cd $1
git branch > ../branch_test.txt
git log --oneline > ../log_file.txt
cd ..

