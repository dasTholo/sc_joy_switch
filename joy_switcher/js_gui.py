import pprint

import PySimpleGUI as sg

from joy_switcher.layouter import get_all_devices

sg.theme('DarkAmber')
# if settings not set pop browsfile, create ini
settings = sg.UserSettings('./config.ini', use_config_file=True, convert_bools_and_none=True)

xml_file_path = settings["SC Layout"]["orginal_file"]
layout = [[sg.Text('Orginal SC Layout XML'),
           sg.Input(xml_file_path.split(sep="/")[-1:], key='-IN-'),
           sg.FileBrowse(file_types=(("XLM file", "*.xml"),), key="Browse")],
          [sg.Text('New SC Layout XML Name'),
           sg.Input(key='mod_name', default_text=settings["SC Layout"].get("modified_layout_name", "")),
           sg.Button('Save', key="save_mod_name")],
          [sg.Button('Load Xml'), sg.Button('Cancel')]]

window = sg.Window('Joy Switcher', layout)


def load_xml_layout(orginal_file):
    devices = get_all_devices(orginal_file)
    # pprint.pprint(devices, indent=4)
    return devices


def load_window_layout(devices):
    global window

    table = [[sg.Text(f"Instance {i}:"),
              sg.Text(devices[i]["name"], key=f"btn{i}"), sg.Text(f"Change to:"),
              sg.Combo([i for i in range(1, len(devices) + 1)], default_value=devices[i]["instance"]),
              sg.Button(f"test{i}")] for i in
             range(1, len(devices) + 1)]

    layout = [[sg.Text('Orginal SC Layout XML'),
               sg.Input(xml_file_path.split(sep="/")[-1:], key='-IN-'),
               sg.FileBrowse(file_types=(("XLM file", "*.xml"),))],
              [sg.Text('New SC Layout XML Name'),
               sg.Input(key='mod_name', default_text=settings["SC Layout"].get("modified_layout_name", "")),
               sg.Button('Save', key="save_mod_name")],
              [sg.Frame("Inputs", layout=table)],
              [sg.Button('Reload Xml')],
              [sg.Button('Save', key="Save"), sg.Button('Cancel')]]
    window1 = sg.Window('Joy Switcher', layout)
    window.close()
    window = window1


def reload_xml(values):
    global xml_file_path
    if values.get("Browse", None) != "":
        settings["SC Layout"].set('orginal_file', values["Browse"])
        xml_file_path = settings["SC Layout"]["orginal_file"]
    else:
        xml_file_path = settings["SC Layout"]["orginal_file"]
    return xml_file_path


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
        devices = load_xml_layout(xml_file_path)
        load_window_layout(devices)

    if event == "Reload Xml":
        xml_file_path = reload_xml(values)
        devices = load_xml_layout(xml_file_path)
        load_window_layout(devices)

    # New Layout Name
    if event == "save_mod_name":
        if ".xml" in settings["SC Layout"].get("modified_layout_name") and ".xml" in values['mod_name']:
            settings["SC Layout"].set("modified_layout_name", values['mod_name'])
        else:
            settings["SC Layout"].set("modified_layout_name", f"{values['mod_name']}.xml")
        window["mod_name"].update(settings["SC Layout"].get("modified_layout_name"))
    if event == "Browse":
        print("browse")
    if event == "Save":
        pass
    #     settings["SC Layout"].set('orginal_file', values['-IN-'])

window.close()
