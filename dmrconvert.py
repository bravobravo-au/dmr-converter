#!./bin/python3
"""
Copyright (c) 2020, bravobravo-au
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    1. Redistributions of source code must retain the above copyright notice, this
       list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright notice,
        this list of conditions and the following disclaimer in the documentation
        and/or other materials provided with the distribution.
    3. Neither the name of the copyright holder nor the names of its
        contributors may be used to endorse or promote products derived from
        this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


import requests
import settings
import argparse
import json
import sys

def ClearString(s):
    if s is None:
        return ''
    return str(s.encode('ascii', 'ignore').decode('ascii', 'ignore'))

def download():
	url = settings.urlscheme + '://' + settings.urlhost + settings.urlpath + settings.urlfilename
	headers = {
			'user-agent': settings.useragent
			}
	r = requests.get(url, allow_redirects=True, headers=headers)
	open(settings.localsavefilename, 'wb').write(r.content)

def testDownloadedFile( jsonFile ):
	with open( jsonFile ) as json_file:
		try:
			json.load(json_file)
		except ValueError as e:
			print ("JSON object issue: %s") % e
			sys.exit()

def process( filename ):
	with open(filename) as f:
		jsonUsers = json.load(f)	
	return jsonUsers

def filterByCountry( jsonUsers, country ):
	retData = []
	for user in jsonUsers:
		if user['country'] == country:
			retData.append( user )
	return retData

def filterByCallsignPrefix( jsonUsers, callsignPrefix ):
	retData = []
	for user in jsonUsers:
		if user['callsign'].startswith( callsignPrefix ):
			retData.append( user )
	return retData

def export( jsonUsers ):
	result = []
	count = 1

	outfile = None
	outfile = open( settings.outputfilenameprefix + settings.outputfilenamesuffix,'w')
	outfile.write('"No.","Radio ID","Callsign","Name","City","State","Country","Remarks","Call Type","Call Alert"\n')

	for user in jsonUsers:
		name=ClearString(user['fname']) + ' ' + ClearString(user['surname'])
		var = '"{count}","{radioid}","{callsign}","{name}","{city}","{state}","{country}","{remarks}","{calltype}","{callalert}"\n'.format(
				count=count,
				radioid=str(user['radio_id'])[0:7],
				callsign=ClearString(user['callsign'])[0:7],
				name=name[0:15],
				city=ClearString(user['city'])[0:14],
				state=ClearString(user['state'])[0:15],
				country=ClearString(user['country'])[0:15],
				remarks='DMR',
				calltype='Private Call',
				callalert='Ring',
				)
		outfile.write( var )
		count += 1
	if outfile:
		outfile.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Convert DMR Radio database for AnyTone CPS')
	parser.add_argument('--download', default=None, type=bool, nargs='?', help='Only download the file')
	parser.add_argument('--process', default=None, type=bool, nargs='?', help='Process the downloaded the file')
	parser.add_argument('--filterByCountry', default=None, type=str, nargs='?', help='Filter results by country name')
	parser.add_argument('--filterByCallsignPrefix', default=None, type=str, nargs='?', help='Filter results by Callsign prefix')
	parser.add_argument('--export', default=None, type=bool, nargs='?', help='Export into CSV file format')

	args = parser.parse_args()

	jsonUsers = []
	processAll = False


	'''
	If we don't pass any of the arguments to process one section then do them all in sequence
	'''
	if not args.download and not args.process and not args.export:
		processAll = True

	if args.download or processAll:
		download()
	if args.process or processAll:
		jsonUsers = process( settings.localsavefilename )
		jsonUsers = jsonUsers['users']
		if args.filterByCountry:
			jsonUsers = filterByCountry( jsonUsers, args.filterByCountry )
		if args.filterByCallsignPrefix:
			jsonUsers = filterByCallsignPrefix( jsonUsers, args.filterByCallsignPrefix )

	if (args.export and len(jsonUsers) > 0) or processAll:
		export( jsonUsers )
