import boto3
import botocore
import paramiko

ec2 = boto3.resource('ec2')

def connect_ssh(key, ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    privkey = paramiko.RSAKey.from_private_key_file(key)
    ssh.connect(ip ,username='ubuntu',pkey=privkey, timeout=300)
    return ssh

def send_cmd(ssh, cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdin.flush()
    data = stdout.read().splitlines()
    for line in data:
        x = line.decode()
        print(x)


def close_ssh(ssh):
    ssh.close()