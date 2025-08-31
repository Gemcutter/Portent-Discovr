#for AWS
import boto3

#for Azure
from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient


add_log = None


def nice_disp(inst, var):
    return f'{var}: {inst[var]}'

def aws_ec2_scan(args): #must have aws cli configured, add option to manually input access and secret keys
    if args["use_env"] == 1: # use env variables
        client = boto3.client('ec2')

    else: # use entered variables
        client = boto3.client('ec2',
                              aws_access_key_id=args["access_key"],
                              aws_secret_access_key=args["secret_key"],)
                              #region_name=region)

    

    results = client.describe_instances()


    for reservation in results['Reservations']:
        add_log("")
        add_log("===============================")
        add_log(nice_disp(reservation, 'ReservationId'))
        add_log(nice_disp(reservation,'OwnerId'))   
        add_log(nice_disp(reservation,'Groups')) 
        add_log("-------------------------------")

        for inst in reservation['Instances']:
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


def azure_vm_scan(args):
    if args["use_env"] == 1: # use env variables
        subscription_id = args["subscription_id"]#"97dbcd1f-1d36-4993-9596-e073bf1d2221"

        credential = DefaultAzureCredential()
        compute_client = ComputeManagementClient(credential, subscription_id)

    else: 
        tenant_id = args["tenant_id"]
        client_id = args["client_id"]
        client_secret = args["secret_value"]
        subscription_id = args["subscription_id"]

        credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        compute_client = ComputeManagementClient(credential, subscription_id)

    # List all VMs in the subscription
    for vm in compute_client.virtual_machines.list_all():
        add_log(f"Name: {vm.name}")
        add_log(f"VM Type: {vm.hardware_profile.vm_size}")
        add_log(f"Location: {vm.location}")
        add_log("-------------------------------")
