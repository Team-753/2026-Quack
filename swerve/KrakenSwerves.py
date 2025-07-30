import phoenix6
from wpimath import kinematics, geometry
import wpilib
import math
from phoenix6 import hardware, controls, signals, configs
import RobotConfig as rc

class SwerveModule:

# this class defines our wheels, the swerve modules and some ways we can control them.
    def __init__(self, driveID: int, turnID: int, coderID: int, coderOffset: float, invertedness: bool) -> None:
        
        self.driveMotor = hardware.TalonFX(driveID)
        self.turnMotor = hardware.TalonFX(turnID)
        self.canCoder = hardware.CANcoder(coderID)
        self.encoderOffset = coderOffset
        self.inverted = invertedness
        
#  _____       _             __  __       _                _____             __ _       
# |  __ \     (_)           |  \/  |     | |              / ____|           / _(_)      
# | |  | |_ __ ___   _____  | \  / | ___ | |_ ___  _ __  | |     ___  _ __ | |_ _  __ _ 
# | |  | | '__| \ \ / / _ \ | |\/| |/ _ \| __/ _ \| '__| | |    / _ \| '_ \|  _| |/ _` |
# | |__| | |  | |\ V /  __/ | |  | | (_) | || (_) | |    | |___| (_) | | | | | | | (_| |
# |_____/|_|  |_| \_/ \___| |_|  |_|\___/ \__\___/|_|     \_____\___/|_| |_|_| |_|\__, |
#                                                                                  __/ |
#                                                                                 |___/                                  
    
        driveMotorConfigs = phoenix6.configs.TalonFXConfiguration() # class containing settings for the drive motor

        driveMotorConfigs.slot0.k_p = 1
        driveMotorConfigs.slot0.k_i = 0.0
        driveMotorConfigs.slot0.k_d = 0.0
        driveMotorConfigs.slot0.k_s = 0.11
        driveMotorConfigs.slot0.k_v = 0.12
        #These are the pid configs for the drive motor. they are mostly default values. they are used to control the acceleration curve of the drive motor through an algorythmn that compares how fast the wheel is going with how fast we want it to go. if you need more help with this wpi and ctre have some resources

        driveMotorConfigs.voltage.peak_forward_voltage = 13
        driveMotorConfigs.voltage.peak_reverse_voltage = -13
        driveMotorConfigs.current_limits.supply_current_limit = 38 # Not quite sure what this does, but it can help to reduce brownouts
        driveMotorConfigs.motor_output.neutral_mode = signals.NeutralModeValue.COAST # when we arent trying to do anything with the motor we set it to coast mode, which stops the motor but allows the shaft to rotate freely, which doesnt let the motor stall
        
        driveMotorConfigs.feedback.sensor_to_mechanism_ratio = rc.SwerveModules.drivingGearRatio #telling the motor how many spins of the motor per desired mechanism output spin. this way we can talk to it in mechanism spins, rather than having to do that math later

        self.driveMotor.configurator.apply(driveMotorConfigs) #sending the config to the drive motor

#  _______                 __  __       _                _____             __ _       
# |__   __|               |  \/  |     | |              / ____|           / _(_)      
#    | |_   _ _ __ _ __   | \  / | ___ | |_ ___  _ __  | |     ___  _ __ | |_ _  __ _ 
#    | | | | | '__| '_ \  | |\/| |/ _ \| __/ _ \| '__| | |    / _ \| '_ \|  _| |/ _` |
#    | | |_| | |  | | | | | |  | | (_) | || (_) | |    | |___| (_) | | | | | | | (_| |
#    |_|\__,_|_|  |_| |_| |_|  |_|\___/ \__\___/|_|     \_____\___/|_| |_|_| |_|\__, |
#                                                                                __/ |
#                                                                               |___/ 
                                                        
        turnMotorConfigs = phoenix6.configs.TalonFXConfiguration() #class containing configs for the turn motor

        turnMotorConfigs.slot1.k_p = 7.2
        turnMotorConfigs.slot1.k_i = 2.4
        turnMotorConfigs.slot1.k_d = 0.0001
        turnMotorConfigs.slot1.k_s = 0.01
        #same as in the drive motor configs, but with slightly different values because we are comparing current position with desired position, instead of comparing velocities. Tune these values with the robot (or test bot) on the ground. If youve got the test bot, i reccomend sticking a weight on it (50lb?) to better simulate the real robot and give you a better impression of the amount of oscillation you will actually see

        turnMotorConfigs.voltage.peak_forward_voltage = 13
        turnMotorConfigs.voltage.peak_reverse_voltage = -13
        #literally the exact same as the purpose of these configs in the drive motor, reduce brownouts

        turnMotorConfigs.feedback.feedback_remote_sensor_id = coderID #tells the turn motor to use the encoder at the specified place on the CAN chain rather than its built in encoder. This lets us use the CAN coders
        turnMotorConfigs.feedback.feedback_sensor_source = signals.FeedbackSensorSourceValue.REMOTE_CANCODER #tells the motor that it will be looking at a CAN coder at that specified place on the can chain. also tells it to always use the can coder instead of the built in encoder
        turnMotorConfigs.motor_output.neutral_mode = signals.NeutralModeValue.COAST #when were not trying to do anything, dont move, but the shaft can move cause stalling the motor out is bad
        turnMotorConfigs.closed_loop_general.continuous_wrap = True # the motor controls something that goes around in a circle (as opposed to an elevtor), sp 0 and 2pi are the same. Step one of minimizing turning of the wheels.
        

        turnMotorConfigs.current_limits.supply_current_limit = 38 #find a real number for this

        self.turnMotor.configurator.apply(turnMotorConfigs) #send the turn motor configs to the turn motor
        
#   _____             _____          _                  _____             __ _       
#  / ____|           / ____|        | |                / ____|           / _(_)      
# | |     __ _ _ __ | |     ___   __| | ___ _ __ ___  | |     ___  _ __ | |_ _  __ _ 
# | |    / _` | '_ \| |    / _ \ / _` |/ _ \ '__/ __| | |    / _ \| '_ \|  _| |/ _` |
# | |___| (_| | | | | |___| (_) | (_| |  __/ |  \__ \ | |___| (_) | | | | | | | (_| |
#  \_____\__,_|_| |_|\_____\___/ \__,_|\___|_|  |___/  \_____\___/|_| |_|_| |_|\__, |
#                                                                               __/ |
#                                                                              |___/ 
                                                    
        canCoderConfigs = phoenix6.configs.CANcoderConfiguration() #a class that stores settings for the CANcoders
        
        canCoderConfigs.magnet_sensor.absolute_sensor_discontinuity_point = 1 # sets the cancoder to count from 0 to 2pi, rather than -pi to pi, which is compatible with other libraries better
        canCoderConfigs.magnet_sensor.magnet_offset = self.encoderOffset # sets the zero position of the CAN coder to be the zero position that we want it to be, not the semi-arbitrary default. This lets us have all the wheels line up with the robot chassis by default, and lets us drive
        canCoderConfigs.magnet_sensor.sensor_direction = signals.SensorDirectionValue.CLOCKWISE_POSITIVE #can coder invert, I did this so that the wheels would align to spin the robot when the z axis on the joystick was manipulated, otherwise they made an x
        
        self.canCoder.configurator.apply(canCoderConfigs) # sending the settings to the CANcoder
        

#  _______          _     
# |__   __|        | |    
#    | | ___   ___ | |___ 
#    | |/ _ \ / _ \| / __|
#    | | (_) | (_) | \__ \
#    |_|\___/ \___/|_|___/
                        
    
    
    def getTurnWheelState(self)-> geometry.Rotation2d:
        """Returns the current position of the turn motor in radians"""
        #what is the angle of the wheel?
        return geometry.Rotation2d(self.turnMotor.get_position().value * (math.tau))
    
    
    
    
    
    
    def setState(self, optimizedDesiredState: kinematics.SwerveModuleState)-> None:
        #getting the wheel to where we want it to be
        optimizedDesiredState.optimize(geometry.Rotation2d(self.turnMotor.get_position().value)) #This fuction, along with the continuous wrap being set to true in the config for the turn motor ensures that the wheel never turns more than 90 degrees relative to the robot chassis. This line in particular lets us invert the direction of the drive motor to make it seem like it had turned an additional 90 degrees
        
        driveMotorVelocity = optimizedDesiredState.speed # getting the speed we should set the motor to from the optimized desired state object and saving it to its own variable
        
        turnMotorPosition = optimizedDesiredState.angle.radians() / math.tau # getting the desired angle from the optimized desired state and saving it as its own variable
        
        self.driveMotor.set_control(self.velocity.with_velocity(driveMotorVelocity)) #setting the drive motor to go to the desired velocity
        
        self.turnMotor.set_control(self.position.with_position(turnMotorPosition)) #setting the turn motor to the desired position
    
    
    
    
    
    
    

    def brake(self):
        self.driveMotor.set_control(self.brake)
        self.turnmotor.set_control(self.brake)
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
