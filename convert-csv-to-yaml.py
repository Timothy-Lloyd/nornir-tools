#Only to use to convert changes made within master-host-inventory.csv to ./inventory/hosts.yaml file.
import csv
import os

print("This will overwrite existing ./inventory/hosts.yaml file with CSV contents, breakout if not desired!")
input()

with open("master-host-inventory.csv", "r") as f:
    csv_2_yaml = csv.reader(f)
    next(csv_2_yaml)
    fi = open(os.path.join("./inventory/hosts.yaml"), "w")
    fi.write("---\n")
    fi.close()

    for row in csv_2_yaml:
        fi = open(os.path.join("./inventory/hosts.yaml"), "a")
        fi.write("{0}:\n   hostname: {1}\n   groups:\n        - {2}\n   connection_options:\n      netmiko:\n         extras:\n            secret: {3}\n"
        .format(row[0], row[1], row[2], row[3]))
        fi.close()
    
    print("Conversion Completed!")
