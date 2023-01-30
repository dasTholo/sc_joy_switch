import json
import os
import pprint

import PySimpleGUI as sg

from joy_switcher.layouter import get_all_devices, set_devices_instance

sg.theme('DarkAmber')
# if settings not set pop browsefile, create ini
if not os.path.exists("./config.json"):
    DEFAULT_SETTINGS = {"SC Layout": {"orginal_file": "", "modified_layout_name": "modified.xml"}}
    with open("./config.json", "w") as configfile:
        configfile.write(json.dumps(DEFAULT_SETTINGS))

config = sg.UserSettings('./config.json', use_config_file=False, convert_bools_and_none=True, autosave=True)
settings = config.get_dict()
xml_file_path = settings["SC Layout"]["orginal_file"]
layout = [[sg.Text('Orginal SC Layout XML'),
           sg.In(xml_file_path.split(sep="/")[-1:], key='-IN-'),
           sg.FileBrowse(file_types=(("XLM file", "*.xml"),), key="Browse")],
          [sg.Text('New SC Layout XML Name'),
           sg.Input(key='mod_name', default_text=settings["SC Layout"].get("modified_layout_name", "")),
           sg.Button('Save', key="save_mod_name")],
          [sg.Button('Load Xml'), sg.Button('Cancel')]]

window = sg.Window('Joy Switcher', layout)
devices = {}


def load_xml_layout(orginal_file):
    """
    Return a List from all known Devices from the xml
    {   1: {   'instance': '1',
           'name': 'Throttle - HOTAS Warthog',
           'uuid': '{ED0EF470-997F-11ED-8003-444553540000}'},}
    :param orginal_file:
    :return:
    """
    global devices
    devices = get_all_devices(orginal_file)
    # pprint.pprint(devices, indent=4)
    return devices


def load_window_layout():
    global window, layout
    table = [[sg.Text(f"Instance {i}:"),
              sg.Text(devices[i]["name"], key=f"btn{i}"), sg.Text(f"Change to:"),
              sg.Combo([i for i in range(1, len(devices) + 1)],
                       default_value=devices[i]["instance"],
                       key=int(devices[i]['instance'])), ] for i in range(1, len(devices) + 1)]

    layout = [[sg.Text('Orginal SC Layout XML'),
               sg.In(xml_file_path.split(sep="/")[-1:], key='-IN-'),
               sg.FileBrowse(file_types=(("XLM file", "*.xml"),))],
              [sg.Text('New SC Layout XML Name'),
               sg.Input(key='mod_name', default_text=settings["SC Layout"].get("modified_layout_name", "")),
               sg.Button('Save', key="save_mod_name")],
              [sg.Frame("Inputs", layout=table)],
              [sg.Button('Reload Xml'), sg.Button(f"Check Inputs", key="check_inputs")],
              [sg.Button('Save', key="Save"), sg.Button('Cancel')]]
    window1 = sg.Window('Joy Switcher', layout)
    window.close()
    window = window1


def reload_xml(values):
    global xml_file_path
    if values.get("Browse", None) != "":
        settings["SC Layout"]["orginal_file"] = values["Browse"]
        save_settings()
        xml_file_path = settings["SC Layout"]["orginal_file"]
    else:
        xml_file_path = settings["SC Layout"]["orginal_file"]
    return xml_file_path


def save_elements(data):
    name_set = set()
    count = 1
    settings["inputs"] = {}
    for input_device in data:
        if input_device not in devices.keys():
            continue
        if devices.get(input_device, None) is not None:
            dev = devices[input_device]
            input_name = dev["name"]
            if input_name in name_set:
                input_name = f"{input_name}_{count}"
            name_set.add(input_name)
            settings["inputs"][input_name] = {"uuid": dev["uuid"],
                                              "old_instance_nr": int(dev["instance"]),
                                              "new_instance_nr": data[input_device]}

        else:
            print(f"Error can´t save device {input_device}")
        save_settings()


def check_inputs(input_devices):
    moded_input_set = set()
    for i in range(1, len(devices) + 1):
        moded_input_set.add(input_devices.get(i))
    key = set(devices.keys())
    if moded_input_set ^ key:
        sg.popup(f'Instance {key - moded_input_set} not set\n'
                 f'check your Inputs')
    else:
        save_elements(input_devices)


def save_settings():
    config.write_new_dictionary(settings)


def write_to_xml():
    new_xml_path = xml_file_path.replace(
        xml_file_path[xml_file_path.index(xml_file_path.split("/")[-1:][0]):],
        settings["SC Layout"]["modified_layout_name"]
    )
    mod_divices_dict = devices.copy()
    #pprint.pprint(mod_divices_dict, indent=4)

    mod_divices_dict = settings["inputs"]
    pprint.pprint(mod_divices_dict)

    for input_device in mod_divices_dict:
        print(f'Inpu Dev {input_device} als Sett {settings[mod_divices_dict[input_device]["name"]]}:\n'
              f' insta: {mod_divices_dict[input_device]["instance"]} \n '
              f'sett: {settings[mod_divices_dict[input_device]["name"]]["new_instance"]}')
        if int(mod_divices_dict[input_device]["instance"]) != int(settings[mod_divices_dict[input_device]["name"]["new_instance"]]):
            print("nich gleich")

    # set_devices_instance(mod_divices_dict, xml_file_path, new_xml_path)


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    print(f"Event: {event}\n"
          f"values: {values}")
    if event == "Load Xml":
        xml_file_path = reload_xml(values)
        # Cut Path Name to filename
        if window['-IN-'].get()[0] != (xml_file_path.split(sep="/")[-1:][0]):
            window['-IN-'].update(xml_file_path.split(sep="/")[-1:][0])
            # print(f"xml {xml_file_path.split(sep='/')[-1:][0]}")
        load_xml_layout(xml_file_path)
        load_window_layout()
        save_settings()

    if event == "Reload Xml":
        xml_file_path = reload_xml(values)
        load_xml_layout(xml_file_path)
        load_window_layout()

    # calc inputs
    if event == "check_inputs":
        check_inputs(values)

    # New Layout Name
    if event == "save_mod_name":
        if ".xml" in settings["SC Layout"].get("modified_layout_name") and ".xml" in values['mod_name']:
            settings["SC Layout"].set("modified_layout_name", values['mod_name'])
        else:
            settings["SC Layout"]["modified_layout_name"] = f"{values['mod_name']}.xml"
        window["mod_name"].update(settings["SC Layout"].get("modified_layout_name"))
        save_settings()
    if event == "Browse":
        print("browse")
    if event == "Save":
        write_to_xml()

window.close()
