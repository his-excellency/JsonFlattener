


def subTableCreation(folderName,topFileName,pydict,Th,symbol='_',xid={'id':''}):
    '''
    Method to create all possible Tables from a JSON
    topFileName: (String) - file to be created
    pydict: The data value in the JSON
    symbol: The symbol to denote subtables
    xid: using it to have a top level ID column in subtables if necessary
    '''

    # Checks if the required file exists- if it does, opens in append mode else in 
    # write mode
    chk = os.path.isfile(folderName+topFileName+".csv")
    if(chk):
        output_file = open(folderName+topFileName+'.csv',mode='a',encoding='utf-8')
    else:
        output_file = open(folderName+topFileName+'.csv',mode='wt',encoding='utf-8')

    # A place holder for required fields
    dct={}

    # This part of the code Separates out data into dictionaries 
    # that could be written to the CSV file being created
    if(type(pydict) is dict):
        for i in pydict:
            if(type(pydict[i]) is dict):
                subTableCreation(folderName,topFileName+symbol+i, pydict[i],Th, symbol, xid)
            elif(type(pydict[i]) is list):
                for j in pydict[i]:
                    subTableCreation(folderName,topFileName+symbol+i, j,Th ,symbol, {Th+'_id':pydict[Th+'_id']})
            #else:
            dct[i]=pydict[i] if pydict[i] is not None or pydict[i] is not '' else ''
    else:
        dct[topFileName.split('_')[-1]]=pydict
    
    # This part of code includes top level ID in the subtables
    if( (Th+'_id') not in dct):
        dct[list(xid.keys())[0]]=xid[list(xid.keys())[0]]

    # Creates a Dict Writer Object
    writerexp = csv.DictWriter(output_file,delimiter='|',extrasaction='ignore',lineterminator='\n',fieldnames=sorted(list(dct.keys())),dialect='excel')
    
    # Writes header if the file is not already present
    if(not chk):
        writerexp.writeheader()
    
    # This part of the code keeps only the atomic values
    # The rest are printed out as separate subtables
    dctres={}
    for ky in dct:
        if( (type(dct[ky]) not  in [list,dict])):# and (dct[ky]!=None or dct[ky]!=[] or dct[ky]!='') ):
        	x=str(dct[ky]).encode('unicode_escape').decode() if dct[ky] is not None else ""
        	dctres[ky]=x
    # Write data to the created CSV file
    writerexp.writerow(dctres)
