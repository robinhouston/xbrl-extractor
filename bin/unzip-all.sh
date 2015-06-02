#!/bin/bash

for z in data/Accounts_Bulk_Data-*.zip
do
	d=${z%.zip}
	if [ ! -e "$d" ]
	then
		unzip -o "$z" -d "$d"
	fi
done
