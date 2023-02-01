import json
import os
import pprint

import PySimpleGUI as sg

from joy_switcher.layouter import get_all_devices, set_devices_instance

sg.theme('DarkAmber')
# if settings not set pop browsefile, create ini
if not os.path.exists("./config.json"):
    DEFAULT_SETTINGS = {"SC Layout": {"original_file": "", "modified_layout_name": "modified"}}
    with open("./config.json", "w") as configfile:
        configfile.write(json.dumps(DEFAULT_SETTINGS))

config = sg.UserSettings('./config.json', use_config_file=False, convert_bools_and_none=True, autosave=True)
settings = config.get_dict()
xml_file_path = settings["SC Layout"]["original_file"]
layout = [[sg.Text('Original SC Layout XML'),
           sg.In(xml_file_path.split(sep="/")[-1:], key='-IN-'),
           sg.FileBrowse(file_types=(("XLM file", "*.xml"),), key="Browse")],
          [sg.Text('New SC Layout Name'),
           sg.Input(key='mod_name', default_text=settings["SC Layout"].get("modified_layout_name", "")),
           sg.Button('Save', key="save_mod_name")],
          [sg.Button('Load Xml'), sg.Button('Cancel')]]

window = sg.Window('Joy Switcher', layout)
devices = {}
checked = False


def load_xml_layout(original_file):
    """
    Return a List from all known Devices from the xml
    {   1: {   'instance': '1',
           'name': 'Throttle - HOTAS Warthog',
           'uuid': '{ED0EF470-997F-11ED-8003-444553540000}'},}
    :param original_file:
    :return:
    """
    global devices
    devices = get_all_devices(original_file)
    # pprint.pprint(devices, indent=4)
    return devices


def load_window_layout():
    global window, layout
    table = [[sg.Text(f"Instance {i}:"),
              sg.Text(devices[i]["name"], key=f"btn{i}"), sg.Push(),
              sg.Text(f"Change to:"),
              sg.Combo([i for i in range(1, len(devices) + 1)],
                       default_value=devices[i]["instance"],
                       key=int(devices[i]['instance'])), ] for i in range(1, len(devices) + 1)]

    layout = [[sg.Text('Original SC Layout XML'),
               sg.In(xml_file_path.split(sep="/")[-1:], key='-IN-', size=(50, 10)),
               sg.FileBrowse(file_types=(('XLM file', '*.xml'),))],
              [sg.Text('New SC Layout Name'),
               sg.In(key='mod_name', default_text=settings["SC Layout"].get("modified_layout_name", "")),
               sg.Button('Save', key="save_mod_name")],
              [sg.Frame("Inputs", layout=table, size=(535, (len(devices) * 30)))],
              [sg.Button('Reload Xml'), sg.Button(f"Check Inputs", key="check_inputs")],
              [sg.Button('Save', key="Save"), sg.Button('Cancel')]]
    window1 = sg.Window('Joy Switcher', layout)
    window.close()
    window = window1


def reload_xml(values):
    global xml_file_path
    if values.get("Browse", None) != "":
        settings["SC Layout"]["original_file"] = values["Browse"]
        save_settings()
        xml_file_path = settings["SC Layout"]["original_file"]
    else:
        xml_file_path = settings["SC Layout"]["original_file"]
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
    new_xml_path = settings["SC Layout"]["modified_layout_name"]
    mod_divices_dict = devices.copy()
    pprint.pprint(mod_divices_dict)
    moded_devices = {"ProfilName": new_xml_path}
    for input_device in settings["inputs"]:
        # If UUID is the same and original xml Instance is different to instance from settings
        if settings["inputs"][input_device]["uuid"] == \
                mod_divices_dict[settings["inputs"][input_device]["old_instance_nr"]]["uuid"] and \
                settings["inputs"][input_device]["new_instance_nr"] != \
                int(mod_divices_dict[settings["inputs"][input_device]["old_instance_nr"]]["instance"]):
            # print(f'Inpu Dev {input_device} als Sett {settings["inputs"][input_device]}:\n'
            #       f'sett nr old: {settings["inputs"][input_device]["old_instance_nr"]}'
            #       f' insta nr old: {mod_divices_dict[settings["inputs"][input_device]["old_instance_nr"]]["instance"]} \n '
            #       f' sett new nr: {settings["inputs"][input_device]["new_instance_nr"]}')

            moded_devices[settings["inputs"][input_device]["old_instance_nr"]] = \
                {
                    "Product": f'{input_device.split("_")[:-1][0] if "_" in input_device else input_device}  '
                               f'{mod_divices_dict[settings["inputs"][input_device]["old_instance_nr"]]["uuid"]}',
                    "Instance": settings["inputs"][input_device]["new_instance_nr"],

                }

            # todo hier das dict bauen

            # set_devices_instance(mod_divices_dict, settings["SC Layout"]["original_file"])
    print(moded_devices)


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
        # save_settings()

    if event == "Reload Xml":
        xml_file_path = reload_xml(values)
        load_xml_layout(xml_file_path)
        load_window_layout()

    # calc inputs
    if event == "check_inputs":
        checked = True
        check_inputs(values)

    # New Layout Name
    if event == "save_mod_name":
        settings["SC Layout"]["modified_layout_name"] = values['mod_name']
        window["mod_name"].update(settings["SC Layout"].get("modified_layout_name"))
        save_settings()
    if event == "Browse":
        print("browse")
    if event == "Save":
        if checked:
            write_to_xml()
            checked = False
        else:
            sg.popup(f"You need to check the inputs first\nPress 'Check Inputs' to continue")

window.close()
