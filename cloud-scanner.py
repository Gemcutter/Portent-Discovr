import boto3


def nice_disp(inst, var):
    return f'{var}: {inst[var]}'

def aws_ec2_scan(): #must have aws cli configured, add option to manually input access and secret keys
    client = boto3.client('ec2')

    results = client.describe_instances()

    for reservation in results['Reservations']:
        for inst in reservation['Instances']:
            print("-------------------------------")
            print(nice_disp(inst, 'InstanceType'))
            print(nice_disp(inst,'State'))       
            print(nice_disp(inst,'InstanceId'))
            print(nice_disp(inst, 'PlatformDetails'))
            print(nice_disp(inst, 'Architecture'))
            print(nice_disp(inst, 'Tags'))
            print(nice_disp(inst, 'LaunchTime'))
            print("")

            print(nice_disp(inst, 'PrivateIpAddress'))
            try:
                print(nice_disp(inst, 'PublicIpAddress'))
            except KeyError:
                print('Public IP: ' + 'N.A.')

            print(nice_disp(inst, 'PrivateDnsName'))
            if inst['PublicDnsName']:
                print(nice_disp(inst, 'PublicDnsName'))
            else:
                print('PublicDnsName: N.A.')

            print("-------------------------------")
            print("")


aws_ec2_scan()