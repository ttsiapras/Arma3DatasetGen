
![Logo](https://www.paulthetall.com/wp-content/uploads/2017/04/arma-3-banner.jpg)


## Authors
Originally developed by
- [@cloftus96](https://github.com/cloftus96)
Modified By
- [@ttsiapras](https://github.com/ttsiapras)
# Using Arma 3 to Generate Synthetic Data

This README details how python and Arma 3 script(s) are used to
generate data for a Neural Network using the editor from the
game Arma 3. It also gives system requirements and many 
other changes that must be made by the user in order for the
python script to run.

## Description
The intention of this script is to create images to further 
develop a neural network. The script generates roughly 
20,000+ images in different environment settings and locations,
from multiple different angles. Some examples of different 
environments are fog, sun, rain, etc.

The Python script starts by writing the Arma 3 script. This
script will get stored in a separate file for later use. It
then opens the game on the system and navigates through the
menu to the editor using an autoclick function. After getting
to the editor, an Arma 3 "mission" is then
run. This mission will be the Arma 3 script that was created at the
start of the python script. This Arma 3 script will generate the object that the neural
network needs pictures of, and start taking screenshots of it.
Then, the Python script will run in the background, and
manage the screenshots created by putting them in an
appropriate folder. Once all of the pictures have been taken,
Python then closes the game and exits.

### Usage
Example usage
```bash
python Data_Generation_Main.py [[6258.016,5474.695,0],[5998.337,4960.8,0]] ['B_CTRG_LSV_01_light_F','B_GEN_Van_02_transport_F'] 120 361 3 50 0.5 12 50
```
Arguments
1. *Map position list* - This is the list of all map locations to simulate as a list of ordered triples.
These **must** be typed as a Pythonic list with each ordered triple as a Pythonic list *or* tuple. No spaces.
2. *Vehicle name list* - This is a list of all in-game vehicles to simulate. This is a
list of strings. These **must** be typed as a Pythonic list of strings. The strings must be
quoted (either single or double is fine). No spaces within this list.
3. *Camera rotation angle step* - The angle step in the XY plane by which to rotate the camera around the
vehicle between each image.
4. *Vehicle rotation angle step* - The angle step by which to rotate the vehicle with respect to its
previous oritnetation.
5. *Cam commit time* - The number of seconds it takes to move the camera to the next position. Note
that this has **not** been tested with values less than 2. If this value is too low, image file
management may not work as intended.
6. *Camera XY position offset* - The radius of the circle in the XY plane about which to rotate the
camera.
7. *Fog increment* - The change in level of fog between each simulated fog setting. Simulated fog values
can be between 0 and 0.8.
8. *Time of day increment* - The change in time of day between each time of day setting. Time of day values
range from 6:00 to 19:30. An example (including partial hours): 1.5 = 1 hour 30 minutes between
each time setting.
9. *Camera Z offset* - The number of units off the ground the camera will be when taking the pictures.
For large vehicles (like tanks) this can be up to 100. For smaller civilian vehicles this is best
limited to something around 50. This can vary depending on the kind of image data desired.

### Notes
In order for the script to work correctly:
- Python 3.7 must be installed, preferably to the path %HOMEDIRECTORY%\Python37.
    - This is the version that the script was tested on. The
    script is not guaranteed to work on any other version.
- This script also uses MATLAB 2018b. It is **imperative** that
this **specific version** is installed, as the script uses a function
that only this version has.
- The game Arma 3 **AND** Steam must **BOTH** be installed **and** updated. 
If the game or Steam is not updated, the sleep times will be
off due to updates.
- Before running this project, run the game Arma 3 once
beforehand, and ensure two things:
    - all necessary licenses have been accepted.
    - resolution is changed to whatever is native, and the
    game changed to fullscreen
- Make sure that the game Arma 3 is **closed** before running
this project. Having two copies of the game open may cause
unnecessary lag.
- Some times of day are so dark that nothing can be seen
(the times we believe are roughly from 12am-5am). There is
a night vision mode in the game, but it is not implemented
for this project.
- Current supported resolutions are 1920x1080, and 1366x768.
More resolutions may be added in the future.
- The script moves the screenshots to this folder:

    %HOMEDIRECTORY%\Users\\%MainUser%\Documents\SyntheticDataGen

  Ensure before running the script that this directory is either
  empty or non-existent. **IMPORTANT: The user should move all data** 
  **out of this folder when done to avoid having data overwritten by a**
  **future execution.**

### Error Codes
- Error Code 0: Script ran as intended
- Error Code 2: Resolution unsupported by script
- Error Code 3: Issue with .sqf file creation
- Error Code 4: Issue with the file merging process

## Necessary Installations
Use these commands in the Windows terminal to install required
packages:

```windows
python -m pip install pyautogui
python -m pip install pypiwin32
```

It is recommended to run this command before you install 
these two packages:

```windows
python -m pip install --upgrade pip
```

*Note: depending on where your python is installed or what
exact version you have, you may need to use the command "py"
instead of "python."*

If you have the python terminal open instead, use these commands:

```
install pyautogui
install pypiwin32
```



## Examples
Here are some examples of the data that this script creates:
![example](https://github.com/ttsiapras/Arma3DatasetGen/blob/5fb228f1064fd3adf18aaeaba4f670e53ee9711c/readme_images/result.png)
