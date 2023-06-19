#!/usr/bin/env python3

import sys

if __name__ == '__main__':
    containers_id = []
    file = open("proc_menage", "r")
    file.readline()
    for line in file :
        containers_id.append(line[:11])
    file.close()
   
    file = open("config_menage.sh","w")
    file.write("#!/bin/bash\n")
    file.write("declare -a menage_id=(")
    for line in containers_id :
        file.write('"'+line+'" ')
    file.write(")\n")
    #file.write('for i in "${menage_id[@]}"\n')
    #file.write("do\n")
    #file.write('echo $i\n')
    #file.write("done\n")

    
    file.close()