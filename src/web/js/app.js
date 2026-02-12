/**
 * Emoji Reactions — Main Application
 * Canvas-based floating emoji animation engine.
 */

// ═══════════════════════════════════════════════════
// Floating Emoji Class
// ═══════════════════════════════════════════════════

class FloatingEmoji {
    constructor(emoji, color, x, canvasHeight) {
        this.emoji = emoji;
        this.color = color;
        this.x = x;
        this.originX = x;
        this.y = canvasHeight - 20;
        this.canvasHeight = canvasHeight;

        // Motion parameters (randomized per instance)
        this.riseSpeed = 1.5 + Math.random() * 2.5;
        this.wobbleAmp = 25 + Math.random() * 20;
        this.wobbleFreq = 0.015 + Math.random() * 0.015;
        this.wobblePhase = Math.random() * Math.PI * 2;

        // Animation state
        this.scale = 0.1;
        this.maxScale = 0.9 + Math.random() * 0.4;
        this.opacity = 1;
        this.rotation = 0;
        this.rotationSpeed = (Math.random() - 0.5) * 3;

        // Lifecycle
        this.born = performance.now();
        this.lifetime = 2800 + Math.random() * 800; // ms
        this.alive = true;

        // Particle trail timing
        this.lastParticle = 0;
    }

    get age() {
        return performance.now() - this.born;
    }

    get progress() {
        return Math.min(1, this.age / this.lifetime);
    }

    update() {
        if (!this.alive) return;

        const p = this.progress;

        // Rise upward
        this.y -= this.riseSpeed;

        // Sinusoidal wobble
        this.x = this.originX + Math.sin(this.y * this.wobbleFreq + this.wobblePhase) * this.wobbleAmp;

        // Scale: elastic pop-in → hold → shrink out
        if (p < 0.12) {
            const t = p / 0.12;
            this.scale = this.maxScale * this._elasticEase(t);
        } else if (p < 0.7) {
            this.scale = this.maxScale;
        } else {
            const t = (p - 0.7) / 0.3;
            this.scale = this.maxScale * (1 - t * t);
        }

        // Opacity fade in last 30%
        this.opacity = p > 0.7 ? 1 - ((p - 0.7) / 0.3) : 1;

        // Gentle rotation
        this.rotation += this.rotationSpeed * 0.01;

        // Death
        if (p >= 1 || this.y < -60) {
            this.alive = false;
        }
    }

    draw(ctx) {
        if (!this.alive || this.opacity < 0.02) return;

        const size = 36 * this.scale;
        if (size < 3) return;

        ctx.save();
        ctx.globalAlpha = this.opacity;
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation);

        // Glow behind emoji
        const glowSize = size * 1.8;
        const glow = ctx.createRadialGradient(0, 0, size * 0.2, 0, 0, glowSize);
        glow.addColorStop(0, this.color + '30');
        glow.addColorStop(0.5, this.color + '10');
        glow.addColorStop(1, 'transparent');
        ctx.fillStyle = glow;
        ctx.beginPath();
        ctx.arc(0, 0, glowSize, 0, Math.PI * 2);
        ctx.fill();

        // Emoji
        ctx.font = `${Math.round(size)}px "Segoe UI Emoji", "Apple Color Emoji", sans-serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(this.emoji, 0, 0);

        ctx.restore();
    }

    _elasticEase(t) {
        if (t <= 0) return 0;
        if (t >= 1) return 1;
        const p = 0.4;
        return Math.pow(2, -10 * t) * Math.sin((t - p / 4) * (2 * Math.PI) / p) + 1;
    }
}


// ═══════════════════════════════════════════════════
// Main App Controller
// ═══════════════════════════════════════════════════

class EmojiReactionApp {
    constructor() {
        // Canvas setup
        this.canvas = document.getElementById('reactionCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.resize();

        // Systems
        this.particles = new ParticleSystem();
        this.audio = new AudioEngine();

        // State
        this.emojis = [];
        this.maxActive = 50;
        this.totalCount = 0;
        this.emojiCounts = {};
        this.hintShown = true;

        // DOM refs
        this.totalEl = document.getElementById('totalCount');
        this.activeEl = document.getElementById('activeCount');
        this.topEmojiEl = document.getElementById('topEmoji');
        this.hintEl = document.getElementById('hint');
        this.buttons = document.querySelectorAll('.emoji-btn');

        this._bindEvents();
        this._startLoop();
    }

    resize() {
        const container = this.canvas.parentElement;
        const dpr = window.devicePixelRatio || 1;
        const rect = container.getBoundingClientRect();

        this.canvas.width = rect.width * dpr;
        this.canvas.height = rect.height * dpr;
        this.canvas.style.width = rect.width + 'px';
        this.canvas.style.height = rect.height + 'px';
        this.ctx.scale(dpr, dpr);

        this.width = rect.width;
        this.height = rect.height;
    }

    _bindEvents() {
        // Emoji buttons
        this.buttons.forEach(btn => {
            const handler = (e) => {
                e.preventDefault();
                // Init audio on first interaction
                this.audio.init();

                const emoji = btn.dataset.emoji;
                const color = btn.dataset.color;
                this._spawnReaction(emoji, color);

                // Button pulse animation
                btn.classList.remove('pulse');
                void btn.offsetWidth; // reflow
                btn.classList.add('pulse');

                // Update per-button count
                const countEl = btn.querySelector('.emoji-count');
                this.emojiCounts[emoji] = (this.emojiCounts[emoji] || 0) + 1;
                countEl.textContent = this.emojiCounts[emoji];
            };

            btn.addEventListener('click', handler);
            btn.addEventListener('touchstart', handler, { passive: false });
        });

        // Responsive resize
        window.addEventListener('resize', () => {
            clearTimeout(this._resizeTimeout);
            this._resizeTimeout = setTimeout(() => this.resize(), 100);
        });

        // Canvas click — spawn at click position
        this.canvas.addEventListener('click', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const emojis = ['❤️', '😂', '😮', '😢', '😡', '👍'];
            const colors = ['#ff3b5c', '#ffcc00', '#ff9500', '#5ac8fa', '#ff2d55', '#34c759'];
            const idx = Math.floor(Math.random() * emojis.length);
            this._spawnAt(emojis[idx], colors[idx], x);
        });
    }

    _spawnReaction(emoji, color) {
        // Spawn 1-3 for burst feel
        const count = [1, 1, 1, 2, 2, 3][Math.floor(Math.random() * 6)];
        for (let i = 0; i < count; i++) {
            const x = this.width / 2 + (Math.random() - 0.5) * 160;
            this._spawnAt(emoji, color, x);
        }

        // Sound
        if (count > 1) {
            this.audio.playBurstPop();
        } else {
            this.audio.playPop();
        }
    }

    _spawnAt(emoji, color, x) {
        if (this.emojis.length >= this.maxActive) {
            this.emojis.shift();
        }

        const fe = new FloatingEmoji(emoji, color, x, this.height);
        this.emojis.push(fe);
        this.totalCount++;

        // Burst particles at spawn point
        this.particles.burst(x, this.height - 20, color, 8);

        // Hide hint after first reaction
        if (this.hintShown) {
            this.hintEl.classList.add('hidden');
            this.hintShown = false;
        }
    }

    _startLoop() {
        const loop = () => {
            this._update();
            this._draw();
            requestAnimationFrame(loop);
        };
        requestAnimationFrame(loop);
    }

    _update() {
        // Update emojis
        const now = performance.now();
        for (const fe of this.emojis) {
            fe.update();

            // Emit trail particles
            if (fe.alive && fe.progress < 0.75 && now - fe.lastParticle > 40) {
                this.particles.emit(fe.x, fe.y + 10, fe.color, 3);
                fe.lastParticle = now;
            }
        }
        this.emojis = this.emojis.filter(e => e.alive);

        // Update particles
        this.particles.update();

        // Update stats DOM (throttled)
        if (!this._lastStats || now - this._lastStats > 200) {
            this.totalEl.textContent = this.totalCount;
            this.activeEl.textContent = this.emojis.length;

            // Find top emoji
            let topEmoji = '—';
            let topCount = 0;
            for (const [emoji, count] of Object.entries(this.emojiCounts)) {
                if (count > topCount) {
                    topCount = count;
                    topEmoji = emoji;
                }
            }
            this.topEmojiEl.textContent = topEmoji;
            this._lastStats = now;
        }
    }

    _draw() {
        const ctx = this.ctx;

        // Clear canvas
        ctx.clearRect(0, 0, this.width, this.height);

        // Draw particles (behind emojis)
        this.particles.draw(ctx);

        // Draw floating emojis
        for (const fe of this.emojis) {
            fe.draw(ctx);
        }
    }
}


// ═══════════════════════════════════════════════════
// Boot
// ═══════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
    window.app = new EmojiReactionApp();
});
