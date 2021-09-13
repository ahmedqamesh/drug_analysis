import pandas as pd
import numpy as np
import os
import re
from scipy.constants.constants import pt
from termcolor import colored
from colorama import init
init()

# I will define a pdf file to include all the final plots
rootdir = os.path.dirname(os.path.abspath(__file__))

def read_excel_sheet(file = None):
    '''
    The function will return the lists as DataFrames
    
    Parameters
    ----------
    file: 'obj' string
        the file name with xls extention [includes the path] of the file under test
    
    returns
    -------
    pandas data frames of the excel sheets under test

    '''
    xls_file = pd.ExcelFile(file)
    DrugsList = pd.read_excel(xls_file, 'Drugs List')
    DrugtoActive = pd.read_excel(xls_file, 'DrugtoActive')
    ActiveIngList = pd.read_excel(xls_file, 'ActiveIngList')
    Interactions = pd.read_excel(xls_file, 'Interactions')
    return DrugsList, DrugtoActive, ActiveIngList, Interactions

def process_drug_list(opt_name = None, file = None, req_drug_name = None, req_drug_id = None): 
    #Load the data file
    DrugsList, _, _, _ = read_excel_sheet(file = file)
    # Track the drug ing
    if opt_name == "Drug Name":
        for drug in req_drug_name:
            print("Searching for Active Ingredint ID using Drug %s"%drug)
            #get drug Id
            drug_id = get_data_info(list = DrugsList,name_to_set = "Drug Name", name_to_get = "Drug ID" , info_to_set = drug)
            
            if drug_id != None:
                get_drug_info(file = file, req_name =drug_id,  drug_name = drug,drug_id = drug_id) 
            else:
                print("Drug %s Not Found"%drug)
                
    if opt_name == "Drug ID":
        for id in req_drug_id:
            print("Searching for Active Ingredint ID using Drug Id %s"%id)
            drug_name = get_data_info(list = DrugsList,DrugsList = "Drug ID", name_to_get = "Drug Name" , info_to_set = int(id))
            #drug_name = get_name_by_id(list = DrugsList, Ing_id = int(id))
            if drug_name != None:   
                get_drug_info(file= file, req_name =int(id),  drug_name = drug_name, drug_id =int(id))
            else:
                print("Drug ID %s Not Found"%id) 
    
    #detect Interactions
    detect_interactions(file = file,req_drug_name = req_drug_name, req_drug_id = req_drug_id)        
               

def get_drug_info(file = None, req_name = None, drug_name = None, drug_id = None):
    _ , DrugtoActive, ActiveIngList, _ = read_excel_sheet(file = file)
    #get Active Ing ID
    Ing_id = get_data_info(list = DrugtoActive,name_to_set = "Drug ID", name_to_get = "Active Ing ID" , info_to_set = drug_id)
    
    #get Active Ing Name
    active_ing_name = get_data_info(list = ActiveIngList,name_to_set = "Active Ing ID ", name_to_get = "Active Ing Name " , info_to_set = Ing_id)

    interaction_id , drug_int_array = detect_int_list(file = file, Active_Ing_ID_1 = int(Ing_id))
    
    return print_drug_info(drug_name, drug_id , Ing_id, active_ing_name, interaction_id, drug_int_array)


def detect_int_list(file = None, Active_Ing_ID_1 = None):
    _, _, ActiveIngList, Interactions = read_excel_sheet(file = file)
    #get Active ing Id 
    condition_interaction_id = ((Interactions["Active Ing ID 1"] == Active_Ing_ID_1))
    
    if condition_interaction_id.any() == True:
        active_id2_array = Interactions[condition_interaction_id]["Active Ing ID 2"]        
        drug_int_array = []
        for i in range(len(active_id2_array)):
            drug_int_name =  get_data_info(list = ActiveIngList,name_to_set = "Active Ing ID ", name_to_get = "Active Ing Name " , info_to_set = int(active_id2_array.iloc[i]))
            if drug_int_name != None:
                drug_int_array = np.append(drug_int_array,drug_int_name)
        interaction_id   = Interactions[condition_interaction_id]["Interaction ID"].iloc[0]
    else:
        interaction_id = None
    return interaction_id, drug_int_array


# getter Methods 
def get_data_info(list = None,name_to_set = None, name_to_get = None , info_to_set = None):
    condition_name = (list[name_to_set] == info_to_set)
    if condition_name.any() == True:   
        drug_name = list[condition_name][name_to_get].iloc[0] 
    else:
        drug_name = None
    return drug_name  

def get_risk(list = None, id1 = None, id2 =None):
    condition_name1 = list["Active Ing ID 1"] == int(id1)
    condition_name2 = list["Active Ing ID 2"] == int(id2)
    if condition_name1.any() == True and condition_name2.any() == True:   
        filter = ((condition_name1) & (condition_name2)).all()
        risk = list[condition_name1 & condition_name2]["Risk"]
    else:
        risk = None
    return risk

def print_drug_info(drug_name, drug_id, Ing_id, active_ing_name, interaction_id, drug_int_array):
    print(f'Drug Name:{drug_name}\nDrug ID:{drug_id}\nActive Ing ID:{Ing_id}\nActive Ing Name:{active_ing_name}\nInteraction Ing:{drug_int_array}')
    
    if interaction_id == None:
        print(f'Drug {drug_name} has no Interaction Risk\n.....................')     
    else: 
        print(f'.....................')

def def_drug_list(drug_req_input = None):
    pattern = re.compile("^\s+|\s*,\s*|\s+$")
    drug_req_list = [x for x in pattern.split(drug_req_input) if x]
    return drug_req_list
   
def main(file = None):
    
    while True:    
        #check the test type
        test_type = input("Please enter the search criteria [1. for Drug Name or 2. for Drug ID]:")            
        drug_req_input = input("Please enter the drugs under test[Separated by commas]:")
        if test_type == str(1):
            req_drug_name = "Drug Name"
            req_drug_id = None
             #check the number of tests          
            drug_req_list = def_drug_list(drug_req_input = drug_req_input)
            #Start the test
            process_drug_list(opt_name = req_drug_name, file = file,req_drug_name = drug_req_list, req_drug_id = req_drug_id)
                
        elif test_type == str(2):
            req_drug_name = None
            req_drug_id = "Drug ID"        
             #check the number of tests
            drug_req_list = def_drug_list(drug_req_input = drug_req_input)
            #Start the test
            process_drug_list(opt_name = req_drug_id, file = file,req_drug_name = req_drug_name, req_drug_id = drug_req_list) 
        else:
            print("The search criteria is invalid")
            
def detect_interactions(file = None, req_drug_name = None, req_drug_id = None):
    DrugsList, DrugtoActive,_, Interactions = read_excel_sheet(file = file)
    id_to_name_list = []# Holds all the corresponding names from req_drug_id
    risk = None
    if req_drug_id:
        for id in req_drug_id:
            drug_name =  get_data_info(list = DrugsList,name_to_set = "Drug ID", name_to_get = "Drug Name",info_to_set = int(id))
            if drug_name != None:   
                id_to_name_list = np.append(id_to_name_list,drug_name)
            else:
                print("Drug ID %s Not Found"%id) 
        req_drug_name = id_to_name_list   #fill the drug array with the corresponding names to the drug id                 
    
    
    req_drug_name_list = []# Holds all the possible combinations  
    for drug1 in req_drug_name:
        for drug2 in req_drug_name:
            if drug1 != drug2:
                req_drug_name_list.append([drug1, drug2])            
    
    req_drug_set = set(tuple(i) for i in req_drug_name_list)# Holds all the possible combinations as a set
    req_drug_filterd = set((a,b) if a<=b else (b,a) for a,b in req_drug_set) # Holds all the filtered set
    #loop over the filtered elements
    for pair in req_drug_filterd: #[(a,b), (c,d)]
        drug_id1 = get_data_info(list = DrugsList,name_to_set = "Drug Name", name_to_get = "Drug ID" , info_to_set = pair[0])
        drug_id2 = get_data_info(list = DrugsList,name_to_set = "Drug Name", name_to_get = "Drug ID" , info_to_set = pair[1])

        if (drug_id1 != None and  drug_id2 !=None):
            
            active_ing_id1 = get_data_info(list = DrugtoActive,name_to_set = "Drug ID", name_to_get = "Active Ing ID" , info_to_set = int(drug_id1))
            active_ing_id2 = get_data_info(list = DrugtoActive,name_to_set = "Drug ID", name_to_get = "Active Ing ID" , info_to_set = int(drug_id2))
            
            if ((active_ing_id1 != None and  active_ing_id1 !=None)):
                
                condition_interaction_id = ((Interactions["Active Ing ID 1"] == active_ing_id1))        
                if condition_interaction_id.any() == True:
                    active_id2_array = Interactions[condition_interaction_id]["Active Ing ID 2"]   
                    if active_ing_id2 in active_id2_array.values:
                        risk = get_risk(list = Interactions, id1 = active_ing_id1, id2 = active_ing_id2)
                        msg_to_print = "#######\nInteraction found between [%s and %s] with Risk %i\n######"%(pair[0], pair[1],risk)
                        print(colored(msg_to_print,"red")) 
                    else:
                        risk = None
                        msg_to_print = "#######\nNo Interaction found between [%s and %s]......\n######"%(pair[0], pair[1])
                        print(colored(msg_to_print,"green")) 
    
    return risk
                    
if __name__ == "__main__":
    file = rootdir+"/data-entry.xlsx" 
    #main(file = file)
    drug_name_array = ["Chlorothiazide","Abilify"]
    drug_id_array = ["16","11","12","13","15"] 
    process_drug_list(opt_name = "Drug Name", file = file,req_drug_name = drug_name_array, req_drug_id = None)
    
    #detect_interactions(file = file,req_drug_name = None, req_drug_id = drug_id_array)
    #detect_interactions(file = file,req_drug_name = drug_name_array, req_drug_id = None)
    
    
    