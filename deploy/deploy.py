#### General Notes ###
# - All methods need try/except block
# - DocDB method is suggested over docker mongo implementation because a cluster of db servers 
#   can easily be built as opposed to a single db server using the docker
# - If compatability issues arrise over docdb please use backup docker method
# - Place boto functions in a seperate file in /boto_scripts to keep this file clean
# - This script should be run from AWS cloud shell
# - docker scripts may need to be adjusted
# - I suggest passing in env variables in the docker run cmd as opposed to using an env file since they are dynamic
# - pass cmds to ec2 using boto using (maybe create a method so this can be done cleanly for both ui/ api):
#   https://stackoverflow.com/questions/34028219/how-to-execute-commands-on-aws-instance-using-boto3
# - For now just set security policy open to all ips, its going to get much more complicated if we try to lock down ips. We can fix this later if needed
# - ideally we just need create_instance method, and one create_load_balancer, one create_security_group, and one send_cmd method that can be reused for both api / ui
#######################

import boto3
import os
import json
from boto_scripts.create_key_pair import create_pem
from boto_scripts.create_instance import create_instance
from boto_scripts.send_cmd import send_cmd, connect_ssh, close_ssh
from boto_scripts.create_security_group import create_security_group
from boto_scripts.create_iam_policy import create_iam_policy
from boto_scripts.create_and_setup_load_balancer import create_load_balancer_security_group, create_load_balancer, create_target_group, register_ec2_instance_with_target_group, create_listener
from os import system
from read_script import read_script

def deploy():
    # Initialize VPC, return vpc_id
    # vpc_id = create_vpc()

    #Iam Policy   
    create_iam_policy()

    #Create load balancer security group.  This will be used for both API load balancer and UI load balancer
    load_balancer_security_group = create_load_balancer_security_group(vpc_id)

    # Create security group for ec2 instances.  Only allows ingress http traffic from load balancers
    create_security_group('Security group for ec2 instances', 'Security group for web and application ec2 instances', load_balancer_security_group.id)

    # Create ssh key
    keyname = create_pem()
    key = keyname +'.pem'
    print('Created key', key)     

    # Create db instance
    db_ip = create_instance(keyname) 
    print('DB Instance IP:', db_ip)


    # DATABASE METHOD-> Mongo Docker
    #    # Reference: https://hub.docker.com/_/mongo
    ssh = connect_ssh(key, db_ip)
    send_cmd(ssh, 'sudo apt update -y')
    send_cmd(ssh, 'sudo apt install docker.io -y')
    send_cmd(ssh, 'sudo docker pull mongo')
    send_cmd(ssh, 'sudo docker run -p 27017:27017 --name some-mongo -d mongo')
    # send_cmd(ssh, 'sudo docker exec -i some-mongo bash')
    send_cmd(ssh, 'echo "APIDIR=/tracker-api" | sudo docker exec -i some-mongo bash -')
    send_cmd(ssh, 'echo "UIDIR=/tracker-ui" | sudo docker exec -i some-mongo bash -')
    send_cmd(ssh, 'echo "apt update -y" | sudo docker exec -i some-mongo bash -')
    send_cmd(ssh, 'echo "apt install wget" | sudo docker exec -i some-mongo bash -')
    send_cmd(ssh, 'echo "wget https://raw.githubusercontent.com/samk901/group4_project_cs6620/main/tracker-api/scripts/init.mongo.js" | sudo docker exec -i some-mongo bash -')
    send_cmd(ssh, 'echo "wget https://raw.githubusercontent.com/samk901/group4_project_cs6620/main/tracker-api/scripts/generate_data.mongo.js" | sudo docker exec -i some-mongo bash -')
    send_cmd(ssh, 'echo "mongo init.mongo.js" | sudo docker exec -i some-mongo bash -')
    send_cmd(ssh, 'echo "mongo generate_data.mongo.js" | sudo docker exec -i some-mongo bash -')
    close_ssh(ssh)

    print('Try connecting at mongodb://'+db_ip)

    # DATABASE METHOD-> Mongo directly on instance
        # cmds = read_script('../install_scripts/mongo_install.sh')
        # for cmd in cmds:
        #     send_cmd(key, db_ip, cmd)
        # print('Try connecting at mongodb://'+db_ip)
            
    # API
        # Inside of create_instance method:
            # create ec2 instance, open port 3000, 
            # sudo apt install git via send_cmd() -> needs to be written (first link)
            # git clone this repository
            # sudo apt install docker
            # docker build
            # docker run, pass in mongo_db_endpoint via -e flag
        
        # tags = []
        #for x in range(3):
        #    tag = create_instance()
        #    tags.append(tag)


    Create and setup api load balacer.  TODO: Jeff to refactor to reduce the number of below lines, keep the logic in load balancer script
    load_balancer_api = create_load_balancer(load_balancer_security_group.id, [
        'subnet-073cd7a90757fd3a4', #TODO: Double check how we will get the subnets to pass in here
        'subnet-0e7ef3710998198bc',
    ])
    target_group_api = create_target_group(vpc_id) 
    registered_target1_api = register_ec2_instance_with_target_group(list(target_group_api.values())[0][0].get('TargetGroupArn'), 'i-008b7ba987ee8d6ea') #TODO: Replace ec2 instance ID here with one we generate
    registered_target2_api = register_ec2_instance_with_target_group(list(target_group_api.values())[0][0].get('TargetGroupArn'), 'i-0ce79f06373a78937') #TODO: Replace ec2 instance ID here with one we generate
    listener_api = create_listener(list(target_group_api.values())[0][0].get('TargetGroupArn'), list(load_balancer_api.values())[0][0].get('LoadBalancerArn'))
    load_balancer_api_dns = list(load_balancer_api.values())[0][0].get('DNSName')
    #TODO: Take this dns value and set it as domain for API calls



    # UI
        # Create instances, open correct port
            # install git, install docker via send_cmd
            # clone repository via send_cmd
            # docker build via send_cmd
            # docker run, pass in dns of api load balancer using -e flag and any other needed
        # Repeat as X times

    #Create and setup ui load balacer.  TODO: Jeff to refactor to reduce the number of below lines, keep the logic in load balancer script
    load_balancer_ui = create_load_balancer(load_balancer_security_group.id, [
        'subnet-073cd7a90757fd3a4', #TODO: Double check how we will get the subnets to pass in here
        'subnet-0e7ef3710998198bc',
    ])
    target_group_ui = create_target_group(vpc_id) #Temporary testing with my VPC_ID, will use vpc_id we generate
    registered_target1_ui = register_ec2_instance_with_target_group(list(target_group_ui.values())[0][0].get('TargetGroupArn'), 'i-008b7ba987ee8d6ea') #TODO: Replace ec2 instance ID here with one we generate
    registered_target2_ui = register_ec2_instance_with_target_group(list(target_group_ui.values())[0][0].get('TargetGroupArn'), 'i-0ce79f06373a78937') #TODO: Replace ec2 instance ID here with one we generate
    listener_ui = create_listener(list(target_group_ui.values())[0][0].get('TargetGroupArn'), list(load_balancer_ui.values())[0][0].get('LoadBalancerArn'))
    load_balancer_ui_dns = list(load_balancer_ui.values())[0][0].get('DNSName')





deploy()
