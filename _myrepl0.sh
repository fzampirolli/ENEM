#!bin/bash
awk '{gsub("<span class=\"_ _0\"></span>1","1",$0); print $0;}' $1
