#!/bin/sh
find ../2.15/com/ichi2 -name '*.class' -print | fgrep -v '$' | java -jar ../ckjm_ext.jar