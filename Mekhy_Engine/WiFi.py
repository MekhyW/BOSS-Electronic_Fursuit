import os
import urllib.request

class Finder:
    def __init__(self, *args, **kwargs):
        self.server_name = kwargs['server_name']
        self.password = kwargs['password']
        self.interface_name = kwargs['interface']
        self.main_dict = {}

    def run(self):
        command = """sudo iwlist wlp2s0 scan | grep -ioE 'ssid:"(.*{}.*)'"""
        result = os.popen(command.format(self.server_name))
        result = list(result)

        if "Device or resource busy" in result:
                return None
        else:
            ssid_list = [item.lstrip('SSID:').strip('"\n') for item in result]
            print("Successfully get ssids {}".format(str(ssid_list)))

        for name in ssid_list:
            try:
                result = self.connection(name)
            except Exception as exp:
                print("Couldn't connect to name : {}. {}".format(name, exp))
            else:
                if result:
                    print("Successfully connected to {}".format(name))

    def connection(self, name):
        cmd = "nmcli d wifi connect {} password {} iface {}".format(name,
            self.password,
            self.interface_name)
        try:
            if os.system(cmd) != 0:
                raise Exception()
        except:
            raise # Not Connected
        else:
            return True # Connected


def WiFiconnectionTest(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

def ConnectWifi():
    server_name = "Galaxy A21s3F3B"
    password = "bossmekhy"
    interface_name = "wlp2s0"
    F = Finder(server_name=server_name,
               password=password,
               interface=interface_name)
    F.run()
    return WiFiconnectionTest()