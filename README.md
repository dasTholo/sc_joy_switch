## SC Joy Switch
This Tool will allow you to switch the Joystick Instances at your exported Star Citizen layout file.
You can change the number of instances and save as a new layout xml file.

# First Start
- Get the executable File from the release Site
- Start the exe, where you want
- Press Browse and get your last Star Citizen layout file

![start_image.png](doc_images%2Fstart_image.png)

- Set new Layout in next Text Field and press Save

![new_layout_name.png](doc_images%2Fnew_layout_name.png)
- Press Load Xml

![joystick_list.png](doc_images%2Fjoystick_list.png)

- Grab the numbers to change the instance number
- Press "Reload Xml" to return or Press "Check Inputs" to test the sequence
- To Finish press "Save"
  - This will write the new layout file, with the new layout name ```layout_new_name_exported.xml```, to the SC folder
- Change to Star Citizen, at console type ```pp_RebindKeys``` and ```pp_RebindKeys layout_new_name_exported.xml```
- Ready to Fly! Have Fun!


# todo
- add cli to layouter for Joystick Gremlin Support



## Dependencies
- [lxml](https://lxml.de/)
- [pysimplegui](https://www.pysimplegui.org/en/latest/)
### Dev Dependencies
- [Nuitka](https://nuitka.net/) File creation

```python -m nuitka --onefile --enable-plugin=tk-inter --windows-disable-console .\joy_switcher\js_gui.py```

# Thanks to
**Big Thanks to Mille S'Abor** for the init idea of this project

Thanks to lxml and pysimplegui to deploy this