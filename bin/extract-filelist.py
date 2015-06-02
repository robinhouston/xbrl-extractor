#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import division

import sys
import re

for line in sys.stdin:
	mo = re.search(r"""<a href="(Accounts_Bulk_Data-\d\d\d\d-\d\d-\d\d\.zip)">""", line)
	if mo:
		print mo.group(1)
