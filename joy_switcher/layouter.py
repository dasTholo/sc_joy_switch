from lxml import etree

SC_PATH = "D:\\OneDrive\\Games\\SC\\SC Profiles\\"
ORG_LAYOUT_FILE = f"{SC_PATH}layout_t_317_1_exported.xml"
MODIFIED_LAYOUT_FILE = f"layout_changed_exported"


def load_xml_file(path, validate=False):
    with open(path, "r") as f:
        parser = etree.XMLParser(dtd_validation=validate)
        return etree.XML(f.read(), parser)


def write_xml_file(path, xml_elements):
    with open(path, "wb") as f:
        f.write(etree.tostring(xml_elements, pretty_print=True, encoding="utf-8", xml_declaration=True))


# xml = load_xml_file(ORG_LAYOUT_FILE)
# childs = xml.getchildren()
# print("Childs")
# print(childs)
# print()

# print(root.attrib["profileName"])

def get_all_devices(xml_path):
    xml = load_xml_file(xml_path)
    device_list = {}
    for device in xml.xpath("options"):
        if device.attrib["type"] == "joystick":
            device_list[int(device.attrib["instance"])] = {"uuid": device.attrib["Product"].split()[-1:][0],
                                                           "name": " ".join(
                                                               map(str, device.attrib["Product"].split()[:-1])),
                                                           "instance": device.attrib["instance"]
                                                           }

    return device_list


def set_devices_instance(mod_devices: dict, old_xml_path, new_xml_name):
    mod_xml = load_xml_file(old_xml_path)
    new_path = old_xml_path.replace(old_xml_path[old_xml_path.index(old_xml_path.split("/")[-1:][0]):], new_xml_name)

    # todo das label hier setzen in den Header aus dem Dict
    for test in mod_xml.xpath("CustomisationUIHeader"):
        print(test.attrib)
    for device in mod_xml.xpath("options"):
        # check name
        # if child.attrib["type"] == "joystick" and child.attrib["Product"]:
        #    child.attrib["instance"] = mod_devices
        if device.attrib["type"] == "joystick" and int(device.attrib["instance"]) in mod_devices.keys():
            if device.attrib['Product'] == mod_devices[int(device.attrib["instance"])]["Product"]:
                print("ja is gleich")
                device.attrib["instance"] = str(mod_devices[int(device.attrib["instance"])]["Instance"])

            # print(f"child instace {device.attrib['instance']}\n"
            #       f"prod: {device.attrib['Product']}")
            # print(device.attrib["instance"])
            # print(type(device.attrib["instance"]))

    write_xml_file(new_path, mod_xml)

def check_device(old_xml, device_list=[]):
    for device in old_xml.xpath("options"):
        dev = device.attrib["Product"].split()

        print(f"dev {dev}")

        dev_id = dev[-1:][0]
        if dev[-1:][0] in device_list:
            print(device.attrib["Product"])
            print(dev[:-1])
            return dev[:-1]


if __name__ == "__main__":
    # check_device(load_xml_file(ORG_LAYOUT_FILE), ["{812F3344-0000-0000-0000-504944564944}"])
    # print(get_all_devices(ORG_LAYOUT_FILE))
    set_devices_instance({1: {'Product': 'vJoy Device  {12C820E0-8E65-11ED-8003-444553540000}', "Instance": 33}},
                         "D:/OneDrive/Games/SC/SC Profiles/layout_t_317_1_exported.xml", "neues_layout.xml")

# print(etree.tostring(root, pretty_print=True))


# https://pyautogui.readthedocs.io/en/latest/install.html#windows
# change to sc
# ^ dann pprebinding load
