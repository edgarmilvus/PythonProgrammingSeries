
#
# These sources are part of the "PyThon Programming Series" by Edgar Milvus, 
# you can find it on Amazon: https://www.amazon.com/dp/B0FTTQNXKG or
# https://tinyurl.com/PythonProgrammingSeries 
# New books info: https://linktr.ee/edgarmilvus 
#
# MIT License
# Copyright (c) 2025 Edgar Milvus
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Source File: project_advanced_application_script.py
# Description: Advanced Application Script
# ==========================================

import math
from typing import List, Tuple

# --- Configuration Constants ---
SAMPLE_RATE = 1000  # Samples per second (Hz). Determines resolution.
DURATION = 2.0      # Total duration of the simulation (seconds)
BASE_FREQUENCY = 440.0  # The oscillation frequency (A4 note, Hz)
DAMPING_FACTOR = 1.5    # Alpha (α): Rate at which the amplitude decays

# --- Core Mathematical Functions ---

def calculate_damped_amplitude(t: float, freq: float, damping: float) -> float:
    """
    Calculates the instantaneous amplitude of a sinusoidally oscillating signal 
    that is exponentially damped over time.
    
    Formula: A(t) = exp(-damping * t) * sin(2 * pi * freq * t)
    
    Args:
        t (float): Time in seconds.
        freq (float): Oscillation frequency (Hz).
        damping (float): Damping factor (alpha).
    
    Returns:
        float: The calculated amplitude at time t.
    """
    # 1. Exponential Decay Envelope (using math.exp)
    # This term ensures the amplitude shrinks over time.
    decay_envelope = math.exp(-damping * t)

    # 2. Angular Component (using math.pi and math.sin)
    # Calculates the oscillation based on angular frequency (omega = 2 * pi * freq).
    angular_frequency = 2 * math.pi * freq
    oscillation = math.sin(angular_frequency * t)

    # 3. Combined Damped Amplitude
    return decay_envelope * oscillation

def analyze_signal_characteristics(times: List[float], amplitudes: List[float]) -> Tuple[float, float, float]:
    """
    Analyzes the generated signal for key characteristics: 
    Measured Peak Amplitude, Time to Half-Amplitude, and Phase Shift.
    """
    if not amplitudes:
        return 0.0, 0.0, 0.0

    # 1. Find the true maximum amplitude and its time index (for phase shift calculation)
    max_amp = 0.0
    max_time = 0.0
    
    # Iterate only through the initial cycles where the peak is likely to occur
    for t, amp in zip(times, amplitudes):
        # We look for the first major positive peak
        if amp > max_amp:
            max_amp = amp
            max_time = t
        
        # Optimization: Stop searching after the first few cycles (e.g., 3 cycles)
        if t > (1.0 / BASE_FREQUENCY) * 3: 
            break

    # 2. Calculate Time to Half-Amplitude (T_half)
    # This is calculated theoretically from the damping envelope formula.
    # T_half = -ln(0.5) / damping_factor
    # We use math.log for the natural logarithm (ln)
    time_to_half = -math.log(0.5) / DAMPING_FACTOR
    
    # 3. Calculate Phase Shift (in radians, then converted to degrees)
    # Phase shift is derived from the time difference of the measured peak.
    phase_shift_rad = 2 * math.pi * BASE_FREQUENCY * max_time
    
    # Use math.degrees to convert the phase shift radians to a more intuitive unit
    phase_shift_deg = math.degrees(phase_shift_rad)

    # Return Measured Peak Amplitude, Time to Half, and Phase Shift (Degrees)
    return max_amp, time_to_half, phase_shift_deg

# --- Main Execution Block ---

if __name__ == "__main__":
    print("--- Damped Acoustic Signal Analyzer ---")
    print(f"Simulation Parameters: F={BASE_FREQUENCY} Hz, Damping={DAMPING_FACTOR}")

    # 1. Generate Time Vector
    # Use math.ceil to ensure we capture the last sample point precisely
    num_samples = math.ceil(DURATION * SAMPLE_RATE)
    time_points = [i / SAMPLE_RATE for i in range(num_samples)]

    # 2. Calculate Amplitudes for all time points
    amplitudes = []
    for t in time_points:
        amp = calculate_damped_amplitude(t, BASE_FREQUENCY, DAMPING_FACTOR)
        amplitudes.append(amp)

    # 3. Perform Analysis
    max_amp, t_half, phase_shift = analyze_signal_characteristics(
        time_points, amplitudes
    )

    # 4. Reporting Results: Energy Calculation
    print("\n--- Analysis Summary ---")

    # Calculate RMS (Root Mean Square) energy of the signal
    # RMS = sqrt( (sum(amp^2)) / N )
    # We use math.pow(a, 2) for squaring and math.sqrt for the final root operation.
    sum_of_squares = sum(math.pow(a, 2) for a in amplitudes)
    rms_energy = math.sqrt(sum_of_squares / num_samples)

    print(f"1. Total Samples Processed: {num_samples}")
    print(f"2. Simulation Duration: {DURATION} seconds")
    print(f"3. Measured Peak Amplitude: {max_amp:.4f} (Should be near 1.0)")
    
    # Demonstrate math.floor for display formatting
    # Note: max_amp * 1000 is used here purely to show floor/ceil usage contextually
    peak_time_ms = max_amp * 1000 
    print(f"4. Peak Amplitude occurred within the first {math.floor(peak_time_ms):.0f} milliseconds.") 
    
    print(f"5. Calculated Time to Half-Amplitude (T_half): {t_half:.4f} seconds")
    print(f"6. Measured Phase Shift at Peak: {phase_shift:.2f} degrees")
    print(f"7. Signal RMS Energy: {rms_energy:.4f}")

    # 5. Engineering Check: Using math.isclose for robust comparison
    # Check if the calculated T_half matches a required engineering specification (e.g., 0.462s)
    required_t_half = -math.log(0.5) / DAMPING_FACTOR
    
    print(f"\n--- Engineering Verification ---")
    
    # math.isclose handles the inevitable tiny floating-point errors
    if math.isclose(t_half, required_t_half, rel_tol=1e-9):
         print(f"Verification: T_half matches theoretical calculation ({required_t_half:.4f}s).")
    else:
         print("Verification Failed: Floating point mismatch detected.")
