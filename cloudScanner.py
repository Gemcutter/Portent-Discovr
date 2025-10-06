#for AWS
import boto3

#for Azure
from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient


add_log = None
aws_region_codes = [
    "us-east-1",      # US East (N. Virginia)
    "us-east-2",      # US East (Ohio)
    "us-west-1",      # US West (N. California)
    "us-west-2",      # US West (Oregon)
    "af-south-1",     # Africa (Cape Town)
    "ap-east-1",      # Asia Pacific (Hong Kong)
    "ap-east-2",      # Asia Pacific (Taipei)
    "ap-northeast-1", # Asia Pacific (Tokyo)
    "ap-northeast-2", # Asia Pacific (Seoul)
    "ap-northeast-3", # Asia Pacific (Osaka)
    "ap-southeast-1", # Asia Pacific (Singapore)
    "ap-southeast-2", # Asia Pacific (Sydney)
    "ap-southeast-3", # Asia Pacific (Jakarta)
    "ap-southeast-4", # Asia Pacific (Melbourne)
    "ap-southeast-5", # Asia Pacific (Malaysia)
    "ap-southeast-7", # Asia Pacific (Thailand)
    "ap-south-1",     # Asia Pacific (Mumbai)
    "ap-south-2",     # Asia Pacific (Hyderabad)
    "ca-central-1",   # Canada (Central)
    "ca-west-1",      # Canada West (Calgary)
    "eu-central-1",   # Europe (Frankfurt)
    "eu-central-2",   # Europe (Zurich)
    "eu-west-1",      # Europe (Ireland)
    "eu-west-2",      # Europe (London)
    "eu-west-3",      # Europe (Paris)
    "eu-north-1",     # Europe (Stockholm)
    "eu-south-1",     # Europe (Milan)
    "eu-south-2",     # Europe (Spain)
    "il-central-1",   # Israel (Tel Aviv)
    "me-south-1",     # Middle East (Bahrain)
    "me-central-1",   # Middle East (UAE)
    "mx-central-1",   # Mexico (Central)
    "sa-east-1"       # South America (São Paulo)
]


def nice_disp(inst, var):
    return f'{var}: {inst[var]}'

def aws_ec2_scan(add_log, activeScanning, netMap, args): #must have aws cli configured, add option to manually input access and secret keys
    try:
        if args["use_env"] == 1: # use env variables
            client = boto3.client('ec2')

        else: # use entered variables
            client = boto3.client('ec2',
                                aws_access_key_id=args["access_key"],
                                aws_secret_access_key=args["secret_key"],
                                region_name="ap-southeast-2") # temporary fix

        

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
    except Exception as e:
        print(e)
    
    activeScanning[0] = False


def azure_vm_scan(add_log, activeScanning, netMap, args):
    try:
        subscription_id = args["subscription_id"]

        credential = DefaultAzureCredential()
        compute_client = ComputeManagementClient(credential, subscription_id)

        # List all VMs in the subscription
        add_log("===============================")
        for vm in compute_client.virtual_machines.list_all():
            add_log(f"Name: {vm.name}")
            add_log(f"VM Type: {vm.hardware_profile.vm_size}")
            add_log(f"Location: {vm.location}")
            add_log("-------------------------------")
    except Exception as e:
        print(e)
    activeScanning[0] = False