#!/usr/bin/env python3

import argparse
import os
import platform
import re
import subprocess
import time
import toml

print ("Beginning backup script\n")

##############################################################################################################################################################################################
#variable declarations

date = time.strftime('%Y-%m-%d_%T') #Date variable
start = time.time() 

##############################################################################################################################################################################################
#Argument Parsing
parser = argparse.ArgumentParser()

#verbose mode
parser.add_argument("-v","--verbose", help="increase output verbosity",action="store_true")

#config file
parser.add_argument("-c","--config",type=str)

args = parser.parse_args()

#verbose conditions
if args.verbose:
    debug = 1   #debug variable
    print("verbose mode on")
    if args.config:
        print ("<debug>","config:",os.path.abspath(args.config))
    else:
        print("\n<debug>","ERROR: no config file")
        quit()
    print ("<debug> date:",date)
else:
    debug = 0

#config conditions
if args.config:
    config_path = os.path.abspath(args.config)
else:
    print("\nERROR: no config specified")
    quit()

#check for dependencies
if (platform.python_version() <= "3.5.0"):
    print ("\nERROR: Python version",platform.python_version(),"is not 3.5+")
    quit()

ssh_check = subprocess.run(["which","ssh"],capture_output=True)
if (ssh_check.returncode != 0):
    print("\nERROR: ssh is not installed")
    quit()

rsync_check = subprocess.run(["which","rsync"],capture_output=True)
if (rsync_check.returncode != 0):
    print("\nERROR: rsync is not installed")
    quit()

##############################################################################################################################################################################################
#Config parser method
def config_parser():
    global config_path  #Global config path
    global debug        #Global debug variable
    
    if os.path.exists(config_path):
        config_file = toml.load(config_path)
        for hosts in config_file.items():
            if (debug == 1):
                print("<debug>",hosts[0]+":",hosts)
            
            #Variable stores
            #host_ip
            try:
                host_ip = hosts[1]["config"]["ip_address"]
            except:
                print("\nERROR:",hosts[0]," missing ip definition")
                quit()
            #host_port
            try: 
                host_port = hosts[1]["config"]["port"]
            except:
                host_port = "22"
            #host_user
            try:
                host_user = hosts[1]["config"]["user"]
            except:
                print("\nERROR:",hosts[0],"missing user definition")
                quit()
            #host_os
            try:
                host_os = hosts[1]["config"]["os"]
            except:
                print("\nERROR:",hosts[0],"missing os definition")
                quit()
            #host_rsync
            try:
                host_rsync = hosts[1]["config"]["rsync"]
            except:
                host_rsync = "arp"  #Default rsync flags
            #paths array check
            try:
                for paths in hosts[1]["paths"]:
                    #host_path check
                    try:
                        host_path = paths["path"]
                    except:
                        print("\nERROR: missing path defintion")
                        quit()
                    #host_dest check
                    try:
                        host_dest = paths["dest"]
                    except:
                        print("\nERROR: missing destination definition")
                        quit()
                    #host_rsync_custom check
                    try: 
                        host_rsync_custom = paths["rsync_custom"]
                    except:
                        host_rsync_custom = host_rsync
                    #exection_rsync instantiation
                    print(host_rsync_custom)
                    execution_rsync(hosts[0],host_ip,host_port,host_user,host_rsync_custom,host_os,host_path,host_dest)
            except KeyboardInterrupt:#change
                print("\nERROR: missing path or destination definitions")
                quit()
            #custom array check
            try:
                for custom in hosts[1]["custom"]:
                    #custom_cmd check
                    try: 
                        custom_cmd = custom["cmd"]
                    except:
                        print("\nERROR: missing custom cmd definition")
                        quit()
                    #custom_cmd_out check
                    try:
                        custom_cmd_out = custom["cmd_out"]
                    except:
                        print("\nERROR: missing custom cmd out definition")
                        quit()
                    #execution_custom instantiation
                    execution_custom(hosts,host_ip,host_port,host_user,host_os,host_rsync_custom,custom_cmd,custom_cmd_out)
                    #execution_custom()
            except:
                pass
    else:
        print("\nERROR: config file does not exist")
        quit()
            
##############################################################################################################################################################################################
#Execution rsync function
def execution_rsync(hosts,host_ip,host_port,host_user,host_os,host_rsync_custom,host_path,host_dest):
    global debug    #Global debug variable

    if (debug == 1):
        print("<debug>",hosts[0] + ":","rsync","-" + host_rsync_custom,"-e","ssh -p" + host_port,host_user + "@" + host_ip + ":" + host_path,host_dest) 
    subprocess.run(["rsync","-" + host_rsync_custom,"-e",'ssh -p' + host_port,host_user + "@" + host_ip + ":" + host_path,host_dest],check=True)

##############################################################################################################################################################################################
#Execution custom function
def execution_rsync(hosts,host_ip,host_port,host_user,host_os,custom_cmd,custom_cmd_out):
    global debug
    
    if(debug == 1):
        print("<debug>",hosts[0] + ":",custom_cmd,custom_cmd_out)

    subprocess.run("ssh","-p",host_port,host_user + "@" + host_ip,custom_cmd,'>',custom_cmd_out,shell=True,check=True)









##############################################################################################################################################################################################
#Instantiation of functions
config_parser()

print ("\nBackup complete in",round(time.time()-start,3),'seconds')
