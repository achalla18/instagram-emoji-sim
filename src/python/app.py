"""
Emoji Reactions — Desktop App (Windows)
Instagram-style floating emoji reaction overlay using tkinter.

Run:  python app.py
"""

import tkinter as tk
import math
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CONFIG
from reactions import ReactionManager

# ═══════════════════════════════════════════════════════
# Constants from config
# ═══════════════════════════════════════════════════════
WIN = CONFIG["window"]
EMOJIS = CONFIG["emojis"]
ANIM = CONFIG["animation"]
PARTICLES = CONFIG["particles"]

WIDTH = WIN["width"]
HEIGHT = WIN["height"]
BG = WIN["background"]
FPS = 60
FRAME_MS = 1000 // FPS

# Darker/lighter variants for gradient effect
BG_DARK = "#0f0f23"
BG_MID = "#16213e"
BG_LIGHT = "#1a1a2e"

BUTTON_AREA_HEIGHT = 100
CANVAS_HEIGHT = HEIGHT - BUTTON_AREA_HEIGHT


class EmojiReactionApp:
    """Main application window."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("✨ Emoji Reactions")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(False, False)

        # Try to set always-on-top
        if WIN.get("always_on_top", False):
            self.root.attributes("-topmost", True)

        # Try to set window icon on Windows
        try:
            self.root.iconbitmap(default="")
        except Exception:
            pass

        self.manager = ReactionManager(WIDTH, CANVAS_HEIGHT, ANIM["max_active"])
        self._build_ui()
        self._animate()

    def _build_ui(self):
        """Construct the UI: canvas + emoji buttons."""

        # ── Header ──
        header = tk.Frame(self.root, bg=BG_DARK, height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header, text="✨ Emoji Reactions",
            font=("Segoe UI Emoji", 16, "bold"),
            fg="#e0e0ff", bg=BG_DARK
        ).pack(pady=10)

        # ── Canvas for floating emojis ──
        self.canvas = tk.Canvas(
            self.root, width=WIDTH, height=CANVAS_HEIGHT,
            bg=BG_DARK, highlightthickness=0, bd=0
        )
        self.canvas.pack()

        # Draw subtle gradient overlay (simulated with rectangles)
        self._draw_background()

        # ── Stats bar ──
        stats_frame = tk.Frame(self.root, bg=BG_MID, height=30)
        stats_frame.pack(fill=tk.X)
        stats_frame.pack_propagate(False)

        self.stats_label = tk.Label(
            stats_frame, text="Reactions: 0  |  Active: 0",
            font=("Segoe UI", 9), fg="#8888aa", bg=BG_MID
        )
        self.stats_label.pack(pady=5)

        # ── Emoji button bar ──
        btn_frame = tk.Frame(self.root, bg=BG_DARK, height=BUTTON_AREA_HEIGHT)
        btn_frame.pack(fill=tk.X, side=tk.BOTTOM)
        btn_frame.pack_propagate(False)

        # Instruction
        tk.Label(
            btn_frame, text="Tap to react!",
            font=("Segoe UI", 10), fg="#6666aa", bg=BG_DARK
        ).pack(pady=(8, 4))

        # Button container
        btn_container = tk.Frame(btn_frame, bg=BG_DARK)
        btn_container.pack()

        for emoji_data in EMOJIS:
            btn = tk.Button(
                btn_container,
                text=emoji_data["icon"],
                font=("Segoe UI Emoji", 22),
                bg="#2a2a4a",
                fg="white",
                activebackground="#3a3a6a",
                relief=tk.FLAT,
                width=3,
                height=1,
                cursor="hand2",
                command=lambda e=emoji_data: self._on_emoji_click(e)
            )
            btn.pack(side=tk.LEFT, padx=4, pady=4)

            # Hover effects
            btn.bind("<Enter>", lambda ev, b=btn: b.configure(bg="#3a3a6a"))
            btn.bind("<Leave>", lambda ev, b=btn: b.configure(bg="#2a2a4a"))

    def _draw_background(self):
        """Draw a subtle gradient background on the canvas."""
        steps = 20
        for i in range(steps):
            y0 = i * CANVAS_HEIGHT // steps
            y1 = (i + 1) * CANVAS_HEIGHT // steps

            # Interpolate from BG_DARK at top to BG_LIGHT at bottom
            t = i / steps
            r = int(15 + t * 11)
            g = int(15 + t * 11)
            b_val = int(35 + t * 11)
            color = f"#{r:02x}{g:02x}{b_val:02x}"

            self.canvas.create_rectangle(
                0, y0, WIDTH, y1,
                fill=color, outline=color, tags="bg"
            )

        # Subtle decorative circles (like IG Live background)
        for _ in range(5):
            import random
            cx = random.randint(0, WIDTH)
            cy = random.randint(0, CANVAS_HEIGHT)
            radius = random.randint(40, 120)
            self.canvas.create_oval(
                cx - radius, cy - radius, cx + radius, cy + radius,
                fill="", outline="#ffffff08", width=1, tags="bg"
            )

    def _on_emoji_click(self, emoji_data: dict):
        """Handle emoji button click — spawn a floating reaction."""
        # Spawn 1-3 emojis for a burst effect
        import random
        count = random.choice([1, 1, 1, 2, 2, 3])
        for i in range(count):
            x = WIDTH // 2 + random.randint(-80, 80)
            self.manager.spawn(emoji_data["icon"], emoji_data["color"], x)

    def _animate(self):
        """Main animation loop — runs at ~60fps via tkinter after()."""
        # Update physics
        self.manager.update()

        # Clear previous frame (keep background)
        self.canvas.delete("emoji")
        self.canvas.delete("particle")

        # Draw particles first (behind emojis)
        if PARTICLES.get("enabled", True):
            for fe in self.manager.emojis:
                for p in fe.particles:
                    if p.opacity > 0.05:
                        r, g, b_val = self._hex_to_rgb(p.color)
                        alpha_hex = max(0, min(255, int(p.opacity * 255)))
                        # tkinter doesn't support alpha, so we blend with background
                        blend = p.opacity * 0.6
                        br = int(r * blend + 15 * (1 - blend))
                        bg = int(g * blend + 15 * (1 - blend))
                        bb = int(b_val * blend + 35 * (1 - blend))
                        color = f"#{br:02x}{bg:02x}{bb:02x}"

                        s = max(1, int(p.size))
                        self.canvas.create_oval(
                            p.x - s, p.y - s, p.x + s, p.y + s,
                            fill=color, outline="", tags="particle"
                        )

        # Draw floating emojis
        for fe in self.manager.emojis:
            if fe.opacity < 0.05:
                continue

            size = int(ANIM["spawn_size"] * fe.scale)
            if size < 4:
                continue

            # Draw glow behind emoji
            glow_r = size + 8
            r, g, b_val = self._hex_to_rgb(fe.color)
            glow_blend = fe.opacity * 0.2
            gr = int(r * glow_blend + 15 * (1 - glow_blend))
            gg = int(g * glow_blend + 15 * (1 - glow_blend))
            gb = int(b_val * glow_blend + 35 * (1 - glow_blend))
            glow_color = f"#{gr:02x}{gg:02x}{gb:02x}"

            self.canvas.create_oval(
                fe.x - glow_r, fe.y - glow_r,
                fe.x + glow_r, fe.y + glow_r,
                fill=glow_color, outline="", tags="emoji"
            )

            # Draw the emoji text
            font_size = max(8, size)
            # Adjust opacity by dimming color (tkinter hack)
            if fe.opacity > 0.5:
                stipple = ""
            else:
                stipple = "gray50"

            self.canvas.create_text(
                fe.x, fe.y,
                text=fe.emoji,
                font=("Segoe UI Emoji", font_size),
                tags="emoji",
                stipple=stipple
            )

        # Update stats
        self.stats_label.config(
            text=f"Reactions: {self.manager.total_spawned}  |  "
                 f"Active: {self.manager.active_count}"
        )

        # Schedule next frame
        self.root.after(FRAME_MS, self._animate)

    @staticmethod
    def _hex_to_rgb(hex_color: str) -> tuple:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 6:
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return (255, 255, 255)

    def run(self):
        """Start the application."""
        print("=" * 45)
        print("  ✨ Emoji Reactions — Desktop App")
        print("  Click the emojis to send reactions!")
        print("=" * 45)
        self.root.mainloop()


if __name__ == "__main__":
    app = EmojiReactionApp()
    app.run()
