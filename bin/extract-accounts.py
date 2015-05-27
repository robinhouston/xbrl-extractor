#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import division

import csv
import os
import re
import sys

from xml.etree import cElementTree

NS_MAP = "xmlns:map"

w = csv.writer(sys.stdout)

def parse_nsmap(file):
	events = "start", "start-ns", "end-ns"

	root = None
	ns_map = []

	for event, elem in cElementTree.iterparse(file, events):
		if event == "start-ns":
			prefix, url = elem
			ns_map.append((url, prefix))
		elif event == "end-ns":
			ns_map.pop()
		elif event == "start":
			if root is None:
				root = elem
			elem.set(NS_MAP, dict(ns_map))

	return cElementTree.ElementTree(root)

def get_element_text(element):
	text = element.text or ""
	for e in element:
		text += get_element_text(e) + " "
	text += (element.tail or "")
	return text.strip()

def extract_accounts(filepath, filetype):
	if filetype == "html":
		return extract_accounts_inline(filepath)
	elif filetype == "xml":
		return extract_accounts_xml(filepath)
	else:
		raise Exception("Unknown filetype: " + filetype)

def extract_accounts_inline(filepath):
	print >>sys.stderr, "Loading {}...".format(filepath)
	
	name = None
	x = parse_nsmap(filepath)
	for e in x.findall("//{http://www.xbrl.org/2008/inlineXBRL}nonNumeric"):
		prefix = e.get("xmlns:map")["http://www.xbrl.org/uk/cd/business/2009-09-01"]
		print >>sys.stderr, e.get("name"), prefix
		if e.get("name") == prefix + ":EntityCurrentLegalOrRegisteredName":
			name = get_element_text(e)
	return [ name ]

def extract_accounts_xml(filepath):
	print >>sys.stderr, "Loading {}...".format(filepath)
	x = cElementTree.parse(filepath)
	name = x.find("//{http://www.xbrl.org/uk/fr/gcd/2004-12-01}EntityCurrentLegalName").text
	return [ name ]

def process(path):
	filename = os.path.basename(path)
	mo = re.match("^(Prod\d+_\d+)_([^_]+)_(\d\d\d\d\d\d\d\d)\.(html|xml)", filename)
	run_code, company, date, filetype = mo.groups()
	accounts = extract_accounts(path, filetype)
	w.writerow([company, date] + accounts)

if len(sys.argv) > 1:
	for f in sys.argv[1:]:
		process(f)
else:
	for x in os.listdir("data"):
		d = os.path.join("data", x)
		if not os.path.isdir(d): continue
		for f in os.listdir(d):
			p = os.path.join(d, f)
			process(p)

