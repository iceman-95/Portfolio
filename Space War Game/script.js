// Get the canvas and its context
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Set canvas size
canvas.width = 800;
canvas.height = 600;

// Load images
const playerImage = new Image();
playerImage.src = 'spaceship.png';

const enemyImage = new Image();
enemyImage.src = 'enemy spaceship.png';

const missileImage = new Image();
missileImage.src = 'missile.png';

const backgroundImage = new Image();
backgroundImage.src = 'space.avif';

const bigEnemyImage = new Image();
bigEnemyImage.src = 'big enemy spaceship.png';

const explosionImage = new Image();
explosionImage.src = 'explosion.png';

const enemyMissileImage = new Image();
enemyMissileImage.src = 'enemy missile.png';

// Game state
let score = 0;
let missedEnemies = 0;
let enemies = [];
let bullets = [];
let running = false;
let backgroundY = 0;

const maxMissedEnemies = 10;
const scoreElement = document.getElementById('scoreValue');

// Missed display
const missedDiv = document.createElement('div');
missedDiv.className = 'missed';
missedDiv.style.position = 'absolute';
missedDiv.style.top = '50px';
missedDiv.style.left = '20px';
missedDiv.style.color = 'white';
missedDiv.style.fontFamily = 'Arial, sans-serif';
missedDiv.style.fontSize = '20px';
missedDiv.textContent = `Missed: 0/${maxMissedEnemies}`;
document.querySelector('.game-container').appendChild(missedDiv);

// Player
const player = {
    x: canvas.width / 2,
    y: canvas.height - 75,
    width: 75,
    height: 75,
    speed: 5
};

// Controls
const keys = {
    ArrowLeft: false,
    ArrowRight: false,
    ArrowUp: false,
    ArrowDown: false,
    Space: false
};

window.addEventListener('keydown', (e) => {
    if (e.code in keys) keys[e.code] = true;
});

window.addEventListener('keyup', (e) => {
    if (e.code in keys) keys[e.code] = false;
});

// Bullets
function createBullet() {
    bullets.push({
        x: player.x + player.width / 2 - 10,
        y: player.y,
        width: 20,
        height: 40,
        speed: 7
    });
}

// Enemies
function createEnemy() {
    const enemyWidth = 50;
    const enemyHeight = 50;
    enemies.push({
        x: Math.random() * (canvas.width - enemyWidth),
        y: -30,
        width: enemyWidth,
        height: enemyHeight,
        speed: 2
    });
}

// Big enemy state
let bigEnemy = null;
let bigEnemyHits = 0;
let bigEnemyBullets = [];
let nextBigEnemyScore = 100;

let bossExplosion = null;
let bossExplosionTimer = 0;

function createBigEnemy() {
    bigEnemy = {
        x: Math.random() * (canvas.width - 150),
        y: -150, // Start above the canvas
        width: 150,
        height: 120,
        speed: 3,
        direction: 1, // 1 for right, -1 for left
        alive: true,
        entering: true // New flag for entry phase
    };
    bigEnemyHits = 0;
    bigEnemyBullets = [];
}

function updateBigEnemy() {
    if (!bigEnemy || !bigEnemy.alive) return;
    if (bigEnemy.entering) {
        // Move down until reaching y = 50
        bigEnemy.y += 2;
        if (bigEnemy.y >= 50) {
            bigEnemy.y = 50;
            bigEnemy.entering = false;
        }
        return;
    }
    bigEnemy.x += bigEnemy.speed * bigEnemy.direction;
    // Reverse direction at canvas edges
    if (bigEnemy.x <= 0) {
        bigEnemy.x = 0;
        bigEnemy.direction = 1;
    } else if (bigEnemy.x + bigEnemy.width >= canvas.width) {
        bigEnemy.x = canvas.width - bigEnemy.width;
        bigEnemy.direction = -1;
    }
    // Fire at the player every 60 frames
    if (Math.random() < 0.02) {
        bigEnemyBullets.push({
            x: bigEnemy.x + bigEnemy.width / 2 - 20,
            y: bigEnemy.y + bigEnemy.height,
            width: 40, // Increased from 20
            height: 80, // Increased from 40
            speed: 5
        });
    }
    // No vertical movement, so no need to remove if off screen vertically
}

function updateBigEnemyBullets() {
    bigEnemyBullets = bigEnemyBullets.filter(bullet => {
        bullet.y += bullet.speed;
        // Check collision with player
        if (checkCollision(bullet, player)) {
            gameOver('Hit by big enemy!');
            return false;
        }
        return bullet.y < canvas.height;
    });
}

// Update
function update() {
    backgroundY = (backgroundY + 1) % canvas.height;

    if (keys.ArrowLeft && player.x > 0) player.x -= player.speed;
    if (keys.ArrowRight && player.x < canvas.width - player.width) player.x += player.speed;
    if (keys.ArrowUp && player.y > 0) player.y -= player.speed;
    if (keys.ArrowDown && player.y < canvas.height - player.height) player.y += player.speed;

    if (keys.Space) {
        if (bullets.length === 0 || bullets[bullets.length - 1].y < player.y - 50) {
            createBullet();
        }
    }

    bullets = bullets.filter(bullet => {
        bullet.y -= bullet.speed;
        return bullet.y > 0;
    });

    // If big enemy is present, pause regular enemy spawning but do not remove existing enemies
    if (!(bigEnemy && bigEnemy.alive)) {
        if (Math.random() < 0.02) createEnemy();
    }

    enemies = enemies.filter(enemy => {
        enemy.y += enemy.speed;
        for (let i = bullets.length - 1; i >= 0; i--) {
            if (checkCollision(bullets[i], enemy)) {
                bullets.splice(i, 1);
                score += 10;
                scoreElement.textContent = score;
                // Check for big enemy spawn
                if (score >= nextBigEnemyScore) {
                    if (!bigEnemy || !bigEnemy.alive) {
                        createBigEnemy();
                        nextBigEnemyScore += 100;
                    }
                }
                return false;
            }
        }
        if (checkCollision(enemy, player)) {
            gameOver('You were hit!');
            return false;
        }
        if (enemy.y > canvas.height) {
            missedEnemies++;
            missedDiv.textContent = `Missed: ${missedEnemies}/${maxMissedEnemies}`;
            if (missedEnemies >= maxMissedEnemies) {
                gameOver('Too many enemies crossed!');
                return false;
            }
            return false;
        }
        return true;
    });

    // Big enemy logic
    if (score >= nextBigEnemyScore && (!bigEnemy || !bigEnemy.alive)) {
        createBigEnemy();
        nextBigEnemyScore += 100;
    }
    updateBigEnemy();
    updateBigEnemyBullets();
    // Check collision between player bullets and big enemy
    if (bigEnemy && bigEnemy.alive) {
        for (let i = bullets.length - 1; i >= 0; i--) {
            if (checkCollision(bullets[i], bigEnemy)) {
                bullets.splice(i, 1);
                bigEnemyHits++;
                if (bigEnemyHits >= 10) {
                    bigEnemy.alive = false;
                    // Show explosion at boss position
                    bossExplosion = {
                        x: bigEnemy.x + bigEnemy.width / 2 - 75,
                        y: bigEnemy.y + bigEnemy.height / 2 - 75,
                        width: 150,
                        height: 150
                    };
                    bossExplosionTimer = 30; // frames
                    setTimeout(() => { bigEnemy = null; }, 100);
                    // No score for killing the boss
                }
            }
        }
        // Check collision with player
        if (checkCollision(bigEnemy, player)) {
            gameOver('You were hit by the big enemy!');
        }
    }
    // Update explosion timer
    if (bossExplosionTimer > 0) {
        bossExplosionTimer--;
        if (bossExplosionTimer === 0) {
            bossExplosion = null;
        }
    }
}

// Collision detection
function checkCollision(obj1, obj2) {
    const shrink = 0.7;
    const a = {
        x: obj1.x + obj1.width * (1 - shrink) / 2,
        y: obj1.y + obj1.height * (1 - shrink) / 2,
        width: obj1.width * shrink,
        height: obj1.height * shrink
    };
    const b = {
        x: obj2.x + obj2.width * (1 - shrink) / 2,
        y: obj2.y + obj2.height * (1 - shrink) / 2,
        width: obj2.width * shrink,
        height: obj2.height * shrink
    };
    return a.x < b.x + b.width &&
           a.x + a.width > b.x &&
           a.y < b.y + b.height &&
           a.y + a.height > b.y;
}

// Draw
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(backgroundImage, 0, backgroundY, canvas.width, canvas.height);
    ctx.drawImage(backgroundImage, 0, backgroundY - canvas.height, canvas.width, canvas.height);
    ctx.drawImage(playerImage, player.x, player.y, player.width, player.height);
    bullets.forEach(b => ctx.drawImage(missileImage, b.x, b.y, b.width, b.height));
    enemies.forEach(e => ctx.drawImage(enemyImage, e.x, e.y, e.width, e.height));
    // Draw big enemy
    if (bigEnemy && bigEnemy.alive) {
        ctx.drawImage(bigEnemyImage, bigEnemy.x, bigEnemy.y, bigEnemy.width, bigEnemy.height);
        // Draw big enemy health bar
        ctx.fillStyle = 'red';
        ctx.fillRect(bigEnemy.x, bigEnemy.y - 10, bigEnemy.width, 8);
        ctx.fillStyle = 'lime';
        ctx.fillRect(bigEnemy.x, bigEnemy.y - 10, bigEnemy.width * ((10 - bigEnemyHits) / 10), 8);
    }
    // Draw big enemy bullets
    bigEnemyBullets.forEach(b => ctx.drawImage(enemyMissileImage, b.x, b.y, b.width, b.height));
    // Draw boss explosion
    if (bossExplosion) {
        ctx.drawImage(explosionImage, bossExplosion.x, bossExplosion.y, bossExplosion.width, bossExplosion.height);
    }
}

// Game loop
function gameLoop() {
    if (!running) return;
    if (paused) return;
    update();
    draw();
    requestAnimationFrame(gameLoop);
}

// Game over and restart
function gameOver(reason) {
    running = false;
    setTimeout(() => {
        alert(`${reason}\nGame Over! Your score: ${score}`);
        startGame();
    }, 100);
}

// Reset and start game
function startGame() {
    score = 0;
    missedEnemies = 0;
    enemies = [];
    bullets = [];
    bigEnemy = null;
    bigEnemyHits = 0;
    bigEnemyBullets = [];
    nextBigEnemyScore = 100;
    player.x = canvas.width / 2;
    player.y = canvas.height - 75;
    scoreElement.textContent = score;
    missedDiv.textContent = `Missed: 0/${maxMissedEnemies}`;
    for (let k in keys) keys[k] = false;
    running = true;
    paused = false;
    const pauseBtn = document.getElementById('pauseBtn');
    const continueBtn = document.getElementById('continueBtn');
    pauseBtn.style.display = 'inline-block';
    continueBtn.style.display = 'none';
    gameLoop();
}

// Wait for images before starting
let imagesLoaded = 0;
const totalImages = 7;

function imageLoaded() {
    imagesLoaded++;
    if (imagesLoaded === totalImages) {
        startGame();
    }
}

playerImage.onload = imageLoaded;
enemyImage.onload = imageLoaded;
missileImage.onload = imageLoaded;
backgroundImage.onload = imageLoaded;
bigEnemyImage.onload = imageLoaded;
explosionImage.onload = imageLoaded;
enemyMissileImage.onload = imageLoaded;

const pauseBtn = document.getElementById('pauseBtn');
const continueBtn = document.getElementById('continueBtn');
let paused = false;

pauseBtn.onclick = function() {
    paused = true;
    pauseBtn.style.display = 'none';
    continueBtn.style.display = 'inline-block';
};

continueBtn.onclick = function() {
    paused = false;
    continueBtn.style.display = 'none';
    pauseBtn.style.display = 'inline-block';
    gameLoop();
};
