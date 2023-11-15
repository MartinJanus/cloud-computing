import requests
import json
import subprocess
import time

# accessing azure-cli to get the bearer access token, parse json
def get_azure_access_token():
    try:
        result = subprocess.run(["az", "account", "get-access-token", "--output", "json"], capture_output=True, check=True)
        token_info = json.loads(result.stdout)
        return token_info['accessToken']
    except subprocess.CalledProcessError as e:
        print("Error getting Azure access token:", e)
        return None
    


token = get_azure_access_token()

# create azure resource
def create_resource(url, data):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"    
    }
    response = requests.put(url, headers=headers, json=data)
    return response.status_code

# user input function
def get_user_input(prompt):
    return input(prompt).strip()


#get bearer token 
# inputting for resource group, virtual network, subnet, public IP, NIC, and VM names
#token = get_user_input("Get Bearer Access Token: ")
resource_group_name = get_user_input("Enter Resource Group Name: ")
virtual_network_name = get_user_input("Enter Virtual Network Name: ")
subnet_name = get_user_input("Enter Subnet Name: ")
public_ip_name = get_user_input("Enter Public IP Address Name: ")
nic_name = get_user_input("Enter Network Interface Name: ")
vm_name = get_user_input("Enter VM Name: ")

# api urls
resource_group_url = f"https://management.azure.com/subscriptions/201646b6-d66b-4a8e-9cbb-ec84ec6a0e82/resourcegroups/{resource_group_name}?api-version=2021-04-01"
virtual_network_url = f"https://management.azure.com/subscriptions/201646b6-d66b-4a8e-9cbb-ec84ec6a0e82/resourceGroups/{resource_group_name}/providers/Microsoft.Network/virtualNetworks/{virtual_network_name}?api-version=2023-05-01"
subnet_url = f"https://management.azure.com/subscriptions/201646b6-d66b-4a8e-9cbb-ec84ec6a0e82/resourceGroups/{resource_group_name}/providers/Microsoft.Network/virtualNetworks/{virtual_network_name}/subnets/{subnet_name}?api-version=2023-05-01"
public_ip_url = f"https://management.azure.com/subscriptions/201646b6-d66b-4a8e-9cbb-ec84ec6a0e82/resourceGroups/{resource_group_name}/providers/Microsoft.Network/publicIPAddresses/{public_ip_name}?api-version=2023-05-01"
nic_url = f"https://management.azure.com/subscriptions/201646b6-d66b-4a8e-9cbb-ec84ec6a0e82/resourceGroups/{resource_group_name}/providers/Microsoft.Network/networkInterfaces/{nic_name}?api-version=2023-05-01"
vm_url = f"https://management.azure.com/subscriptions/201646b6-d66b-4a8e-9cbb-ec84ec6a0e82/resourceGroups/{resource_group_name}/providers/Microsoft.Compute/virtualMachines/{vm_name}?api-version=2023-07-01"

# resource group data
resource_group_data = {
    "location": "westeurope"
}

# virtual network data
virtual_network_data = {
    "properties": {
        "addressSpace": {
            "addressPrefixes": ["10.0.0.0/16"]
        },
        "flowTimeoutInMinutes": 10
    },
    "location": "westeurope"
}

# subnet data
subnet_data = {
    "properties": {
        "addressPrefix": "10.0.0.0/16"
    }
}

# public ip address data
public_ip_data = {
    "location": "westeurope"
}

# network interface data 
nic_data = {
    "properties": {
        "ipConfigurations": [
            {
                "name": "ipconfig1",
                "properties": {
                    "publicIPAddress": {
                        "id": f"/subscriptions/201646b6-d66b-4a8e-9cbb-ec84ec6a0e82/resourceGroups/{resource_group_name}/providers/Microsoft.Network/publicIPAddresses/{public_ip_name}"
                    },
                    "subnet": {
                        "id": f"/subscriptions/201646b6-d66b-4a8e-9cbb-ec84ec6a0e82/resourceGroups/{resource_group_name}/providers/Microsoft.Network/virtualNetworks/{virtual_network_name}/subnets/{subnet_name}"
                    }
                }
            }
        ]
    },
    "location": "westeurope"
}

# vm data
vm_data = {
    "id": f"/subscriptions/201646b6-d66b-4a8e-9cbb-ec84ec6a0e82/resourceGroups/{resource_group_name}/providers/Microsoft.Compute/virtualMachines/{vm_name}",
    "type": "Microsoft.Compute/virtualMachines",
    "properties": {
        "osProfile": {
            "adminUsername": "martin",
            "secrets": [],
            "computerName": vm_name,
            "linuxConfiguration": {
                "ssh": {
                    "publicKeys": [
                        {
                            "path": "/home/martin/.ssh/authorized_keys",
                            "keyData": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCsxP2gmr2VhefmSeB07WtVpOP3IquuVmGgx23jjW7ihA+rJjsUnEA/uf5a9Qr5tvA3fDlaADTKOn8A54j2KVut1My4soro4YL5ziyiIYjzcn9CCI7EUscB41f1vNQqGuhvJot2UB4mKRLDgJgtCUzM5jm5Su32yJQa1Zybl9uxyU/BFnK3JFiynoMl30ADbZYBz6owc4+yFJDy46l0SiAiOJRKlPQmrH10YMnWQyiFrON07b2RJRyPr80QXt9t+ynWGwJeO5nv1WQZirNVuzze1yWCQtQ8L3ySFSj9LA3Xw2n34NEWUvK6PMGmJf1+FnxjVzC6KxExKkglXXfcv8N9 martin@martin"
                        }
                    ]
                },
                "disablePasswordAuthentication": True
            }
        },
        "networkProfile": {
            "networkInterfaces": [
                {
                    "id": f"/subscriptions/201646b6-d66b-4a8e-9cbb-ec84ec6a0e82/resourceGroups/{resource_group_name}/providers/Microsoft.Network/networkInterfaces/{nic_name}",
                    "properties": {
                        "primary": True
                    }
                }
            ]
        },
        "storageProfile": {
            "imageReference": {
                "sku": "16.04-LTS",
                "publisher": "Canonical",
                "version": "latest",
                "offer": "UbuntuServer"
            },
            "dataDisks": []
        },
        "hardwareProfile": {
            "vmSize": "Standard_D1_v2"
        },
        "provisioningState": "Creating"
    },
    "name": vm_name,
    "location": "westeurope"
}

# azure resources
resource_group_response = create_resource(resource_group_url, resource_group_data)
virtual_network_response = create_resource(virtual_network_url, virtual_network_data)
subnet_response = create_resource(subnet_url, subnet_data)
public_ip_response = create_resource(public_ip_url, public_ip_data)
time.sleep(5)
nic_response = create_resource(nic_url, nic_data)
vm_response = create_resource(vm_url, vm_data)

# print response messages
print("Resource Group Response:", resource_group_response)
print("Virtual Network Response:", virtual_network_response)
print("Subnet Response: ", subnet_response)
print("Public IP Response: ", public_ip_response)
print("Network Interface Response: ", nic_response)
print("Virtual Machine Response: ", vm_response)
