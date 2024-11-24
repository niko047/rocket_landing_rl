import pygame
import sys
from spaceship import Spaceship
from landing_platform import LandingPlatform
from constants import *

pygame.init()
pygame.font.init()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rocket Landing Simulator")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 30)

def draw_hud(screen, spaceship, game_state, score):
    # Draw velocity indicators
    velocity_text = f"Velocity: ({spaceship.velocity_x:.1f}, {spaceship.velocity_y:.1f})"
    angle_text = f"Angle: {spaceship.angle % 360:.1f}°"
    vel_surface = font.render(velocity_text, True, TEXT_COLOR)
    angle_surface = font.render(angle_text, True, TEXT_COLOR)
    screen.blit(vel_surface, (10, 10))
    screen.blit(angle_surface, (10, 40))
    
    # Draw score
    score_text = f"Score: {score}"
    score_surface = font.render(score_text, True, TEXT_COLOR)
    screen.blit(score_surface, (SCREEN_WIDTH - 150, 10))
    
    # Draw game state messages
    if game_state == "landed":
        msg = "Successful Landing! Press SPACE to restart"
        color = SUCCESS_COLOR
    elif game_state == "crashed":
        msg = "Crashed! Press SPACE to restart"
        color = FAILURE_COLOR
    else:
        return
    
    state_surface = font.render(msg, True, color)
    screen.blit(state_surface, 
                (SCREEN_WIDTH/2 - state_surface.get_width()/2, 
                 SCREEN_HEIGHT/2))

def main():
    spaceship = Spaceship(SCREEN_WIDTH // 2, 100)
    landing_platform = LandingPlatform(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120)
    game_state = GAME_STATE_PLAYING
    score = 0
    
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_state != GAME_STATE_PLAYING:
                    # Reset game
                    spaceship.reset(SCREEN_WIDTH // 2, 100)
                    game_state = GAME_STATE_PLAYING
        
        # Get pressed keys for thrust control
        keys = pygame.key.get_pressed()
        
        # Update
        if game_state == GAME_STATE_PLAYING:
            update_result = spaceship.update(keys)
            
            if update_result == "reset":
                spaceship.reset(SCREEN_WIDTH // 2, 100)
            else:
                game_state = spaceship.check_landing(landing_platform)
                
                if game_state == "landed":
                    landing_score = int(1000 * (1 - abs(spaceship.velocity_y)/MAX_LANDING_VELOCITY) *
                                      (1 - abs(spaceship.angle)/MAX_LANDING_ANGLE))
                    score += landing_score
        
        # Draw
        screen.fill(BACKGROUND_COLOR)
        
        # Draw ocean
        pygame.draw.rect(screen, OCEAN_COLOR, 
                        (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
        
        landing_platform.draw(screen)
        spaceship.draw(screen)
        draw_hud(screen, spaceship, game_state, score)
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main() 