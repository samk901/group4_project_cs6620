import boto3
import botocore
import paramiko

ec2 = boto3.resource('ec2')


def send_cmd(ip, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    privkey = paramiko.RSAKey.from_private_key_file('final_project_key.pem')
    ssh.connect(ip ,username='ec2-user',pkey=privkey)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdin.flush()
    data = stdout.read().splitlines()
    for line in data:
        x = line.decode()
        #print(line.decode())
        #print(x,i)
        ssh.close()

#send_cmd('54.145.13.62', 'mkdir test')

