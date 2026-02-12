/**
 * Audio Engine — Web Audio API
 * Synthesizes pop/bubble sounds for emoji reactions.
 * No external audio files needed!
 */

class AudioEngine {
    constructor() {
        this.ctx = null;
        this.enabled = true;
        this.volume = 0.15;
        this.initialized = false;
    }

    /** Initialize AudioContext (must be called after user gesture) */
    init() {
        if (this.initialized) return;
        try {
            this.ctx = new (window.AudioContext || window.webkitAudioContext)();
            this.initialized = true;
        } catch (e) {
            console.warn('Web Audio not available:', e);
            this.enabled = false;
        }
    }

    /** Play a bubbly pop sound */
    playPop() {
        if (!this.enabled || !this.ctx) return;

        const now = this.ctx.currentTime;

        // Oscillator — short sine wave chirp
        const osc = this.ctx.createOscillator();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(600, now);
        osc.frequency.exponentialRampToValueAtTime(1200, now + 0.04);
        osc.frequency.exponentialRampToValueAtTime(300, now + 0.12);

        // Gain envelope — quick attack, fast decay
        const gain = this.ctx.createGain();
        gain.gain.setValueAtTime(0, now);
        gain.gain.linearRampToValueAtTime(this.volume, now + 0.01);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.15);

        // Subtle noise burst for texture
        const noiseGain = this.ctx.createGain();
        noiseGain.gain.setValueAtTime(this.volume * 0.3, now);
        noiseGain.gain.exponentialRampToValueAtTime(0.001, now + 0.06);

        const bufferSize = this.ctx.sampleRate * 0.06;
        const noiseBuffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
        const data = noiseBuffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
            data[i] = (Math.random() * 2 - 1) * 0.5;
        }
        const noise = this.ctx.createBufferSource();
        noise.buffer = noiseBuffer;

        // Filter the noise to sound more like a bubble
        const filter = this.ctx.createBiquadFilter();
        filter.type = 'bandpass';
        filter.frequency.value = 2000;
        filter.Q.value = 2;

        // Connect graph
        osc.connect(gain);
        gain.connect(this.ctx.destination);

        noise.connect(filter);
        filter.connect(noiseGain);
        noiseGain.connect(this.ctx.destination);

        // Play
        osc.start(now);
        osc.stop(now + 0.15);
        noise.start(now);
        noise.stop(now + 0.06);
    }

    /** Play a slightly different pop for burst reactions */
    playBurstPop() {
        if (!this.enabled || !this.ctx) return;

        const now = this.ctx.currentTime;
        const baseFreq = 400 + Math.random() * 400;

        const osc = this.ctx.createOscillator();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(baseFreq, now);
        osc.frequency.exponentialRampToValueAtTime(baseFreq * 2.5, now + 0.03);
        osc.frequency.exponentialRampToValueAtTime(baseFreq * 0.5, now + 0.1);

        const gain = this.ctx.createGain();
        gain.gain.setValueAtTime(0, now);
        gain.gain.linearRampToValueAtTime(this.volume * 0.7, now + 0.005);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);

        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.start(now);
        osc.stop(now + 0.12);
    }

    toggle() {
        this.enabled = !this.enabled;
        return this.enabled;
    }
}

window.AudioEngine = AudioEngine;
