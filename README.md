# PythonMujoco

I was using Python in my reasearch and I had to use Mujoco Haptix. Since I couldn't find a python interface I decided to write my own. I only ported the Haptix api, I have plans to port the rest of the functions in a close future.

I added an example file, but here it is the main steps:

1- import PythonMujoco
2- Init the class passing the path to the mujoco dll
3- create the HxCommand, HxSensor, HxRobotInfo struct
4- update the HxRobotInfo struct by calling hx_robot_info() function
5- send the commands by calling function hx_update

If you need help or have comments please contact me.

Hope this helps you,

Henrique Dantas
dantash@oregonstate.edu

