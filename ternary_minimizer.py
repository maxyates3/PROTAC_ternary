#script to minimize full ternary complex

import os
import collections


#first, read in ternary.pdb list 
pdb_lst = []  
pdb_file = open("pdb_list.txt" , 'r')
for line in pdb_file:
    name = line.strip()
    pdb_lst.append(name)
pdb_file.close


#next, for each terary.pdb, copy the ligand coordinates (dictionary?) into a new .pdb file
def lig_to_dictionary(ter_file):
    lig_dic = collections.OrderedDict()
    f_file = open(ter_file , "r")
    counter = 0
    for line in f_file:
        if line.startswith("HETATM"):
#            residue_name = line[17:20].strip()
#            atom_name = line[10:15].strip()
#            key = residue_name + " " + atom_name #couldn't I just do line number here instead? 
            key = counter
            val = line.rstrip('\n')
            lig_dic[key] = val
            #i+=1
            counter += 1 
        if line.startswith("ATOM"):
            pass 
    return lig_dic 

def lig_pdb_maker(ter_file,lig_dic):
    name = ter_file.strip(".pdb") + "_lig.pdb"
    f = open(name, "w")
    for value in lig_dic.values():
        f.write(value)
        f.write(os.linesep)
    f.close()
    print(name + " was succesfully created!")
    return f 

def babel_runner(ter_file):
    name = ter_file.strip(".pdb") + "_lig.pdb"
    mol2_name = name.strip(".pdb") + ".mol2"
    command = "/mnt/shared_applications/openbabel/2.4.1/bin/obabel -h -ipdb " + name + " -omol2 -O " + mol2_name 
    print("About to run: " + command)
    os.system(command)
    return 0 

def mol2_to_params(ter_file):
    #do we want the user to specify the three letter identifier to match the inputed params value earlier? I think we should!
    name = ter_file.strip(".pdb") + "_lig.mol2"
    command = "/mnt/shared_applications/Rosetta_JKlab/Rosetta/main/source/scripts/python/public/molfile_to_params_yates.py " + name + " -n TRN --clobber --no-param"
    print("About to run: " + command)
    os.system(command)
    return 0 


def insert_lig(pdb2_lig, ter_file):
    counter1 = 1
    counter2 = 1
    dic_file = pdb2_lig 
    lig2_dic = collections.OrderedDict()
    for line in dic_file:
        key = counter1
        val = line 
        lig2_dic[key] = val
        counter1 += 1
    counter1 -= 1
    lig2_dic.pop(int(counter1))
    f = open(ter_file, "r")
    mod_pdb = ter_file.strip(".pdb") + "_mod.pdb"
    ff = open(mod_pdb, 'w')
    judgement = False 
    for line in f:
        if line.startswith("ATOM"):
            judgement = True
        if line.startswith("HETATM"):
            judgement =  False
        if line.startswith("TER"):
            judgement = False 
        elif judgement:
            ff.write(line)
    f.close()
    ff.close()
    with open(mod_pdb, 'r+') as fff:
        for key in lig2_dic:
            new_line = str(lig2_dic[key])
            fff.write(new_line)
    fff.close()
    print(ter_file + " was modified?")
    return fff

def rosetta_minimizer(params, ter_file):
    #so will need to just really run an os.system cmd to minimize the mod_pdb? Maybe add in a note that tells the person to use the highest rmsd, I could have then input it?
    print("WARNING: make sure that the .PARAMS file being used is from the highest rmsd structure that was minimized!")
    mod_pdb = ter_file.strip(".pdb") + "_mod.pdb"
    cmd = "/mnt/shared_applications/Rosetta_JKlab/Rosetta/main/source/bin/minimize.default.linuxgccrelease -s " + str(mod_pdb) + " -extra_res_fa " + params + " -run:min_type lbfgs_armijo_nonmonotone -run:min_tolerance 0.001 "
    os.system(cmd)
    return 0
    
#    params = str(input("What is the name of your PARAMS file to use in minimization? (please include .PARAMS): "))

def main():
    params = "TRN.params" 
    for pdb in pdb_lst:
        orig_lig  = lig_to_dictionary(pdb)
        new_lig = lig_pdb_maker(pdb, orig_lig)
    print("Moving on to generating params")
    counter = int(1)
    for pdb in pdb_lst:
        mol2_lig = babel_runner(pdb)
        mol2_to_params(pdb)
        curdur = os.getcwd()
        path = str(curdur) + "/TRN_0001.pdb"
        print(path)
        if os.path.isfile(path):
                pass 
        else:
                continue  
        lig_file = open("TRN_0001.pdb", 'r')
        fin_pdb = insert_lig(lig_file, pdb)
        lig_file.close()
        cmd1 = "rm " + pdb.strip(".pdb") + "_lig.pdb"
        os.system(cmd1)
        rosetta_minimizer(params, pdb)
        print("Eureka! " + str(pdb) + " was successfully minimized!")
        cmd2 = "rm TRN_0001.pdb"
        os.system(cmd2)
        
main()
    

#Just extra commands that I didn't need but could come in handy later in time
#    p = subprocess.Popen(['/bin/bash', '-c', command])                                                                                                              
# p.wait()
#            cmd = "sed -e " + str(counter2) + "d " + ter_file +        " >> " + ter_file.strip(".pdb") + "_mod" + str(counter2) + ".pdb"
#            os.system(cmd)
#            pass
#        if line.startswith("HETATM"):
#            cmd2 = "sed -e " + str(counter2) + "d " + ter_file.strip(".pdb") + "_mod" + str(counter2) + ".pdb" + " >> " + ter_file.strip(".pdb") + "_mod" + str(counter2) + ".pdb"
#            os.system(cmd2)
#            counter2 += 1
#            continue
#        else:
#            pass~
