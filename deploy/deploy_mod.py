from boto_scripts.create_key_pair import create_pem
from boto_scripts.create_instance_mod import create_instance

from boto_scripts.create_security_group import create_security_group
from boto_scripts.create_and_setup_load_balancer import create_load_balancer_security_group, create_load_balancer, \
    create_target_group, register_ec2_instance_with_target_group, create_listener
from boto_scripts.create_iam_policy import create_iam_policy
from boto_scripts.create_servers import create_db_server, create_api_server, create_ui_server


def deploy():


    vpc_id = 'vpc-08a8476b32003e8d3'

    create_iam_policy()

    #Create load balancer security group.  This will be used for both API load balancer and UI load balancer
    load_balancer_security_group = create_load_balancer_security_group(vpc_id)
    print("getting here1")

    ec2_instance_security_group = create_security_group('final_project', 'EC2 instance security group', load_balancer_security_group.id)
    print("getting here2")

    # Create ssh key
    keyname = create_pem()
    key = keyname + '.pem'
    print('Created key', key)

    # Create 5 EC2 instaces (1 for database, 2 for API servers, 2 for UI servers)
    instances = create_instance(keyname, num_instances=5)

    #DB instance info
    db_ip = instances[0].public_ip_address
    db_id = instances[0].instance_id

    #Api instance info
    api_ip1 = instances[1].public_ip_address
    api_id1 = instances[1].instance_id
    api_ip2 = instances[2].public_ip_address
    api_id2 = instances[2].instance_id

    # UI instance info
    ui_ip1 = instances[3].public_ip_address
    ui_id1 = instances[3].instance_id
    ui_ip2 = instances[4].public_ip_address
    ui_id2 = instances[4].instance_id

    #Setup db server with mongo and initialize dummy data in database
    create_db_server(key, db_ip)
    print('Try connecting at mongodb://' + db_ip)

    #Create 2 API servers and create/setup load balancer for api servers
    create_api_server(key, db_ip, api_ip1)
    create_api_server(key, db_ip, api_ip2)
    # print('Try connecting at', 'http://' + api_ip1 + ':3000/graphql')

    load_balancer_api = create_load_balancer(load_balancer_security_group.id, [
        'subnet-073cd7a90757fd3a4', #TODO: Double check how we will get the subnets to pass in here
        'subnet-0e7ef3710998198bc',
    ], 'api_load_balancer')
    target_group_api = create_target_group(vpc_id, 'api_load_balancer_target_group') 
    registered_target1_api = register_ec2_instance_with_target_group(list(target_group_api.values())[0][0].get('TargetGroupArn'), api_id1) 
    registered_target2_api = register_ec2_instance_with_target_group(list(target_group_api.values())[0][0].get('TargetGroupArn'), api_id2)
    listener_api = create_listener(list(target_group_api.values())[0][0].get('TargetGroupArn'), list(load_balancer_api.values())[0][0].get('LoadBalancerArn'))
    load_balancer_api_dns = list(load_balancer_api.values())[0][0].get('DNSName')
    #----------------------------------------------------------------------------------------------------------------------------------

    #Create 2 UI servers and create/setup load balancer for UI servers
    create_ui_server(key, load_balancer_api_dns, ui_ip1)
    create_ui_server(key, load_balancer_api_dns, ui_ip2)
    # print('Try connecting at', 'http://' + ui_ip1 +':3000')

    load_balancer_ui = create_load_balancer(load_balancer_security_group.id, [
        'subnet-073cd7a90757fd3a4', #TODO: Double check how we will get the subnets to pass in here
        'subnet-0e7ef3710998198bc',
    ], 'ui_load_balancer')
    target_group_ui = create_target_group(vpc_id, 'ui_load_balancer_target_group') #Temporary testing with my VPC_ID, will use vpc_id we generate
    registered_target1_ui = register_ec2_instance_with_target_group(list(target_group_ui.values())[0][0].get('TargetGroupArn'), ui_id1)
    registered_target2_ui = register_ec2_instance_with_target_group(list(target_group_ui.values())[0][0].get('TargetGroupArn'), ui_id2)
    listener_ui = create_listener(list(target_group_ui.values())[0][0].get('TargetGroupArn'), list(load_balancer_ui.values())[0][0].get('LoadBalancerArn'))
    load_balancer_ui_dns = list(load_balancer_ui.values())[0][0].get('DNSName')
    
    print("Visit the live site at " + load_balancer_ui_dns)

deploy()