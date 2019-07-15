#!/usr/bin/env bash
# $1 - repo
cd $1
git log --oneline > ../log_file.txt
cd ..

