#!/usr/bin/python
import paramiko
import time

hosts_file = '/home/user/hosts'
ssh_user = 'user'
ssh_key_filename = '/home/user/id_rsa'
ssh_password = '111'

ssh = paramiko.SSHClient()


def ssh_connect():
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=ssh_user, key_filename=ssh_key_filename)
    return None


def get_hosts():
    hosts = []
    c = open(hosts_file, "r+")
    for line in c:
        hosts.append(line.rstrip())
    return hosts


def get_logs():
    containers = []
    ssh_connect()
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo docker ps | awk \'{if(NR>1) print $NF}\'', get_pty=True)
    running_containers = ssh_stdout.read().split()
    logs = ['/opt/getty/apps/logs/' + s + '.log' for s in running_containers]

    for log in logs:
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo du -h %s' % log, get_pty=True)
        containers.append(ssh_stdout.read())
    return containers


def command_run():
    ssh_connect()
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo docker restart $(sudo docker ps -q)', get_pty=True)
    return ssh_stdout.read()


hosts = get_hosts()
log = open('output.log', 'wt')
for host in hosts:
    try:
        result = command_run()
        time.sleep(120)
        print host
        print result
        log.write((host + '\n' + result + '\n'))
    except Exception as e:
        log.write((host + '\n' + str(e) + ' \n'))

log.close()
