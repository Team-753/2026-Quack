import commands2

class MyRobot(commands2.TimedCommandRobot):
    def __init__(self, period=.02):
        super().__init__(period)


    #Please note, various periodic commands are not in this file. Please refer to the docs if you want periodic comamands. 

    def robotInit(self):
        pass
    
    def autonomousInit(self):
        """Code run at the start of auto. This currently figures out what the robot is doing for auto"""
        pass
    

    def teleopInit(self):
        pass

          

    def disabledInit(self):
        pass
    
    
    