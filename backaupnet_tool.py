#!/usr/bin/env python3

import json


def load_json():
    try:
        with open("file/devices.json") as f:
            config_file = json.load(f)
        return config_file
    
    except FileNotFoundError as e:
        print()
        print("#! FILE NOT FOUND")
        print(f"#! Problem: {e}")
        print("#! Exiting...")
        print()
        exit()

    except json.decoder.JSONDecodeError as e:
        print()
        print("#! WRONG JSON FILE")
        print(f"#! Problem: {e}")
        print("#! Exiting...")
        print()
        exit()

    except Exception as e:
        print()
        print("#! ERROR !#")
        print(f"#! Error occure: {e}")
        print("#! Exiting...")
        print()
        exit()


class Config_Load():

    data = load_json()

    def __init__(self) -> None:
        pass



    @classmethod
    def get_vendor_dev(cls, vendor):
        dev_lst = []
        exist = False
        
        try:
            cls.data["devices"][vendor]
            exist = True

        except KeyError as e:
            print()
            print(f"#! Device {vendor} don't exist.")
            return None

        except Exception as e:
            exit()

        finally:
            if exist:
                for device in cls.data["devices"][vendor].items():
                    dev_lst.append(device)
                return dev_lst



class Backup():

    def __init__(self) -> None:
        Config_Load()
        self.cisco = Config_Load.get_vendor_dev("cisco")
        self.mikrotik = Config_Load.get_vendor_dev("mikrotik")


    def create_device(self):
        for vendor in self.data["devices"].keys():
            if vendor == "cisco":
                Cisco(vendor, vendor.keys())


class Device():

    device_lst = []
    vendor_lst = set()

    def __init__(
            self,
            vendor: str,
            ip: str,
            username: str,
            password: str,
            pashprase: str,
            port: int,
            connection: str
            ) -> None:
        self.vendor = vendor
        self.ip = ip
        self.username = username
        self.password = password
        self.pashprase = pashprase
        self.port = port
        self.connection = connection
        Device.device_lst.append(self)
        Device.vendor_lst.add(self.vendor)


class Cisco(Device):

    cisco_dev_lst = []

    def __init__(
            self, 
            vendor: str, 
            ip: str, 
            username: str, 
            password: str, 
            pashprase: str, 
            port: int, 
            connection: str
            ) -> None:
        super().__init__(
            vendor, 
            ip, 
            username, 
            password, 
            pashprase, 
            port, 
            connection
            )



class Mikrotik(Device):


    mikrotik_dev_lst = []


    def __init__(
            self, 
            vendor: str, 
            ip: str, 
            username: str, 
            password: str, 
            pashprase: str, 
            port: int, 
            connection: str
            ) -> None:
        super().__init__(
            vendor, 
            ip, 
            username, 
            password, 
            pashprase, 
            port, 
            connection
            )



if __name__ == "__main__":
    pass