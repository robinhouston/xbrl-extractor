daily_csv_files=$(shell curl -L http://download.companieshouse.gov.uk/en_accountsdata.html | bin/extract-filelist.py | sed 's/^/data\//; s/\.zip$$/.csv/')

monthly_csv_files=$(shell curl -L http://download.companieshouse.gov.uk/en_monthlyaccountsdata.html | bin/extract-filelist.py | sed 's/^/data\//; s/\.zip$$/.csv/')

accounts.csv.zip: accounts.csv
	zip -o "$@" "$<"

accounts.csv: $(daily_csv_files) $(monthly_csv_files)
	( head -1 "$<" ; echo $^ | xargs -n 1 tail +2 ) > "$@"

data/Accounts_Bulk_Data-%.zip:
	curl -L -o "$@" http://download.companieshouse.gov.uk/$(@F)

data/Accounts_Monthly_Data-%.zip:
	curl -L -o "$@" http://download.companieshouse.gov.uk/$(@F)

data/Accounts_Bulk_Data-%.csv: data/Accounts_Bulk_Data-% bin/extract-accounts.py
	bin/extract-accounts.py "$<" > "$@"

data/Accounts_Monthly_Data-%.csv: data/Accounts_Bulk_Data-% bin/extract-accounts.py
	bin/extract-accounts.py "$<" > "$@"

data/Accounts_Bulk_Data-%: data/Accounts_Bulk_Data-%.zip
	unzip -o "$@" "$<"

# For debugging. E.g. `make print-daily_csv_files`
print-%:
	@echo '$*=$($*)'
