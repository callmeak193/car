import pygame
import random

# Initialize pygame
pygame.init()

# Game screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Game with Moving Road")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Load background image (road)
background_img = pygame.image.load('road.png')  # Load your road background image
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load blast image
blast_img = pygame.image.load('blast.png')  # Load the blast image
blast_img = pygame.transform.scale(blast_img, (100, 100))  # Adjust size if needed
blast_position = None  # Variable to store blast position

# Car settings
car_img = pygame.image.load('car.png')  # Load the car image
car_img = pygame.transform.scale(car_img, (60, 100))
car_x = SCREEN_WIDTH // 2 - 30  # Keep car in the center horizontally
car_y = SCREEN_HEIGHT - 150  # Keep car fixed near the bottom of the screen
car_angle = 0
steering_speed = 4  # Adjusted for smoother left-right movement

# Road movement settings
road_y1 = 0
road_y2 = -SCREEN_HEIGHT
road_speed = 5  # Speed of the road moving downward

# Button dimensions
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 50
button_left = pygame.Rect(50, 500, BUTTON_WIDTH, BUTTON_HEIGHT)
button_right = pygame.Rect(650, 500, BUTTON_WIDTH, BUTTON_HEIGHT)
button_restart = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 25, BUTTON_WIDTH, BUTTON_HEIGHT)

# Clock for FPS control
clock = pygame.time.Clock()

# Load the font for button text
font = pygame.font.Font(None, 36)

# Load traffic car images
traffic_cars = []
for i in range(3):
    traffic_car_img = pygame.image.load(f'car{i + 1}.png')  # Load traffic car images (car1.png, car2.png, car3.png)
    traffic_car_img = pygame.transform.scale(traffic_car_img, (60, 100))
    
    # Random starting position within the road
    if random.choice([True, False]):  # Randomly place car on left or right side
        traffic_car_x = random.randint(100, SCREEN_WIDTH // 2 - 60)  # Left side
    else:
        traffic_car_x = random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - 100 - 60)  # Right side
    
    traffic_car_y = random.randint(-600, -100)  # Start off-screen above
    traffic_speed = random.randint(3, 7)  # Random speed for each traffic car
    traffic_cars.append([traffic_car_img, traffic_car_x, traffic_car_y, traffic_speed])

def draw_buttons():
    """Draw the left and right buttons with text."""
    pygame.draw.rect(screen, GREEN, button_left)
    pygame.draw.rect(screen, GREEN, button_right)

    left_text = font.render('Left', True, WHITE)
    right_text = font.render('Right', True, WHITE)
    
    screen.blit(left_text, (button_left.x + 10, button_left.y + 10))
    screen.blit(right_text, (button_right.x + 10, button_right.y + 10))

def draw_restart_button():
    """Draw the restart button after a crash."""
    pygame.draw.rect(screen, RED, button_restart)
    restart_text = font.render('Restart', True, WHITE)
    screen.blit(restart_text, (button_restart.x + 10, button_restart.y + 10))

def check_collision(car_rect, traffic_cars):
    """Check for collision between the player's car and traffic cars."""
    for traffic_car in traffic_cars:
        traffic_car_rect = pygame.Rect(traffic_car[1], traffic_car[2], 60, 100)  # Create rect for traffic car
        if car_rect.colliderect(traffic_car_rect):  # Check collision
            return traffic_car[1], traffic_car[2]  # Return the position of the collision
    return None  # No collision

def game_loop():
    global car_x, road_y1, road_y2, blast_position, traffic_cars

    running = True
    crashed = False
    distance_traveled = 0  # Keep track of distance traveled

    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not crashed:
                    if button_left.collidepoint(event.pos):
                        car_x -= 30  # Move car left
                    elif button_right.collidepoint(event.pos):
                        car_x += 30  # Move car right
                else:
                    if button_restart.collidepoint(event.pos):
                        crashed = False
                        blast_position = None
                        distance_traveled = 0  # Reset distance
                        # Reset traffic cars
                        traffic_cars = []
                        for i in range(3):
                            traffic_car_img = pygame.image.load(f'car{i + 1}.png')
                            traffic_car_img = pygame.transform.scale(traffic_car_img, (60, 100))
                            traffic_car_x = random.randint(100, SCREEN_WIDTH // 2 - 60)
                            traffic_car_y = random.randint(-600, -100)
                            traffic_speed = random.randint(3, 7)
                            traffic_cars.append([traffic_car_img, traffic_car_x, traffic_car_y, traffic_speed])

        if not crashed:
            # Key presses for steering
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                car_x -= steering_speed
            if keys[pygame.K_RIGHT]:
                car_x += steering_speed

            # Ensure the car stays within the horizontal boundaries
            if car_x < 0:
                car_x = 0
            if car_x > SCREEN_WIDTH - 60:  # Subtract car width to stay on screen
                car_x = SCREEN_WIDTH - 60

            # Move the road
            road_y1 += road_speed
            road_y2 += road_speed

            # Reset the road positions when they go off-screen (continuous scrolling)
            if road_y1 >= SCREEN_HEIGHT:
                road_y1 = -SCREEN_HEIGHT
            if road_y2 >= SCREEN_HEIGHT:
                road_y2 = -SCREEN_HEIGHT

            # Draw the road (two images to create the scrolling effect)
            screen.blit(background_img, (0, road_y1))
            screen.blit(background_img, (0, road_y2))

            # Draw the car (it stays fixed near the bottom)
            screen.blit(car_img, (car_x, car_y))

            # Create a rect for the player's car for collision detection
            car_rect = pygame.Rect(car_x, car_y, 60, 100)

            # Update and draw traffic cars
            for traffic_car in traffic_cars:
                traffic_car_img, traffic_car_x, traffic_car_y, traffic_speed = traffic_car
                traffic_car_y += traffic_speed  # Move traffic car down

                # Reset traffic car position when it goes off-screen (reappear at the top)
                if traffic_car_y > SCREEN_HEIGHT:
                    traffic_car_y = random.randint(-600, -100)  # Reset to a new random position
                    if random.choice([True, False]):  # Randomly place car on left or right side
                        traffic_car_x = random.randint(100, SCREEN_WIDTH // 2 - 60)  # Left side
                    else:
                        traffic_car_x = random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - 100 - 60)  # Right side

                traffic_car[2] = traffic_car_y  # Update the traffic car's y position
                screen.blit(traffic_car_img, (traffic_car_x, traffic_car_y))

            # Check for collision and set blast position
            blast_position = check_collision(car_rect, traffic_cars)

            # Draw blast effect if a collision occurs
            if blast_position:
                crashed = True  # Stop the game after crash
                screen.blit(blast_img, (blast_position[0] - 20, blast_position[1] - 20))  # Center the blast image

            # Draw buttons for steering (left and right)
            draw_buttons()

            # Update distance traveled (assuming road speed represents km/mile per frame)
            distance_traveled += road_speed / 100  # You can adjust this value for scaling

            # Draw the distance traveled on the screen
            distance_text = font.render(f"Distance: {int(distance_traveled)} km", True, BLACK)
            screen.blit(distance_text, (10, 10))

        else:
            # Show the restart button if the car crashed
            draw_restart_button()

        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()

# Start the game loop
game_loop()
