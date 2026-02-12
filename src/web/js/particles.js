/**
 * Particle Trail System
 * Creates glowing particles behind floating emojis.
 */

class Particle {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.vx = (Math.random() - 0.5) * 1.2;
        this.vy = (Math.random() - 0.5) * 0.8;
        this.size = Math.random() * 4 + 1.5;
        this.color = color;
        this.life = 1.0;
        this.decay = Math.random() * 0.025 + 0.015;
        this.gravity = 0.015;
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;
        this.vy += this.gravity;
        this.vx *= 0.99;
        this.life -= this.decay;
        this.size *= 0.985;
    }

    draw(ctx) {
        if (this.life <= 0) return;

        const alpha = this.life * 0.5;
        ctx.save();
        ctx.globalAlpha = alpha;

        // Glow layer
        const gradient = ctx.createRadialGradient(
            this.x, this.y, 0,
            this.x, this.y, this.size * 2
        );
        gradient.addColorStop(0, this.color);
        gradient.addColorStop(1, 'transparent');

        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size * 2, 0, Math.PI * 2);
        ctx.fill();

        // Core dot
        ctx.globalAlpha = alpha * 1.5;
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size * 0.5, 0, Math.PI * 2);
        ctx.fill();

        ctx.restore();
    }

    get alive() {
        return this.life > 0;
    }
}


class ParticleSystem {
    constructor() {
        this.particles = [];
        this.maxParticles = 300;
    }

    emit(x, y, color, count = 4) {
        const spread = 12;
        for (let i = 0; i < count; i++) {
            if (this.particles.length >= this.maxParticles) {
                this.particles.shift();
            }
            this.particles.push(new Particle(
                x + (Math.random() - 0.5) * spread,
                y + Math.random() * 8,
                color
            ));
        }
    }

    /** Burst effect on spawn */
    burst(x, y, color, count = 12) {
        for (let i = 0; i < count; i++) {
            if (this.particles.length >= this.maxParticles) {
                this.particles.shift();
            }
            const angle = (Math.PI * 2 * i) / count + Math.random() * 0.3;
            const speed = Math.random() * 3 + 1;
            const p = new Particle(x, y, color);
            p.vx = Math.cos(angle) * speed;
            p.vy = Math.sin(angle) * speed;
            p.size = Math.random() * 3 + 2;
            p.decay = Math.random() * 0.03 + 0.02;
            this.particles.push(p);
        }
    }

    update() {
        for (const p of this.particles) {
            p.update();
        }
        this.particles = this.particles.filter(p => p.alive);
    }

    draw(ctx) {
        for (const p of this.particles) {
            p.draw(ctx);
        }
    }

    get count() {
        return this.particles.length;
    }
}

// Export for use in app.js
window.ParticleSystem = ParticleSystem;
