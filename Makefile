data/filelist.txt: data/filelist.html
	bin/extract-filelist.py

data/filelist.html:
	curl -L -o "$@" http://download.companieshouse.gov.uk/en_accountsdata.html
