#flattenpyDict.py

import json
import ijson
import csv
import sys
import os
import flatdict as fd
import numpy as np
import requests
import codecs
import glob
from pandas.io.json import json_normalize as jn


dd={
	'a':1,
	'b':2,
	'c':3,
	'd':{
		'a':1,
		'b':2,
		'c':''
		},
	'e':[{
		'a':None,
		'b':2,
		'c':{
			'g':23,
			'f':34
			}
		},{
		'a':3,
		'b':'kl',
		'cNone':{}
		}],
	'f':{
		'a':12,
		'b':[1,2,3,5],
		'zz':[],
		'pp':''
	}
}


def flatten2thecore(pydct,symbol='/'):
	if(pydct=={}):return pydct
	fttn={}

	def faux(pydct,keyname=''):
		if type(pydct) is dict:
			if(pydct=={}):
				fttn[keyname]=''
			else:
				for i in pydct:
					faux(pydct[i],keyname+i+symbol)
		elif type(pydct) is list:
			if(pydct==[]):
				fttn[keyname]=''
			else:
				for i in range(len(pydct)):
					faux(pydct[i],keyname+str(i+1)+symbol)
		else:
			if(pydct=='' or pydct==None):
				fttn[keyname[:-1]]=''
			else:
				fttn[keyname[:-1]]=pydct

	faux(pydct)
	return fttn


print(sorted(flatten2thecore(dd)))

def getFileNames(dirStr):
	return glob.glob(dirStr+"*") 


def get_files_by_file_size(dirname, reverse=False):

    filepaths = []
    for basename in os.listdir(dirname):
        filename = os.path.join(dirname, basename)
        if os.path.isfile(filename):
            filepaths.append(filename)
    for i in range(len(filepaths)):
        filepaths[i] = (filepaths[i], os.path.getsize(filepaths[i]))
    filepaths.sort(key=lambda filename: filename[1], reverse=reverse)
    for i in range(len(filepaths)):
        filepaths[i] = filepaths[i][0]

    return filepaths

#This part of the code can be changed as per the requirements of the user.

Dir_Name='D:/Big Json files/'

for f in get_files_by_file_size(Dir_Name):
	print(f)
	
	csvname = f.split('/')[-1]
	csvname = csvname[:-5]

	wExp=open(csvname+'.csv',mode='wt',encoding='utf-8')
	
	with open(f,mode='r',encoding='utf-8') as order_data:
		jsnObj = ijson.items(order_data,'item')
		cnt=0
		mx=0
		for i in jsnObj:
			if(type(i) is dict):
				flaj=flatten2thecore(i)
				tmp=flaj.keys()
				if(mx<len(tmp)):
					majkeys=tmp
					mx=len(majkeys)
				print(cnt,end='\r')
				cnt+=1
		cnt=0
	
	writerexp = csv.DictWriter(wExp,lineterminator='\n',fieldnames=majkeys,dialect='excel')
	writerexp.writeheader()
	

	with open(f,mode='r',encoding='utf-8') as order_data:
		jsnObj = ijson.items(order_data,'item')

		majkeys=set(list(majkeys))
		for i in jsnObj:
			if(type(i) is dict):
				flaj=flatten2thecore(i)
				subkeys=list(flaj)
				for j in subkeys:
					if(j not in majkeys):
						flaj.pop(j,None)
				writerexp.writerow(flaj)
				print(cnt,end='\r')
			cnt+=1

	break



