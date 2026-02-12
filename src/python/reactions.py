

import math
import random
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Particle:
    """A tiny particle in an emoji's trail."""
    x: float
    y: float
    vx: float
    vy: float
    size: float
    opacity: float
    color: str
    life: float = 1.0
    decay: float = 0.02

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.02  # slight gravity
        self.life -= self.decay
        self.opacity = max(0, self.life * 0.6)
        self.size *= 0.97

    @property
    def alive(self) -> bool:
        return self.life > 0


@dataclass
class FloatingEmoji:
    """A single floating emoji reaction with full animation state."""
    emoji: str
    color: str
    x: float
    y: float
    start_y: float
    target_y: float  # where it disappears
    
    # Motion
    rise_speed: float = 2.0
    wobble_amp: float = 30.0
    wobble_freq: float = 0.03
    wobble_phase: float = 0.0
    
    # Animation state
    scale: float = 0.3
    max_scale: float = 1.2
    opacity: float = 1.0
    rotation: float = 0.0
    rotation_speed: float = 0.0
    
    # Lifecycle
    born_at: float = field(default_factory=time.time)
    lifetime: float = 3.0  # seconds
    alive: bool = True
    
    # Particles
    particles: list = field(default_factory=list)
    last_particle_spawn: float = 0.0
    
    def __post_init__(self):
        self.wobble_phase = random.uniform(0, math.pi * 2)
        self.rotation_speed = random.uniform(-2, 2)
    
    @property
    def age(self) -> float:
        return time.time() - self.born_at
    
    @property
    def progress(self) -> float:
        """0.0 = just spawned, 1.0 = about to die."""
        return min(1.0, self.age / self.lifetime)
    
    def update(self):
        """Advance one frame of animation."""
        if not self.alive:
            return
        
        progress = self.progress
        
        self.y -= self.rise_speed
        
        self.x += math.sin(self.y * self.wobble_freq + self.wobble_phase) * 1.5
        
        if progress < 0.15:
            # Elastic pop-in
            t = progress / 0.15
            self.scale = self.max_scale * self._elastic_ease(t)
        elif progress < 0.7:
            self.scale = self.max_scale
        else:
            # Shrink out
            t = (progress - 0.7) / 0.3
            self.scale = self.max_scale * (1.0 - t * t)
        
        if progress > 0.7:
            self.opacity = 1.0 - ((progress - 0.7) / 0.3)
        else:
            self.opacity = 1.0
        
        self.rotation += self.rotation_speed
        
        now = time.time()
        if now - self.last_particle_spawn > 0.05 and progress < 0.8:
            self._spawn_particle()
            self.last_particle_spawn = now
        
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.alive]
        
        if progress >= 1.0 or self.y < self.target_y:
            self.alive = False
    
    def _spawn_particle(self):
        """Create a new trail particle behind the emoji."""
        spread = 15
        self.particles.append(Particle(
            x=self.x + random.uniform(-spread, spread),
            y=self.y + random.uniform(0, 10),
            vx=random.uniform(-0.5, 0.5),
            vy=random.uniform(-0.3, 0.3),
            size=random.uniform(2, 6),
            opacity=0.5,
            color=self.color,
            decay=random.uniform(0.015, 0.04),
        ))
    
    @staticmethod
    def _elastic_ease(t: float) -> float:
        """Elastic ease-out for the pop-in effect."""
        if t <= 0:
            return 0
        if t >= 1:
            return 1
        p = 0.4
        return math.pow(2, -10 * t) * math.sin((t - p / 4) * (2 * math.pi) / p) + 1


class ReactionManager:
    """Manages all active floating emoji reactions."""
    
    def __init__(self, canvas_width: int, canvas_height: int, max_active: int = 50):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.max_active = max_active
        self.emojis: list[FloatingEmoji] = []
        self.total_spawned = 0
    
    def spawn(self, emoji: str, color: str, x: Optional[float] = None):
        """Spawn a new floating emoji reaction."""
        if len(self.emojis) >= self.max_active:
            # Remove oldest
            self.emojis.pop(0)
        
        if x is None:
            x = self.canvas_width / 2 + random.uniform(-60, 60)
        
        spawn_y = self.canvas_height - 80
        target_y = -50  # above the top edge
        
        fe = FloatingEmoji(
            emoji=emoji,
            color=color,
            x=x,
            y=spawn_y,
            start_y=spawn_y,
            target_y=target_y,
            rise_speed=random.uniform(1.5, 3.5),
            wobble_amp=random.uniform(20, 40),
            wobble_freq=random.uniform(0.02, 0.04),
        )
        
        self.emojis.append(fe)
        self.total_spawned += 1
        return fe
    
    def update(self):
        """Update all active emojis."""
        for e in self.emojis:
            e.update()
        self.emojis = [e for e in self.emojis if e.alive]
    
    @property
    def active_count(self) -> int:
        return len(self.emojis)
