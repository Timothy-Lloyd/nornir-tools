from nornir import InitNornir
from nornir_utils.plugins.tasks.files import write_file
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
from nornir_netmiko import netmiko_send_config
import getpass
import io
import time
import os

localtime = time.localtime()
formattime = time.strftime("%d-%m-%Y %H:%M:%S", localtime)
datetime = time.strftime("%d-%m-%Y", localtime)

if not os.path.exists("output"):
    os.mkdir("output")
if not os.path.exists("output/nornir-cli-runner"):
    os.mkdir("output/nornir-cli-runner")
if not os.path.exists("output/nornir-cli-runner/" + datetime):
    os.mkdir("output/nornir-cli-runner/" + datetime)

def showtasks(nr):
    output = nr.run(
        task = netmiko_send_command,
        command_string = command,
        enable = True
    )
    nr.run(
        task = write_file,
        content = output.result,
        filename = f"output/nornir-cli-runner/{datetime}/{nr.host} " + command + " " + formattime + ".txt"
    )

def verifytasks(nr):
    output = nr.run(
        task = netmiko_send_command,
        command_string = "show run",
        enable = True
    )
    if command in output.result:
        nr.run(
            task = write_file,
            append = True,
            content = f"\r\n##################\r\n{nr.host}\r\n{command} - Exists!\r\n##################\r\n",
            filename = f"output/nornir-cli-runner/{datetime}/VERFIY PASS " + command + " " + formattime + ".txt"
        )
        print(f"\r\n##################\r\n{nr.host}\r\n{command} - Exists!\r\n##################\r\n")
    else:
        nr.run(
        task = write_file,
        append = True,
        content = f"\r\n##################\r\n{nr.host}\r\n{command} - Does not exist!\r\n##################\r\n",
        filename = f"output/nornir-cli-runner/{datetime}/VERFIY FAIL " + command + " " + formattime + ".txt"
        )
        print(f"\r\n##################\r\n{nr.host}\r\n{command} - Does not exist!\r\n##################\r\n")

print("\r\nWelcome to nornir based cli command runner!\r\n\r\nSelect mode, s = show/run, c = configuration or v = to verify the existance of a command:")
mode = input()

nr = InitNornir(
    config_file="config.yaml", dry_run=False
)

print("\r\nPlease enter the credentials to perform the tasks required:\r\n")
print("Username: ", end="")
usern = str(input())
password = getpass.getpass()
secret = getpass.getpass(prompt='Secret: ')
nr.inventory.defaults.username = usern
nr.inventory.defaults.password = password

for host in nr.inventory.hosts.keys():
    nr.inventory.hosts[host].connection_options['netmiko'].extras['secret'] = secret

if mode == "s":
    print("Enter command to run on all devices:")
    command = input()
    
    output = nr.run(
        task=showtasks
        )
    print_result(output)

if mode == "c":
    print("Enter configuration commands with care. When finished press Ctrl-D (Ctrl-Z on Windows) once to break then please wait.")
    cmdset = []
    while True:
        try:
            cmdline = input()
        except EOFError:
            break
        cmdset.append(cmdline)
    
    output = nr.run(
    task = netmiko_send_config,
    config_commands = cmdset
    )
    print_result(output)


if mode == "v":
    print("Enter configuration to verify existence on all devices:")
    command = input()
    
    output = nr.run(
        task=verifytasks
        )

