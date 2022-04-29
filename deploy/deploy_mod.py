from boto_scripts.create_key_pair import create_pem
from boto_scripts.create_instance_mod import create_instance

# from boto_scripts.create_security_group import create_security_group
# from boto_scripts.create_and_setup_load_balancer import create_load_balancer_security_group, create_load_balancer, \
#     create_target_group, register_ec2_instance_with_target_group, create_listener
from boto_scripts.create_servers import create_db_server, create_api_server, create_ui_server


def deploy():
    # Create ssh key
    keyname = create_pem()
    key = keyname + '.pem'
    print('Created key', key)

    # Create db instance
    instances = create_instance(keyname, num_instances=3)
    # db_ip = instances[0].public_ip_address
    # db_id = instances[0].instance_id

    # # Create api instance
    # api_ip = instances[1].public_ip_address
    # api_id = instances[1].instance_id

    # # Create ui instance
    # ui_ip = instances[2].public_ip_address
    # ui_id = instances[2].instance_id

    # create_db_server(key, db_ip)
    # print('Try connecting at mongodb://' + db_ip)

    # create_api_server(key, db_ip, api_ip)
    # print('Try connecting at', 'http://' + api_ip + ':3000/graphql')

    # create_ui_server(key, api_ip, ui_ip)
    # print('Try connecting at', 'http://' + ui_ip+':3000')

deploy()