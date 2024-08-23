import pygame
import math
import robot
import numpy as np

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Robot Arm with Two Joints")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

robot = robot.Robot(1.2, 0.9)

# Initialize variables
base_x, base_y = WIDTH // 2, HEIGHT // 2+100  # Base position of the robot
length1, length2 = robot.L1*100, robot.L2*100  # Lengths of the arm segments
angle1, angle2 = np.pi/4, np.pi/4  # Angles in degrees
goal_angle1, goal_angle2 = angle1, angle2

# Base of robot
base_size_x = 40
base_size_y = 20

# Thickness of robot segments
segment_thickness = 7


# Function to calculate the end positions of the arm segments
def calculate_positions(base_x, base_y, angle1, angle2, length1, length2):
    x1 = base_x + length1 * math.cos(angle1)
    y1 = base_y - length1 * math.sin(angle1)
    x2 = x1 + length2 * math.cos(angle1 + angle2)
    y2 = y1 - length2 * math.sin(angle1 + angle2)
    return (x1, y1), (x2, y2)

_ , initial_position = calculate_positions(base_x, base_y, angle1, angle2, length1, length2)

def update_robot(goal_angle1, goal_angle2, angle1, angle2, increment=0.01):
    # Update angles
    if goal_angle1 > angle1+increment:
        angle1 += increment
    elif goal_angle1 < angle1-increment:
        angle1 -= increment
    else:
        angle1 = goal_angle1
    
    if goal_angle2 > angle2+increment:
        angle2 += increment
    elif goal_angle2 < angle2-increment:
        angle2 -= increment
    else:
        angle2 = goal_angle2
    
    x1 = base_x + length1 * math.cos(angle1)
    y1 = base_y - length1 * math.sin(angle1)
    x2 = x1 + length2 * math.cos(angle1 + angle2)
    y2 = y1 - length2 * math.sin(angle1 + angle2)
    return (x1, y1), (x2, y2), angle1, angle2


def draw_robot(joint1_pos, joint2_pos, angle1, angle2):
     # Draw base
    pygame.draw.rect(window, BLUE, (base_x-base_size_x/2, base_y, base_size_x, base_size_y))

    # Draw first segment
    pygame.draw.line(window, BLACK, (base_x, base_y), joint1_pos, segment_thickness)

    # Draw second segment
    pygame.draw.line(window, BLACK, joint1_pos, joint2_pos, int(segment_thickness*0.8))

    # Draw joints
    pygame.draw.circle(window, BLUE, joint1_pos, 5)
    pygame.draw.circle(window, BLUE, joint2_pos, 5)

    # Draw angle arcs
    # Arc for the first angle
    pygame.draw.arc(
        window, RED,
        (base_x - 50, base_y - 50, 100, 100),  # arc rectangle
        0, angle1, 2  # start angle, stop angle, and width of arc
    )

    # Arc for the second angle
    pygame.draw.arc(
        window, RED,
        (joint1_pos[0] - 50, joint1_pos[1] - 50, 100, 100),  # arc rectangle
        angle1, angle2 + angle1, 5  # start angle, stop angle, and width of arc
    )


# Set up font for rendering text
font = pygame.font.SysFont("Arial", 24)


# Initialize text input variables
input_text = ""
input_rect = pygame.Rect(10, 40, 200, 50)
input_active = False

# Text next to the input box
instruction_text = font.render(
    "Enter 2 new angles (e.g., 30, 60):", True, BLACK
)
instruction_rect = instruction_text.get_rect(topleft=(10, 10))

# Cursor variables
cursor_width = 2
cursor_color = BLACK
cursor_blink_interval = 500  # in milliseconds
cursor_last_toggle = pygame.time.get_ticks()
cursor_visible = True


# Function for drawing the input box
def draw_input_box():
    pygame.draw.rect(window, BLACK, input_rect, 2)
    text_surface = font.render(input_text, True, BLACK)
    window.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

    # Draw the instruction text
    window.blit(instruction_text, instruction_rect.topleft)

    # Draw the cursor if the input box is active and the cursor is visible
    if input_active and cursor_visible:
        cursor_x = (
            input_rect.x + 5 + text_surface.get_width()
        )  # Cursor position at the end of the text
        pygame.draw.line(
            window,
            cursor_color,
            (cursor_x, input_rect.y + 5),
            (cursor_x, input_rect.y + input_rect.height - 5),
            cursor_width,
        )

    # Draw the angles text box
    pygame.draw.rect(window, BLACK, angles_box, 2)
    angles_surface = font.render(angles_text, True, BLACK)
    window.blit(angles_surface, (angles_box.x + 5, angles_box.y + 5))

    # Draw the position text box
    pygame.draw.rect(window, BLACK, position_box, 2)
    position_surface = font.render(position_text, True, BLACK)
    window.blit(position_surface, (position_box.x + 5, position_box.y + 5))



def rad_to_deg(radians):
    return round(radians * 180 / math.pi, 0)

def deg_to_rad(degrees):
    return round(degrees * math.pi / 180, 9)

# Initialize angles text box variables
angles_box = pygame.Rect(10, 560, 330, 32)
angles_text = f"Current angles: {rad_to_deg(angle1), rad_to_deg(angle2)}"

# Initialize position text box variables
position_box = pygame.Rect(450, 560, 330, 32)
position_text = f"Current positioin: {round(initial_position[1]/100,2), round(initial_position[0]/100,2)}"


# Setup the clock
clock = pygame.time.Clock()
running = True

while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the user clicks on the input box
            if input_rect.collidepoint(event.pos):
                input_active = not input_active
            else:
                input_active = False
        elif event.type == pygame.KEYDOWN:
            # Capture key events when the input box is active
            if input_active:
                # Add blinking line to input box

                if event.key == pygame.K_RETURN:
                    try:
                        # Attempt to convert the entered text to a numpy array of floats
                        angles = np.array(
                            [deg_to_rad(float(x)) for x in input_text.split(",")]
                        )
                        if len(angles) != 2:
                            print("Invalid input. Please enter two angles.")
                        else:
                            goal_angle1, goal_angle2 = angles
                        angles_text = (
                            f"Current angles: {rad_to_deg(goal_angle1), rad_to_deg(goal_angle2)}"
                        )
                    except ValueError:
                        angles_text = (
                            "Invalid input. Please enter valid 3D coordinates."
                        )
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
        elif event.type == pygame.QUIT:
            running = False


    # Clear the screen
    window.fill(WHITE)

    # Draw the input box
    draw_input_box()

    # Update robot
    joint1_pos, joint2_pos, angle1, angle2 = update_robot(goal_angle1, goal_angle2, angle1, angle2)

    # Updateposition box
    position_text = f"Current position: {round(joint2_pos[1]/100,2), round(joint2_pos[0]/100,2)}"

    # Draw the robot arm
    draw_robot(joint1_pos, joint2_pos, angle1, angle2)

    
    # Refresh the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
