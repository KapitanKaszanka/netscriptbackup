#!/usr/bin/bash

for i in R1_192.168.10.11 R2_192.168.10.12 R3_192.168.10.13 R4_192.168.10.14
do
	rm -rf backup_configuration/$i/.git/
done
