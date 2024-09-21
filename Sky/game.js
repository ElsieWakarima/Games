const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Constants
const SCREEN_WIDTH = 400;
const SCREEN_HEIGHT = 600;
const PLAYER_WIDTH = 50;
const PLAYER_HEIGHT = 50;
const GRAVITY = 0.5;
const PLAYER_JUMP_STRENGTH = -10;
const HORIZONTAL_SPEED = 2;
const PLATFORM_WIDTH = 80;
const PLATFORM_HEIGHT = 10;
const PLATFORM_COLOR = '#64C832';

// Player object
const player = {
    x: SCREEN_WIDTH / 2 - PLAYER_WIDTH / 2,
    y: SCREEN_HEIGHT - PLAYER_HEIGHT - 10,
    width: PLAYER_WIDTH,
    height: PLAYER_HEIGHT,
    velocityY: 0,
    isJumping: false,
    moveLeft: false,
    moveRight: false,
    jump() {
        if (!this.isJumping) {
            this.velocityY = PLAYER_JUMP_STRENGTH;
            this.isJumping = true;
        }
    },
    applyGravity() {
        this.velocityY += GRAVITY;
        this.y += this.velocityY;
    },
    checkCollision(platforms) {
        platforms.forEach(platform => {
            if (this.y + this.height >= platform.y && this.y + this.height <= platform.y + 10 &&
                this.x + this.width > platform.x && this.x < platform.x + PLATFORM_WIDTH &&
                this.velocityY >= 0) {
                this.velocityY = 0;
                this.isJumping = false;
                this.y = platform.y - this.height;
            }
        });
    },
    update(platforms) {
        // Horizontal movement
        if (this.moveLeft && this.x > 0) this.x -= HORIZONTAL_SPEED;
        if (this.moveRight && this.x + this.width < SCREEN_WIDTH) this.x += HORIZONTAL_SPEED;

        // Apply gravity
        this.applyGravity();

        // Check collision with platforms
        this.checkCollision(platforms);

        // Limit player's position to bottom of the screen
        if (this.y > SCREEN_HEIGHT) {
            alert('Game Over!');
            document.location.reload();
        }
    },
    draw() {
        ctx.fillStyle = '#FF6464';
        ctx.fillRect(this.x, this.y, this.width, this.height);
    }
};

// Platform constructor
class Platform {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.width = PLATFORM_WIDTH;
        this.height = PLATFORM_HEIGHT;
    }

    draw() {
        ctx.fillStyle = PLATFORM_COLOR;
        ctx.fillRect(this.x, this.y, this.width, this.height);
    }
}

// Create platforms
const platforms = [];
for (let i = 0; i < 5; i++) {
    const x = Math.random() * (SCREEN_WIDTH - PLATFORM_WIDTH);
    const y = Math.random() * (SCREEN_HEIGHT - 100);
    platforms.push(new Platform(x, y));
}

// Listen for keyboard input
document.addEventListener('keydown', (e) => {
    if (e.code === 'ArrowLeft') player.moveLeft = true;
    if (e.code === 'ArrowRight') player.moveRight = true;
    if (e.code === 'Space') player.jump();
});

document.addEventListener('keyup', (e) => {
    if (e.code === 'ArrowLeft') player.moveLeft = false;
    if (e.code === 'ArrowRight') player.moveRight = false;
});

// Main game loop
function gameLoop() {
    ctx.clearRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);

    // Draw player and platforms
    player.update(platforms);
    player.draw();
    platforms.forEach(platform => platform.draw());

    requestAnimationFrame(gameLoop);
}

// Start the game
gameLoop();
