#! /usr/bin/env sh

# shell scripts for cleaning extracted data
TARGET=$1;

# 1. remove non-ascii and a few other things
perl -i.bak -pe "s/[^[:ascii:]]//g; s/>+=20|=[0-9]+//g; s/(&#39;)/'/g" $TARGET

# 2. strip leading unicodes
sed -i $TARGET -re '/=09|=30/d' \
        -e 's/=[A-Z][0-9]//g' \
        -e '/(http)s?/d' \
        -e '/^> /d' \
        -e 's/^(<+ )//g' \
        -e 's///g' \ 
        -e '/@media|@font-face/d' \

# single line it
# tr '\n' ' ' < $TARGET > cleaned_$TARGET
