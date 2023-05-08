  
from termcolor import colored
import subprocess
import argparse
import os
import csv
import sys


ids =  {}
data =[]
PWN3rFile = "../data/PWN3r.csv"
def printLogo():
    logo = """
 ___    _       _  _   _    ___       
(  _`\ ( )  _  ( )( ) ( ) /'_  )      
| |_) )| | ( ) | || `\| |(_)_) | _ __ 
| ,__/'| | | | | || , ` | _(_ < ( '__)
| |    | (_/ \_) || |`\ |( )_) || |   
(_)    `\___x___/'(_) (_)`\____)(_)   
    """
    print(colored(logo, "green"))
    print("By EGYCCAL")
      
  
    '''  try:
        import pyfiglet
    except:         
        subprocess.run(["pip3", "install" , "pyfiglet"])

    text = "PWN3r"

    font = "puffy"

    result = pyfiglet.figlet_format(text, font=font)
    colored_result = colored(result, "green")

    print(colored_result )
    '''
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



def function_1():  
    print(colored("You chose option 1.", "yellow"))
    return


def function_2():   
    print(colored("You chose option 2.", "green"))
    return

def function_3():   
    print(colored("You chose option 3.", "cyan"))
    return

def function_4():   
    print(colored("Goodbye!", "red"))
    return

def function_5():   
    print(colored("Invalid choice. Please try again.", "red"))
    return

def noOption():
    while True:
        # Print the menu options
        print(colored("Menu:", "cyan"))
        print(colored("1. List binaries with SUID bit set", "yellow"))
        print(colored("2. execute the binary ", "green"))
        print(colored("3. Quit", "red"))
        #print(colored("4. Quit", "red"))

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
            function_4()
            break
        else:
            function_5()
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
        for bin in found_bin:
            for row in data:
                #use strip to remove spaces in the start and end of the text
                if row["name"].strip()== bin:
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
    print("entre")
    id = input(f"Enter the command ID opress 'q' to exit.\n")
    if id == 'q':
        sys.exit()
    while id not in ids.keys() :
        id = input(f"You have entered an invalid Value, please a valid Value or press 'q'.\n")
        if id == 'q':
            sys.exit()

    if ids[id]["type"] ==  "File Read":
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
        if ids[id]["name"] in ["timeout","mv", "perl","python", "ruby","gcc", "as","wget"]:
            print(ids[id]["notes"])
        else:
            cmd = ids[id]["cmd"]
            #print(cmd)
            result = subprocess.run(cmd, shell=True)
            if result.returncode == 0 :
                print(result.stdout)
            else:
                print (result.stderr)
    else:
        pass
    return 



def main():
    os.system('cls' if os.name == 'nt' else 'clear')
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