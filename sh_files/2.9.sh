#!/bin/sh
find ../2.9/com/ichi2 -name '*.class' -print | fgrep -v '$' | java -jar ../ckjm_ext.jar