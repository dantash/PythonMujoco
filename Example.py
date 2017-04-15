# EXAMPLE OF HOW TO USE PythonMujoco TO UPDATE MUJOCO POSITION
# FOR MORE INFORMATION ABOUT THE API VISIT http://www.mujoco.org/book/haptix.html 

import PythonMujoco

command = PythonMujoco.HxCommand()
command.ref_pos_enabled = 1
command.ref_pos[0] = -1.57

sensor = PythonMujoco.HxSensor()
robot_info = PythonMujoco.HxRobotInfo()

# Declare Function

mj_lib = PythonMujoco.MjHxInterface("YOUR PATH TO mjhaptix_user.dll")

try:
    mj_lib.hx_connect('', 0)
    print 'Mujoco opened'
    robot_info = mj_lib.hx_robot_info(robot_info)
    mj_lib.hx_update(command, sensor)
    print sensor1.joint_pos[0]
except Exception as inst:
    print(type(inst))    # the exception instance
    print(inst.args)     # arguments stored in .args
    print(inst)
finally:
    mj_lib.hx_close()
