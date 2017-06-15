#!/usr/bin/python

import os

brands={
	87 : 'phonak',
	88 : 'beltone',
	89 : 'widex',
	90 : 'siemens',
	91 : 'rexton',
	92 : 'sonic_innovations',
	93 : 'bernafon',
	94 : 'hansaton',
	95 : 'oticon',
	96 : 'unitron',
	97 : 'sona',
	98 : 'resound',
	99 : 'starkey',
# a ajouter
	100 : 'newson',
	101: 'audio_service',
	102: 'biotone',
	103: 'interton',
	104: 'audiologys'
}

brands2id = {v: k for k, v in brands.iteritems()}
#print(brands2id)

marques={}
with open('marques-gen-completed2.csv', 'r') as csv:
	for l in csv:
		l.strip()
		d=l.split(';')
		marques[d[0]] = d[1].lower().strip()
#LMB:marque	
	
postid_lmblib={}
with open('wpid-lmb.csv', 'r') as csv:
        for l in csv:
                l.strip()
                d=l.split(';')
                postid_lmblib[d[0]] = d[1].strip()
# postid : LMB
lmblib_postid = {v: k for k, v in postid_lmblib.iteritems()}

#with open('data.txt','r') as f:
#	for line in f:
#	#line='A-0000-0001234;siemens;1756'
#		line = line.strip()
#		d = line.split(';')
#		brand_id=brands2id[d[1]]
#		post_id=d[2]


for k,m in marques.iteritems():
	lib = k
	marque = m
	post_id = lmblib_postid[lib]
	brand_id = brands2id[marque]

	i=1
	if i == 1:	
		os.system("curl -u brand:brand175 -X PUT https://woo2.audiologys.com/wp-json/wc/v1/products/123?consumer_key=ck_1df2a57e1546585739bb65d77361936aa7a0e5ee\&consumer_secret=cs_51d052851e2428d1243ad76ae834ced8032779c3 -H 'Content-Type: application/json'  -d '{\"id\": \"" + str(post_id) +"\", \"brands\": [" + str(brand_id) + "]}'")
		i+=1

