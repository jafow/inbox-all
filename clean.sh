#! /usr/bin/env sh

# shell scripts for cleaning extracted data
TARGET=$1;

# 1. remove non-ascii and a few other things
perl -i.bak -pe "s/[^[:ascii:]]//g; s/>+=20//g; s/(&#39;)/'/g" $TARGET
