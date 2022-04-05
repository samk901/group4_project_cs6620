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
from boto_scripts.send_cmd import send_cmd


def deploy():
    # Initialize VPC, return vpc_id
        # vpc_id = create_vpc()


        # This is broken in aws academy / not needed
        #create_iam_policy()
    
        # Create ssh key
        keyname = create_pem()
        
    # DATABASE METHOD-> Mongo Docker
        # Reference: https://hub.docker.com/_/mongo
        # create security group using vpc_id (open port 27017 to all ips or just the api loadbalancer ip?)
        # create ec2 instance, return ip address
        # sudo apt install docker via top link of this file
        # sudo docker pull mongo
        # docker run --name some-mongo -d mongo:tag

        # Create instance to load mongo onto
#        time.sleep(10)
        public_ip = create_instance(keyname)
        print(public_ip)
        send_cmd(public_ip, 'sudo apt update -y')
        send_cmd(public_ip, 'sudo apt upgrade -y')
        send_cmd(public_ip, 'sudo apt install docker.io -y')
            
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

        # create load balancer -> turns multiple instances into one public dns we can ref
        # Reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb.html#ElasticLoadBalancing.Client.create_load_balancer, return public dns address
        # dns = create_load_balancer(tags)



    # UI
        # Create instances, open correct port
            # install git, install docker via send_cmd
            # clone repository via send_cmd
            # docker build via send_cmd
            # docker run, pass in dns of api load balancer using -e flag and any other needed
        # Repeat as X times
        # Add load balancer on top so we have on dns/ip to connect to

    # return dns or ip of UI





deploy()
