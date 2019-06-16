import csv
import sys


def csv_read_to_list(reader):
    result = []
    for key in reader:
        ip = key['Ip Address']
        oi_index = key['Oid Index']
        value14 = key['Value14']
        value20 = key['Value20']
        result.append({'ip':ip,'oi_index':oi_index,'value14':value14,'value20':value20})
    return result




#with open('datenbank.csv','r') as csvfile:
#	f1 = csvfile.readlines()
 
    #reader  = csv.DictReader(csvfile, delimiter =',')
    # reader1 = csv.DictReader(csvfile1)
f1 = 'datenbank.csv'
f2 = 'Check_Data.csv'
reader1 = csv.DictReader(open (f1), delimiter = ",")
#reader1 = f1.readlines()
reader2 = csv.DictReader(open (f2), delimiter = ",")

list1 = csv_read_to_list(reader1)
list2 = csv_read_to_list(reader2)


print ('Value\tError Status \t\tIP address\tPort')
for entry1 in list1:
    for entry2 in list2: 
        if (entry1['ip'] == entry2['ip'] and entry1['oi_index'] == entry2['oi_index']):                  
	    if (entry1['value14'] == entry2['value14'] and entry1['value20'] == entry2['value20']):
                break
	    if entry1['value14'] != entry2['value14']:
 	        if (int(entry2['value14']) < 5):
		    print ('|'+entry2['value14']+'|'+'\tNORMAAAL Error |14|\t'+ entry2['ip'] + '\t' + entry2['oi_index'])	
	        elif (int(entry2['value14']) >= 8):    
		    print ('|'+entry2['value14']+'|'+'\tCRITICAL Error |14|\t'+ entry2['ip'] + '\t' + entry2['oi_index'])
	        else:
		    print ('|'+entry2['value14']+'|'+'\tWARNING  Error |14|\t' + entry2['ip'] +'\t' + entry2['oi_index'])
	    else: 
		break
   	    if (entry1['value20'] != entry2['value20']):
 	        if (int(entry2['value20']) < 5):
	            print ('|'+entry2['value20']+'|'+'\tNORMAAAL Error |20|\t'+ entry2['ip'] + '\t' + entry2['oi_index'])	
	        elif (int(entry2['value20']) >= 8):    
  	            print ('|'+entry2['value20']+'|'+'\tCRITICAL Error |20|\t'+ entry2['ip'] + '\t' + entry2['oi_index'])
	        else:
		    print ('|'+entry2['value20']+'|'+'\tWARNING  Error |20|\t' + entry2['ip'] +'\t' + entry2['oi_index'])
	    else: 
		break 

