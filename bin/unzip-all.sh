#!/bin/bash

for z in data/Accounts_Bulk_Data-*.zip
do
	d=${z%.zip}
	echo unzip "$z" -d "$d"
done
