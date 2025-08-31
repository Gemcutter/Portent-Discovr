#for AWS
import boto3

#for Azure
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient


def nice_disp(inst, var):
    return f'{var}: {inst[var]}'

def aws_ec2_scan(add_log, args): #must have aws cli configured, add option to manually input access and secret keys
    if args[0] == 0 and args[1] == 0: # use env variables
        client = boto3.client('ec2')

    else: # use entered variables
        client = boto3.client('ec2',
                              aws_access_key_id=args[0],
                              aws_secret_access_key=args[1],)
                              #region_name=region)

    

    results = client.describe_instances()


    for reservation in results['Reservations']:
        add_log("")
        add_log("===============================")
        add_log(nice_disp(reservation, 'ReservationId'))
        add_log(nice_disp(reservation,'OwnerId'))   
        add_log(nice_disp(reservation,'Groups')) 

        for inst in reservation['Instances']:
            add_log("-------------------------------")
            add_log(nice_disp(inst, 'InstanceType'))
            add_log(nice_disp(inst,'State'))       
            add_log(nice_disp(inst,'InstanceId'))
            add_log(nice_disp(inst, 'PlatformDetails'))
            add_log(nice_disp(inst, 'Architecture'))
            add_log(nice_disp(inst, 'Tags'))
            add_log(nice_disp(inst, 'LaunchTime'))
            add_log("")

            add_log(nice_disp(inst, 'PrivateIpAddress'))
            try:
                add_log(nice_disp(inst, 'PublicIpAddress'))
            except KeyError:
                add_log('Public IP: ' + 'N.A.')

            add_log(nice_disp(inst, 'PrivateDnsName'))
            if inst['PublicDnsName']:
                add_log(nice_disp(inst, 'PublicDnsName'))
            else:
                add_log('PublicDnsName: N.A.')

        add_log("-------------------------------")
        add_log("")


def azure_vm_scan(add_log, args):
    pass

if __name__ == "__main__":
    print("A")
    subscription_id = "97dbcd1f-1d36-4993-9596-e073bf1d2221"

    # Authenticate
    credential = DefaultAzureCredential()
    compute_client = ComputeManagementClient(credential, subscription_id)

    # List all VMs in the subscription
    for vm in compute_client.virtual_machines.list_all():
        print(f"Name: {vm.name}, Location: {vm.location}, Resource Group: {vm.id.split('/')[4]}")