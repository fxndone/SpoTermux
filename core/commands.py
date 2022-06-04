import os

def exec_command(comm):
    if not os.path.isdir(".files/"):
        os.mkdir(".files/")
    out_code = os.system(comm + " 1> .files/.command 2> /dev/null")
    with open(".files/.command", 'r') as f:
        out_data = f.read()
    if os.path.isfile(".files/.command"):
        os.remove(".files/.command")
    return (out_data, out_code)

def clear_screen():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")