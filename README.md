# nornir-tools
nornir-tools is a collection of simple CLI tools designed to be used on network devices such as routers, switches, firewalls etc.  

**To do list:**  
1. Add more features
2. Add napalm functions
3. Record failures

## Requirements (tested versions):
python3 (3.8.10)  
python3-nornir-netmiko (0.1.2)  
python3-nornir (3.3.0)  

## Prerequisites:
Add details to files in ./inventory/  

## nornir-cli-runner
nornir-cli-runner will connect to devices listed within ./inventory/hosts.yaml and perform cli commands requested when running the program. Output will be printed to the screen and also to a file in folder called "output". The tool is currently configured for 10 workers which vastly increases the speed of any tasks sent to multiple devices.  
### How to use:
Edit the master-host-inventory.csv file with the list of devices and then run the csv-to-yaml.py tool which will convert the csv file into the correct format and overwrite the ./inventory/hosts.yaml file. Alternatively edit the ./inventory/hosts.yaml file with the list of devices and save in the format required by the application.  
Once the host files are complete, simply run the application and pick from show, configuration or verification mode and you will be asked for the command(s) to be entered and then attempt to perform the tasks on each line in the hosts file.  
