from boto_scripts.send_cmd import connect_ssh, send_cmd, close_ssh


def create_db_server(key, instance_ip):
    ssh = connect_ssh(key, instance_ip)
    send_cmd(ssh, 'sudo apt update -y')
    send_cmd(ssh, 'sudo apt install docker.io -y')
    send_cmd(ssh, 'sudo docker pull mongo')
    send_cmd(ssh, 'sudo docker run -p 27017:27017 --name some-mongo -d mongo')
    # send_cmd(ssh, 'sudo docker exec -i some-mongo bash')
    send_cmd(ssh, 'echo "APIDIR=/tracker-api" | sudo docker exec -i some-mongo bash -')
    send_cmd(ssh, 'echo "UIDIR=/tracker-ui" | sudo docker exec -i some-mongo bash -')
    send_cmd(ssh, 'echo "apt update -y" | sudo docker exec -i some-mongo bash -')
    send_cmd(ssh, 'echo "apt install wget" | sudo docker exec -i some-mongo bash -')
    send_cmd(ssh,
             'echo "wget https://raw.githubusercontent.com/samk901/group4_project_cs6620/main/tracker-api/scripts/init.mongo.js" | sudo docker exec -i some-mongo bash -')
    send_cmd(ssh,
             'echo "wget https://raw.githubusercontent.com/samk901/group4_project_cs6620/main/tracker-api/scripts/generate_data.mongo.js" | sudo docker exec -i some-mongo bash -')
    send_cmd(ssh, 'echo "mongo init.mongo.js" | sudo docker exec -i some-mongo bash -')
    send_cmd(ssh, 'echo "mongo generate_data.mongo.js" | sudo docker exec -i some-mongo bash -')
    close_ssh(ssh)


def create_api_server(key, db_ip, instance_ip):
    ssh = connect_ssh(key, instance_ip)
    send_cmd(ssh, 'git clone https://github.com/samk901/group4_project_cs6620.git')
    send_cmd(ssh, 'sudo apt update -y')
    send_cmd(ssh, 'sudo apt install docker.io -y')
    send_cmd(ssh, 'sudo docker build -t node -f group4_project_cs6620/tracker-api/Dockerfile .')
    send_cmd(ssh, 'sudo docker run -d -e DB_URL=mongodb://{db_ip} -e PORT=3000 -p 3000:3000 node:latest'.format(db_ip=str(db_ip)))
    close_ssh(ssh)


def create_ui_server(key, api_ip, instance_ip):
    ssh = connect_ssh(key, instance_ip)
    send_cmd(ssh, 'git clone https://github.com/samk901/group4_project_cs6620.git')
    send_cmd(ssh, 'sudo apt update -y')
    send_cmd(ssh, 'sudo apt install docker.io -y')
    # send_cmd(ssh, 'sudo usermod -aG docker $USER')
    send_cmd(ssh, 'sudo docker build -t ui -f group4_project_cs6620/tracker-ui/Dockerfile .')
    send_cmd(ssh, 'sudo docker run -d -e UI_API_ENDPOINT=http://{api_ip}:3000/graphql -e UI_SERVER_PORT=3000 -p 3000:3000 ui:latest'.format(api_ip=str(api_ip)))
    close_ssh(ssh)
