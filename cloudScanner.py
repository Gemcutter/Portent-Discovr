import boto3


def nice_disp(inst, var):
    return f'{var}: {inst[var]}'

def aws_ec2_scan(add_log, args): #must have aws cli configured, add option to manually input access and secret keys
    client = boto3.client('ec2')

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