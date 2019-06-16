from easysnmp import Session, snmp_get, snmp_walk
import sys
import os
import netsnmp
from netmiko import ConnectHandler
import csv


def CSV_Writer(csvfilename,error_14,error_20):	
    with open('Check_Data.csv','a')as csvfile:
       	fieldnames = ['Ip Address', 'Oid Index','Value14','Value20']
	filewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)		
	filewriter.writeheader()
	for item in error_14:
	    for item1 in error_20:
	        if(item1.oid_index == item.oid_index):
		    filewriter.writerow({'Ip Address':ip,'Oid Index':item.oid_index,'Value14': item.value,'Value20': item1.value})
      		    break

def csv_read_to_list(reader):
    result = []
    for key in reader:
        ip = key['Ip Address']
        oi_index = key['Oid Index']
        value14 = key['Value14']
        value20 = key['Value20']
        result.append({'ip':ip,'oi_index':oi_index,'value14':value14,'value20':value20})
    return result
    
	
# reading Ip list and get snmp walk and wirte data to a csv file 		

with open('switches_IP_list.txt') as f:
     ip_list = f.read().splitlines()
f = open('Check_Data.csv','w+')
f.close()
for ip in ip_list:
    print ('*******************************************')
    print ('*  Connecting to :' + ip +'\t\t  *' )
    print ('*******************************************')
    print ('---------------------------------------------------------------')
    session = Session(hostname = ip , community ='public', version = 2)   
    error_14  = session.walk("1.3.6.1.2.1.2.2.1.14")
    error_20  = session.walk("1.3.6.1.2.1.2.2.1.20")
    CSV_Writer('',error_14,error_20)

# reading csv files and check the SNMP error 
f1 = 'datenbank.csv'
f2 = 'Check_Data.csv'

reader1 = csv.DictReader(open (f1), delimiter = ",")
reader2 = csv.DictReader(open (f2), delimiter = ",")

list1 = csv_read_to_list(reader1)
list2 = csv_read_to_list(reader2)


print ('Value\tError Status \t\tIP address\tPort')
had_an_insert = False
for entry2 in list2:
    had_a_hit = False
    for entry1 in list1: 
        if (entry1['ip'] == entry2['ip'] and entry1['oi_index'] == entry2['oi_index']):
	    had_a_hit = True 	                 
	    if (entry1['value14'] == entry2['value14'] and entry1['value20'] == entry2['value20']):
                break
	    if entry1['value14'] != entry2['value14']:
 	        if (int(entry2['value14']) < 5):
		    print ('|'+entry1['value14']+'|'+'\tNORMAAAL Error |14|\t'+ entry2['ip'] + '\t' + entry2['oi_index'])	
	        elif (int(entry2['value14']) >= 8):    
		    print ('|'+entry1['value14']+'|'+'\tCRITICAL Error |14|\t'+ entry2['ip'] + '\t' + entry2['oi_index'])
	        else:
		    print ('|'+entry2['value14']+'|'+'\tWARNING  Error |14|\t' + entry2['ip'] +'\t' + entry2['oi_index'])
	   
   	    if (entry1['value20'] != entry2['value20']):
 	        if (int(entry2['value20']) < 5):
	            print ('|'+entry1['value20']+'|'+'\tNORMAAAL Error |20|\t'+ entry2['ip'] + '\t' + entry2['oi_index'])	
	        elif (int(entry2['value20']) >= 8):    
  	            print ('|'+entry1['value20']+'|'+'\tCRITICAL Error |20|\t'+ entry2['ip'] + '\t' + entry2['oi_index'])
	        else:
		    print ('|'+entry1['value20']+'|'+'\tWARNING  Error |20|\t' + entry2['ip'] +'\t' + entry2['oi_index'])
	   

	    break
	# update Data base	
    if had_a_hit == False:
        list1.append({'ip':entry2['ip'],'oi_index':entry2['oi_index'],'value14':entry2['value14'],'value20':entry2['value20']})

#empty the file
f = open('datenbank1.csv','w+')
f.close()
#write to a file 
with open('datenbank1.csv','a') as csvfile:
    fieldnames = ['Ip Address', 'Oid Index','Value14','Value20']	
    dict_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    dict_writer.writeheader()
    for item in list1:
        dict_writer.writerow({'Ip Address':item["ip"],'Oid Index':item["oi_index"],'Value14': item["value14"],'Value20':item["value20"]})


while True:
    print ('\nEnter 1 to RESET \n''Enter 2 to EXIT ') 
    user_choice = raw_input('\n Enter your choice :')
    if user_choice == '1':
    
        ip_addr = raw_input("Enter The IP Address : ") 
        port_num = raw_input("Enter the Port Number :")
        val_ue_14 = raw_input("Enter the Error 14 Reset Value :")
        val_ue_20 = raw_input("Enter the Error 20 Reset Value :")

        for i in list1:
            if i['ip'] == ip_addr and i['oi_index'] == port_num:
	        i['value14']= val_ue_14
	        i['value20'] = val_ue_20
    elif user_choice == '2':
	print('Exiting Program ....... ')
	break
    else:
	print ('Invalid input , Exitting Program .....')
	break

with open('Reset_Error.csv','a') as csvfile:
    fieldnames = ['Ip Address', 'Oid Index','Value14','Value20']	
    dict_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    dict_writer.writeheader()
    for item in list1:
        dict_writer.writerow({'Ip Address':item["ip"],'Oid Index':item["oi_index"],'Value14': item["value14"],'Value20':item["value20"]})
