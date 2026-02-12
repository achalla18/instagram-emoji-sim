

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'python'))

from reactions import FloatingEmoji, ReactionManager, Particle


def test_particle_lifecycle():
    """Particles should decay and die."""
    p = Particle(x=100, y=100, vx=0.5, vy=-0.3, size=4, opacity=0.6, color="#ff0000")
    assert p.alive
    
    for _ in range(100):
        p.update()
    
    assert not p.alive
    assert p.opacity <= 0
    print("  PASS  particle lifecycle")


def test_floating_emoji_creation():
    """FloatingEmoji should initialize with valid state."""
    fe = FloatingEmoji(
        emoji="❤️", color="#ff3b5c",
        x=200, y=600, start_y=600, target_y=-50
    )
    assert fe.alive
    assert fe.scale == 0.3
    assert fe.opacity == 1.0
    assert fe.emoji == "❤️"
    print("  PASS  emoji creation")


def test_floating_emoji_rises():
    """Emoji should move upward over time."""
    fe = FloatingEmoji(
        emoji="😂", color="#ffcc00",
        x=200, y=600, start_y=600, target_y=-50,
        rise_speed=3.0
    )
    initial_y = fe.y
    
    for _ in range(10):
        fe.update()
    
    assert fe.y < initial_y, f"Emoji should rise: {fe.y} should be < {initial_y}"
    print("  PASS  emoji rises")


def test_floating_emoji_death():
    """Emoji should die after its lifetime."""
    fe = FloatingEmoji(
        emoji="😮", color="#ff9500",
        x=200, y=600, start_y=600, target_y=-50,
        lifetime=0.1  # very short
    )
    time.sleep(0.15)
    fe.update()
    assert not fe.alive
    print("  PASS  emoji death")


def test_manager_spawn():
    """Manager should track spawned emojis."""
    mgr = ReactionManager(canvas_width=400, canvas_height=700, max_active=10)
    
    mgr.spawn("❤️", "#ff3b5c")
    mgr.spawn("😂", "#ffcc00")
    
    assert mgr.active_count == 2
    assert mgr.total_spawned == 2
    print("  PASS  manager spawn")


def test_manager_max_active():
    """Manager should cap active emojis."""
    mgr = ReactionManager(canvas_width=400, canvas_height=700, max_active=3)
    
    for i in range(10):
        mgr.spawn("👍", "#34c759")
    
    assert mgr.active_count <= 3, f"Expected max 3, got {mgr.active_count}"
    assert mgr.total_spawned == 10
    print("  PASS  manager max active cap")


def test_manager_cleanup():
    """Dead emojis should be removed on update."""
    mgr = ReactionManager(canvas_width=400, canvas_height=700)
    
    # Spawn with very short lifetime
    fe = mgr.spawn("😢", "#5ac8fa")
    fe.lifetime = 0.05
    
    time.sleep(0.1)
    mgr.update()
    
    assert mgr.active_count == 0, "Dead emojis should be cleaned up"
    print("  PASS  manager cleanup")


def test_elastic_ease():
    """Elastic ease function should return valid values."""
    fe = FloatingEmoji(
        emoji="❤️", color="#ff0000",
        x=0, y=0, start_y=0, target_y=-50
    )
    
    assert fe._elastic_ease(0) == 0
    assert fe._elastic_ease(1) == 1
    assert 0 <= fe._elastic_ease(0.5) <= 1.5  # elastic can overshoot
    print("  PASS  elastic ease function")


def test_progress_calculation():
    """Progress should go from 0 to 1 over lifetime."""
    fe = FloatingEmoji(
        emoji="👍", color="#34c759",
        x=0, y=600, start_y=600, target_y=-50,
        lifetime=1.0
    )
    
    assert fe.progress < 0.1, "Progress should start near 0"
    
    time.sleep(0.5)
    p = fe.progress
    assert 0.3 < p < 0.8, f"Mid-life progress should be ~0.5, got {p}"
    print("  PASS  progress calculation")


if __name__ == "__main__":
    print()
    print("=" * 45)
    print("  Emoji Reactions — Test Suite")
    print("=" * 45)
    print()
    
    tests = [
        test_particle_lifecycle,
        test_floating_emoji_creation,
        test_floating_emoji_rises,
        test_floating_emoji_death,
        test_manager_spawn,
        test_manager_max_active,
        test_manager_cleanup,
        test_elastic_ease,
        test_progress_calculation,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  FAIL  {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"  ERROR {test.__name__}: {e}")
            failed += 1
    
    print()
    print(f"  Results: {passed} passed, {failed} failed")
    print("=" * 45)
