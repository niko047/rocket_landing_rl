import math
import pygame
from constants import *
import random

class Spaceship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 40
        self.angle = 0  # 0 degrees is pointing up
        self.velocity_y = 0
        self.velocity_x = 0
        self.angular_velocity = 0
        self.landed = False
        self.crashed = False
        
        # Thrust
        self.thrusters = {
            "ul": False,  # Upper left
            "ur": False,  # Upper right
            "bl": False,  # Bottom left
            "br": False,  # Bottom right
            "b": False,   # Bottom center
        }
    
    def update(self, keys):
        # Handle key inputs for thrusters using arrow keys
        shift_pressed = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        
        # Bottom thrusters with arrow keys
        self.thrusters["bl"] = keys[pygame.K_LEFT] and not shift_pressed
        self.thrusters["br"] = keys[pygame.K_RIGHT] and not shift_pressed
        self.thrusters["b"] = keys[pygame.K_DOWN]
        
        # Upper thrusters with SHIFT + arrow keys
        self.thrusters["ul"] = keys[pygame.K_LEFT] and shift_pressed
        self.thrusters["ur"] = keys[pygame.K_RIGHT] and shift_pressed
        
        # Apply gravity
        self.velocity_y += GRAVITY
        
        # Apply thrusters
        self._apply_thrusters()
        
        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.angle += self.angular_velocity
        
        # Apply drag (increased for more control)
        self.velocity_x *= 0.98
        self.velocity_y *= 0.98
        self.angular_velocity *= 0.93
        
        # Check if out of bounds
        if (self.y < -BOUNDARY_PADDING or 
            self.y > SCREEN_HEIGHT + BOUNDARY_PADDING or
            self.x < -BOUNDARY_PADDING or 
            self.x > SCREEN_WIDTH + BOUNDARY_PADDING):
            return "reset"
        
        return "playing"
    
    def _apply_thrusters(self):
        angle_rad = math.radians(self.angle)
        
        # Added thrust multiplier for finer control
        thrust_multiplier = 0.7 if pygame.key.get_pressed()[pygame.K_LSHIFT] else 1.0
        
        if self.thrusters["b"]:
            self.velocity_y -= math.cos(angle_rad) * THRUST_POWER * thrust_multiplier
            self.velocity_x += math.sin(angle_rad) * THRUST_POWER * thrust_multiplier
            
        if self.thrusters["bl"]:
            self.velocity_y -= math.cos(angle_rad) * THRUST_POWER * 0.5
            self.velocity_x += math.sin(angle_rad) * THRUST_POWER * 0.5
            self.angular_velocity += ROTATION_SPEED * 0.5
            
        if self.thrusters["br"]:
            self.velocity_y -= math.cos(angle_rad) * THRUST_POWER * 0.5
            self.velocity_x += math.sin(angle_rad) * THRUST_POWER * 0.5
            self.angular_velocity -= ROTATION_SPEED * 0.5
            
        if self.thrusters["ul"]:
            self.angular_velocity += ROTATION_SPEED
            
        if self.thrusters["ur"]:
            self.angular_velocity -= ROTATION_SPEED
    
    def draw(self, screen):
        # Calculate corners of the rectangle
        corners = self._get_corners()
        
        # Draw spaceship body
        pygame.draw.polygon(screen, SPACESHIP_COLOR, corners)
        
        # Draw thrusters
        self._draw_thrusters(screen, corners)
        
        # Debug visualization
        if DEBUG_MODE:
            # Calculate side thruster positions
            upper_left_pos = (
                corners[0][0] * 0.75 + corners[3][0] * 0.25,
                corners[0][1] * 0.75 + corners[3][1] * 0.25
            )
            upper_right_pos = (
                corners[1][0] * 0.75 + corners[2][0] * 0.25,
                corners[1][1] * 0.75 + corners[2][1] * 0.25
            )
            
            # Draw all thruster positions
            # Bottom center thruster
            bottom_center = ((corners[2][0] + corners[3][0])/2,
                            (corners[2][1] + corners[3][1])/2)
            pygame.draw.circle(screen, (255, 0, 0), 
                             (int(bottom_center[0]), int(bottom_center[1])), 3)
            
            # Bottom left thruster
            pygame.draw.circle(screen, (255, 0, 0),
                             (int(corners[3][0]), int(corners[3][1])), 3)
            
            # Bottom right thruster
            pygame.draw.circle(screen, (255, 0, 0),
                             (int(corners[2][0]), int(corners[2][1])), 3)
            
            # Upper left thruster (side position)
            pygame.draw.circle(screen, (255, 0, 0),
                             (int(upper_left_pos[0]), int(upper_left_pos[1])), 3)
            
            # Upper right thruster (side position)
            pygame.draw.circle(screen, (255, 0, 0),
                             (int(upper_right_pos[0]), int(upper_right_pos[1])), 3)
    
    def _get_corners(self):
        angle_rad = math.radians(self.angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        corners = [
            (-self.width/2, -self.height/2),
            (self.width/2, -self.height/2),
            (self.width/2, self.height/2),
            (-self.width/2, self.height/2)
        ]
        
        rotated_corners = []
        for x, y in corners:
            rotated_x = x * cos_a - y * sin_a + self.x
            rotated_y = x * sin_a + y * cos_a + self.y
            rotated_corners.append((rotated_x, rotated_y))
            
        return rotated_corners
    
    def _draw_thrusters(self, screen, corners):
        if any(self.thrusters.values()):
            for thruster, active in self.thrusters.items():
                if active:
                    self._draw_thrust(screen, corners, thruster)
    
    def _draw_thrust(self, screen, corners, thruster):
        angle_rad = math.radians(self.angle)
        thrust_length = 20
        
        # Calculate side thruster positions (1/4 from top)
        upper_left_pos = (
            corners[0][0] * 0.75 + corners[3][0] * 0.25,
            corners[0][1] * 0.75 + corners[3][1] * 0.25
        )
        upper_right_pos = (
            corners[1][0] * 0.75 + corners[2][0] * 0.25,
            corners[1][1] * 0.75 + corners[2][1] * 0.25
        )
        
        if thruster == "b":  # Bottom center thruster
            start = ((corners[2][0] + corners[3][0])/2,
                    (corners[2][1] + corners[3][1])/2)
            end = (start[0] + thrust_length * math.sin(angle_rad),
                  start[1] + thrust_length * math.cos(angle_rad))
            pygame.draw.line(screen, THRUST_COLOR, start, end, 3)
            
        elif thruster == "bl":  # Bottom left thruster
            start = (corners[3][0], corners[3][1])  # Bottom left corner
            end = (start[0] + thrust_length * math.sin(angle_rad),
                  start[1] + thrust_length * math.cos(angle_rad))
            pygame.draw.line(screen, THRUST_COLOR, start, end, 2)
            
        elif thruster == "br":  # Bottom right thruster
            start = (corners[2][0], corners[2][1])  # Bottom right corner
            end = (start[0] + thrust_length * math.sin(angle_rad),
                  start[1] + thrust_length * math.cos(angle_rad))
            pygame.draw.line(screen, THRUST_COLOR, start, end, 2)
            
        elif thruster == "ul":  # Upper left thruster
            start = upper_left_pos
            # Thrust direction is perpendicular to rocket body
            end = (start[0] + thrust_length * math.cos(angle_rad),
                  start[1] - thrust_length * math.sin(angle_rad))
            pygame.draw.line(screen, THRUST_COLOR, start, end, 2)
            
        elif thruster == "ur":  # Upper right thruster
            start = upper_right_pos
            # Thrust direction is perpendicular to rocket body
            end = (start[0] - thrust_length * math.cos(angle_rad),
                  start[1] + thrust_length * math.sin(angle_rad))
            pygame.draw.line(screen, THRUST_COLOR, start, end, 2)
            
        # Add a flame effect
        if thruster in ["b", "bl", "br"]:
            # Random flame variations
            flame_points = []
            num_points = 3
            base_x = (start[0] + end[0]) / 2
            base_y = (start[1] + end[1]) / 2
            
            for i in range(num_points):
                variation = thrust_length * 0.3 * (random.random() - 0.5)
                flame_points.append((
                    end[0] + variation,
                    end[1] + variation
                ))
            
            if len(flame_points) >= 3:
                pygame.draw.polygon(screen, FLAME_COLOR, 
                                  [start, flame_points[0], flame_points[1], flame_points[2]], 0)
    
    def check_landing(self, platform):
        # Get the bottom center point of the spaceship
        corners = self._get_corners()
        ship_bottom_center = ((corners[2][0] + corners[3][0])/2,
                             (corners[2][1] + corners[3][1])/2)
        
        # Get the platform boundaries
        platform_left = platform.x - platform.width/2
        platform_right = platform.x + platform.width/2
        platform_top = platform.y - platform.height/2
        
        # Check if bottom center is within platform x-bounds
        is_above_platform = (platform_left <= ship_bottom_center[0] <= platform_right)
        
        # Check if any corner is below water level
        water_level = SCREEN_HEIGHT - 100
        is_in_water = any(corner[1] > water_level for corner in corners)
        
        # Check if any corner is touching the platform
        touching_platform = any(
            platform_left <= corner[0] <= platform_right and 
            abs(corner[1] - platform_top) < 5
            for corner in corners[2:] # Only check bottom corners
        )
        
        # Calculate total velocity magnitude
        total_velocity = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
        
        # Normalize angle to 0-360 range
        normalized_angle = self.angle % 360
        if normalized_angle > 180:
            normalized_angle = normalized_angle - 360
        
        # Define landing conditions
        speed_ok = total_velocity < MAX_LANDING_VELOCITY
        angle_ok = abs(normalized_angle) < MAX_LANDING_ANGLE
        
        # Debug information
        debug_info = {
            'velocity': total_velocity,
            'angle': normalized_angle,
            'is_above_platform': is_above_platform,
            'touching_platform': touching_platform
        }
        
        # Check crash conditions first
        if is_in_water:
            self.crashed = True
            return "crashed"
        
        # Check if touching platform
        if touching_platform:
            if speed_ok and angle_ok:
                self.landed = True
                return "landed"
            else:
                self.crashed = True
                return "crashed"
        
        return "playing"
    
    def reset(self, x, y):
        self.__init__(x, y)
    
    def _apply_thrusters_gym(self, actions):
        """Version of apply_thrusters for gym environment without pygame dependencies"""
        angle_rad = math.radians(self.angle)
        
        # Actions should be a dictionary or array indicating which thrusters to fire
        # Example: actions = {"ul": 0/1, "ur": 0/1, "bl": 0/1, "br": 0/1, "b": 0/1}
        self.thrusters = actions
        
        if self.thrusters["b"]:
            self.velocity_y -= math.cos(angle_rad) * THRUST_POWER
            self.velocity_x += math.sin(angle_rad) * THRUST_POWER
            
        if self.thrusters["bl"]:
            self.velocity_y -= math.cos(angle_rad) * THRUST_POWER * 0.5
            self.velocity_x += math.sin(angle_rad) * THRUST_POWER * 0.5
            self.angular_velocity += ROTATION_SPEED * 0.5
            
        if self.thrusters["br"]:
            self.velocity_y -= math.cos(angle_rad) * THRUST_POWER * 0.5
            self.velocity_x += math.sin(angle_rad) * THRUST_POWER * 0.5
            self.angular_velocity -= ROTATION_SPEED * 0.5
            
        if self.thrusters["ul"]:
            self.angular_velocity += ROTATION_SPEED
            
        if self.thrusters["ur"]:
            self.angular_velocity -= ROTATION_SPEED
    
    def update_gym(self, actions):
        """Update method for gym environment without pygame dependencies"""
        # Apply gravity
        self.velocity_y += GRAVITY
        
        # Apply thrusters based on AI actions
        self._apply_thrusters_gym(actions)
        
        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.angle += self.angular_velocity
        
        # Apply drag
        self.velocity_x *= 0.98
        self.velocity_y *= 0.98
        self.angular_velocity *= 0.93
        
        # Check if out of bounds
        if (self.y < -BOUNDARY_PADDING or 
            self.y > SCREEN_HEIGHT + BOUNDARY_PADDING or
            self.x < -BOUNDARY_PADDING or 
            self.x > SCREEN_WIDTH + BOUNDARY_PADDING):
            return "reset"
        
        return "playing"
    
    def get_state(self):
        """Return the state of the spaceship for the AI"""
        return {
            'x': self.x,
            'y': self.y,
            'velocity_x': self.velocity_x,
            'velocity_y': self.velocity_y,
            'angle': self.angle,
            'angular_velocity': self.angular_velocity
        }