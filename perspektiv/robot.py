
import numpy as np



class Robot():

    def __init__(self, L1, L2):
        self.L1 = L1
        self.L2 = L2

    def forward_kinematics(self, theta1, theta2):
        x = self.L1 * np.cos(theta1) + self.L2 * np.cos(theta1 + theta2)
        y = self.L1 * np.sin(theta1) + self.L2 * np.sin(theta1 + theta2)
        return x, y
    
    def calculate_joint_positions(self, base_x, base_y, angle1, angle2):
        x1 = self.L1 * np.cos(angle1)
        y1 = self.L1 * np.sin(angle1)
        x2 = x1 + self.L2 * np.cos(angle1 + angle2)
        y2 = y1 + self.L2 * np.sin(angle1 + angle2)
        return (x1, y1), (x2, y2)
    
    def inverse_kinematics(self, x, y):

        d = np.sqrt(x**2+y**2)
        if d > self.L1+self.L2:
            print("Position out of reach")
            return None, None
        
        # calculate theta2
        theta2 = np.pi-np.arccos((-d**2+self.L1**2+self.L2**2)/(2*self.L1*self.L2))
        
        # Calculate theta1
        thetah = np.arctan2(y, x)
        thetai = np.arccos((-self.L2**2+self.L1**2+d**2)/(2*self.L1*d))
        theta1 = thetah - thetai
        return theta1, theta2
    


if __name__ == "__main__":
    robot = Robot(1, 1)
    x, y = robot.forward_kinematics(np.pi/4, 2*np.pi-np.pi/4)
    print(x, y)
    theta1, theta2 = robot.inverse_kinematics(x, y)
    print(theta1, theta2)
    x, y = robot.forward_kinematics(theta1, theta2)
    print(x, y)
