#!/usr/bin/env python
__author__ = "Jesús Vázquez"
import json
from optparse import OptionParser


# Added this from source: https://svn.blender.org/svnroot/bf-blender/trunk/blender/build_files/scons/tools/bcolors.py
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main():
    parser = OptionParser()
    parser.add_option("-a", "--add",
                      help="Add command to the file")
    parser.add_option("-f", "--find",
                      help="Find command")
    parser.add_option("-l", "--list",
                      help="List tags | commands")
    parser.add_option("-c", "--createtag",
                      help="Create a new tag")

    (options, args) = parser.parse_args()

    if options.add:
        add_command(options.add)
    elif options.find:
        find_command(options.find)
    elif options.list:
        list_ucmd(options.list)
    elif options.createtag:
        create_tag(options.createtag)
    # Default print all comands + help
    else:
        list_ucmd('commands')


def load_data():
    global data
    with open(commands_file) as data_file:
        data = json.load(data_file)
    return data


def add_command(command):
    global data
    confirm_command = input(bcolors.OKGREEN + "[+] Sure you want to add this command? (y/n): " + command + "\n> ")
    while confirm_command.lower() != 'y' and confirm_command.lower() != 'n':
        confirm_command = input(bcolors.FAIL + "[-] Sure you want to add this command? (y/n): " + command + "\n> ")
    if confirm_command.lower() == 'y':
        tags = list_ucmd("tags")
        tag = input(bcolors.OKGREEN + "[+] Enter a valid tag for the command. You can always add a new tag (ucmd -c tagName)\n> ")
        while tag not in tags:
            tag = input(bcolors.FAIL + "[-] Enter a valid tag for the command. You can always add a new tag (ucmd -c tagName)\n> ")
        des = input(bcolors.OKGREEN + "[+] Enter a command description (optional)\n> ")
        countCommands = len(data[tag])
        newCommand = {'id': countCommands+1, 'command': command, 'des': des}
        data[tag].append(newCommand)
        save_data(data)

def find_command(command):
    global data
    matches = []
    for key in data.keys():
        for childKey in data[key]:
            if childKey['command'].lower().find(command.lower()) >= 0:
                matches.append(childKey['command'] + " : " + childKey['des'])
    for command in matches:
        print(bcolors.OKGREEN + "[+] " + command + bcolors.ENDC)


def list_ucmd(l):
    global data
    result = []
    if l.lower() == 'tags':
        print(bcolors.WARNING + "AVAILABLE TAGS" + bcolors.ENDC)
        for key in data.keys():
            print(bcolors.OKBLUE + "[+] " + bcolors.BOLD + key + bcolors.ENDC)
            result.append(key)
    elif l.lower() == 'commands':
        print(bcolors.WARNING + "AVAILABLE COMMANDS" + bcolors.ENDC)
        for key in data.keys():
            print(bcolors.OKBLUE + "[+] " + bcolors.BOLD + key + bcolors.ENDC)
            for childKey in data[key]:
                print(bcolors.OKBLUE + "\t" + str(childKey['id']) + ": " + bcolors.OKGREEN
                      + childKey['command'] + " " + bcolors.OKBLUE + childKey['des']
                      + bcolors.ENDC)

    else:
        print(bcolors.FAIL + "[-] Can't list \'" + l + "\'. Right parameters are "
              + bcolors.OKGREEN + "tags | commands" + bcolors.ENDC)
    return result

def create_tag(tag):
    global data
    confirm_tag = input(bcolors.OKGREEN + "[+] Sure you want to add this tag? (y/n): " + tag + "\n> ")
    while confirm_tag.lower() != 'y' and confirm_tag.lower() != 'n':
        confirm_tag = input(bcolors.FAIL + "[-] Sure you want to add this tag? (y/n): " + tag + "\n> ")
    if confirm_tag.lower() == 'y':
        newTag = { tag: [] }
        data.update(newTag)
        save_data(data)


def save_data(data):
    print(bcolors.OKBLUE + "[+] Saving data...")
    with open(commands_file, 'w') as outfile:
            json.dump(data, outfile)


commands_file = "usefulCommands.json"
data = load_data()

if __name__ == '__main__':
    main()
