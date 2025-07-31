from swerveSubsys import driveTrainCommand,joystickSubsys,driveTrainSubsys,hotasSubsys
import wpilib,commands2
class robotContainer():
    def __init__(self):
        self.controller=commands2.button.CommandJoystick(1)
        #Declare Subystems
        self.driveSubsystem=driveTrainSubsys()
        self.joystick=hotasSubsys(self.controller)
        #self.joystick.setDefaultCommand(testDefCommand(self.joystick))
        self.driveSubsystem.setDefaultCommand(driveTrainCommand(self.driveSubsystem,self.joystick))
        print("containerInited")
        self.buttonBindings()
    def buttonBindings(self):
        print("bindings configed")