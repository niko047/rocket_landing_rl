# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BACKGROUND_COLOR = (0, 0, 30)  # Dark blue for sky
SPACESHIP_COLOR = (200, 200, 200)  # Light grey
THRUST_COLOR = (255, 165, 0)  # Orange
PLATFORM_COLOR = (100, 100, 100)  # Grey
OCEAN_COLOR = (0, 0, 150)  # Deep blue
SUCCESS_COLOR = (0, 255, 0)  # Green
FAILURE_COLOR = (255, 0, 0)  # Red
TEXT_COLOR = (255, 255, 255) # White
FLAME_COLOR = (255, 100, 0)  # Bright orange for flame effect

# Physics
GRAVITY = 0.1  # Reduced from 0.5
THRUST_POWER = 0.2  # Reduced from 0.7
ROTATION_SPEED = 2  # Reduced from 3
MAX_LANDING_VELOCITY = 1.5  # Slightly more forgiving
MAX_LANDING_ANGLE = 20     # Slightly more forgiving

# Screen boundaries
BOUNDARY_PADDING = 50  # Padding before reset

# Game states
GAME_STATE_PLAYING = "playing"
GAME_STATE_LANDED = "landed"
GAME_STATE_CRASHED = "crashed"

# Debug settings
DEBUG_MODE = True  # Set to False in production

# Landing parameters (adjusted)
LANDING_TOLERANCE = 5      # Pixels of tolerance for landing detection

# Animation
FLAME_VARIATION = 0.3  # How much the flame varies in size