import os
import subprocess
import yaml

config = yaml.safe_load(open(os.path.dirname(os.path.abspath(__file__)) + "/config.yml"))

def main():
    for client in config["clients"]:
        if config["clients"][client]["wake"] is True:
            wake_computer(config["clients"][client]["mac"], client)
        wait_for_ping(config["clients"][client]["ip"], client)
        start_command(config["command"], \
            config["clients"][client]["username"], \
            config["clients"][client]["ip"], client)

def wake_computer(mac, name):
    print("[", name, "]", " Waking up ", "(MAC: ", mac, ").", sep="")
    try:
        subprocess.run(["wol", mac], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("[", name, "]", " wol returned a non-zero exit code,", sep="")
        exit(1)

def wait_for_ping(ip, name):
    print("[", name, "]", " Waiting for ", ip, " to come online.", sep="")
    fail_counter = 0
    while True:
        if fail_counter >= 15:
            print("[", name, "]", "The client took too long to start, skipping.")
            break
        else:
            try:
                subprocess.run(["ping", ip, "-c 3"], check=True, capture_output=True)
            except subprocess.CalledProcessError:
                print("[", name, "]", " Attempt ", str(fail_counter + 1), "/15.", " Still down...", sep="")
                fail_counter += 1
            else:
                print("[", name, "]", " And we are up! This took ", str(fail_counter + 1), " attempts.", sep="")
                break

def start_command(command, username, ip, name):
    uname_ip = username + "@" + ip
    print("[", name, "]", " Executing \'", command, "\' on ", uname_ip, sep="")
    subprocess.run(["ssh", uname_ip, command])
    print("[", name, "]", " Execution finished!", sep="")

if __name__ == "__main__":
    main()
