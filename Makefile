accounts.csv.zip: accounts.csv
	zip -o "$@" "$<"

accounts.csv: .input-files
	bin/extract-accounts.py > "$@" || rm "$@"

ZIPFILES=$(shell curl -L http://download.companieshouse.gov.uk/en_accountsdata.html | bin/extract-filelist.py | sed 's/^/data\//')

data/Accounts_Bulk_Data-%.zip:
	curl -L -o "$@" http://download.companieshouse.gov.uk/$(@F)

.input-files: bin/unzip-all.sh $(ZIPFILES)
	bin/unzip-all.sh && touch "$@"
