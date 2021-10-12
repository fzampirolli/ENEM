#!bin/bash
awk '{gsub("<span class=\"_ _1\"></span>1","1",$0); print $0;}' $1
