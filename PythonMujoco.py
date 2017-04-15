from ctypes import c_float, POINTER, Structure, cdll, c_int, byref, c_char_p
# import timeit

hxMAXMOTOR = 32
hxMAXCONTACTSENSOR = 32
hxMAXIMU = 32
hxMAXJOINT = 32
mjMAXSZ = 1000


class HxCommand(Structure):
    """ creates a struct to match HxCommand """

    _fields_ = [('ref_pos', c_float*hxMAXMOTOR),
                ('ref_pos_enabled', c_int),
                ('ref_vel', c_float*hxMAXMOTOR),
                ('ref_vel_enabled', c_int),
                ('gain_pos', c_float*hxMAXMOTOR),
                ('gain_pos_enabled', c_int),
                ('gain_vel', c_float*hxMAXMOTOR),
                ('gain_vel_enabled', c_int)]

    def __init__(self):
        data_init = [0.0] * hxMAXMOTOR
        self.ref_pos = (c_float * hxMAXMOTOR)(*data_init)
        self.ref_vel = (c_float * hxMAXMOTOR)(*data_init)
        self.gain_pos = (c_float * hxMAXMOTOR)(*data_init)
        self.gain_vel = (c_float * hxMAXMOTOR)(*data_init)

class MjState(Structure):
    """ creates a struct to match MjState """

    _fields_ = [('nq', c_int),
                ('nv', c_int),
                ('na', c_int),
                ('time', c_float),
                ('qpos', c_float*mjMAXSZ),
                ('qvel', c_float*mjMAXSZ),
                ('act', c_float*mjMAXSZ)]

    def __init__(self):
        data_init = [0.0] * mjMAXSZ
        self.qpos = (c_float * mjMAXSZ)(*data_init)
        self.qvel = (c_float * mjMAXSZ)(*data_init)
        self.act = (c_float * mjMAXSZ)(*data_init)


class HxTime(Structure):
    """ creates a struct to match HxTime """

    _fields_ = [('sec', c_int),
                ('nsec', c_int)]


class HxSensor(Structure):
    """ creates a struct to match HxSensor """

    _fields_ = [('time_stamp', HxTime),
                ('motor_pos', c_float*hxMAXMOTOR),
                ('motor_vel', c_float*hxMAXMOTOR),
                ('motor_torque', c_float*hxMAXMOTOR),
                ('joint_pos', c_float*hxMAXJOINT),
                ('joint_vel', c_float*hxMAXJOINT),
                ('contact', c_float*hxMAXCONTACTSENSOR),
                ('imu_linear_acc', c_float*3*hxMAXIMU),
                ('imu_angular_vel', c_float*3*hxMAXIMU),
                ('imu_orientation', c_float*4*hxMAXIMU)]

    def __init__(self):
        data_init = [0.0] * hxMAXMOTOR
        data_init2 = [tuple([0.0] * 3)] * hxMAXIMU
        data_init3 = [tuple([0.0] * 4)] * hxMAXIMU
        self.time_stamp = HxTime()
        self.motor_pos = (c_float * hxMAXMOTOR)(*data_init)
        self.motor_vel = (c_float * hxMAXMOTOR)(*data_init)
        self.motor_torque = (c_float * hxMAXMOTOR)(*data_init)
        self.joint_pos = (c_float * hxMAXJOINT)(*data_init)
        self.joint_vel = (c_float * hxMAXJOINT)(*data_init)
        self.imu_linear_acc = (c_float * 3 * hxMAXIMU)(*data_init2)
        self.imu_angular_vel = (c_float * 3 * hxMAXIMU)(*data_init2)
        self.imu_orientation = (c_float * 4 * hxMAXIMU)(*data_init3)

class HxRobotInfo(Structure):
    """ creates a struct to match HxRobotInfo """
    _fields_ = [('motor_count', c_int),
                ('joint_count', c_int),
                ('contact_sensor_count', c_int),
                ('imu_count', c_int),
                ('motor_limit', c_float*2*hxMAXJOINT),
                ('joint_limit', c_float*2*hxMAXJOINT),
                ('update_rate', c_float)]

    def __init__(self):
        data_init = [0.0] * mjMAXSZ
        self.qpos = (c_float * mjMAXSZ)(*data_init)
        self.qvel = (c_float * mjMAXSZ)(*data_init)
        self.act = (c_float * mjMAXSZ)(*data_init)

class MjHxInterface(object):
    def __init__(self, path):
        mjDll = cdll.LoadLibrary(path)
        # Define functions of MJ Haptix
        self.function_hx_update = mjDll.hx_update
        self.function_hx_update.argtypes = [POINTER(HxCommand), POINTER(HxSensor)]
        self.function_hx_update.restype = c_int

        self.function_hx_last_result = mjDll.hx_last_result
        self.function_hx_last_result.argtypes = None
        self.function_hx_last_result.restype = c_char_p

        self.function_hx_read_sensors = mjDll.hx_read_sensors
        self.function_hx_read_sensors.argtypes = [POINTER(HxSensor)]
        self.function_hx_read_sensors.restype = c_int

        self.function_hx_robot_info = mjDll.hx_robot_info
        self.function_hx_robot_info.argtypes = [POINTER(HxRobotInfo)]
        self.function_hx_robot_info.restype = c_int

        self.function_hx_connect = mjDll.hx_connect
        self.function_hx_connect.argtypes = [c_char_p, c_int]
        self.function_hx_connect.restype = c_int

        self.function_hx_close = mjDll.hx_close
        self.function_hx_close.argtypes = None
        self.function_hx_close.restype = c_int

        self.function_mj_get_state = mjDll.mj_get_state
        self.function_mj_get_state.argtypes = [POINTER(MjState)]
        self.function_mj_get_state.restype = c_int

    def hx_connect(self, ip, port):
        return self.function_hx_connect(ip, port)

    def hx_robot_info(self, robot_info):
        self.function_hx_robot_info(byref(robot_info))
        return robot_info

    def hx_update(self, command, sensor):
        self.function_hx_update(byref(command), byref(sensor))
        return sensor

    def hx_close(self):
        self.function_hx_close()

    def hx_read_sensors(self, sensor):
        self.function_hx_read_sensors(byref(sensor))
        return sensor
