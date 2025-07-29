#Joystick and Aux Controller
class Joystick:
    USB_ID = 0 #USB ID for the joystick, this is the one that is used by the driver station
    xDeadband = 0.1 #deadband in the x of the joystick
    yDeadband = 0.1 #deadband on the y of the joystick
    thetaDeadband = 0.2 #deadband for theta of the joystick


class AuxController:
    USB_ID = 1

# Robot
class robotDimensions:
    width = 0.7366 #pretty sure this is the width between swerve modules
    length = 0.7366 #prolly length between modules

# Swerve Modules
class SwerveModules: 
    drivingGearRatio: 0 #gear ratio for the driving motor
    turningGearRatio: 0 #gear ratio for the turning motor
    wheelDiameter: 0 #diameter of the wheel in meters

    class frontRight:
        moduleName = "Front Right"
        drivingMotorID = 0 # ID for the driving motor
        turningMotorID = 0 # ID for the turning motor
        turningEncoderID = 0 # ID for the turning encoder
        turningEncoderOffset = 0.0 # Offset for the turning encoder

    class frontLeft:
        moduleName = "Front Left"
        drivingMotorID = 0 # ID for the driving motor
        turningMotorID = 0 # ID for the turning motor
        turningEncoderID = 0 # ID for the turning encoder
        turningEncoderOffset = 0.0 # Offset for the turning encoder

    class backRight:
        moduleName = "Back Right"
        drivingMotorID = 0 # ID for the driving motor
        turningMotorID = 0 # ID for the turning motor
        turningEncoderID = 0 # ID for the turning encoder
        turningEncoderOffset = 0.0 # Offset for the turing encoder

    class backLeft:
        moduleName = "Back Left"
        drivingMotorID = 0 # ID for the driving motor
        turningMotorID = 0 # ID for the turning motor
        turningEncoderID = 0 # ID for the turning encoder
        turningEncoderOffset = 0.0 # Offset for the turning encoder

#Vision
class Vision: 
    
    class limelight: 
        limelightName = "Limelight Name Placeholder"
        
    class protonCamera:
        protonCameraName = "Proton Camera Name Placeholder"

#Pneumatics
class Pneumatics: 
    pass