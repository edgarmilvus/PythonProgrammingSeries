
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

# Source File: solution_exercise_4.py
# Description: Solution for Exercise 4
# ==========================================

# --- Exercise 3 Solution ---
# Using the base script structure defined above.

OUTPUT_FILENAME = 'generated_track_ex3_crossfade.wav'
GENERATION_DURATION_SECONDS = 40 

async def steer_music_task(session):
    """
    Task to implement a smooth cross-fade between two weighted prompts (Ambient -> Rock).
    """
    print("\n--- Prompt Cross-Fade Task Initialized ---")
    
    # Wait 10 seconds for the initial ambient music to establish
    await asyncio.sleep(10)
    print("TIME 10s: Starting cross-fade transition...")
    
    # Define the starting and ending weights and the transition parameters
    WEIGHT_A_START = 1.5
    WEIGHT_B_START = 0.1
    STEPS = 10 # 10 steps over 20 seconds (2 seconds per step)
    
    # Calculate the incremental change needed for each step
    DECREMENT = (WEIGHT_A_START - 0.1) / STEPS 
    INCREMENT = (1.5 - WEIGHT_B_START) / STEPS 

    current_weight_a = WEIGHT_A_START
    current_weight_b = WEIGHT_B_START
    
    for i in range(STEPS):
        # Update weights
        current_weight_a -= DECREMENT
        current_weight_b += INCREMENT
        
        # Ensure weights stay within reasonable bounds
        current_weight_a = max(0.1, current_weight_a)
        current_weight_b = min(1.5, current_weight_b)

        # Send the updated prompt weights
        new_prompts = [
            types.WeightedPrompt(text='Ambient, Spacey Synths, Ethereal Ambience', weight=current_weight_a),
            types.WeightedPrompt(text='Garage Rock, Crunchy Distortion, Funk Drums', weight=current_weight_b),
        ]
        
        await session.set_weighted_prompts(prompts=new_prompts)
        
        print(f"Step {i+1}/{STEPS}: Ambient Weight={current_weight_a:.2f}, Rock Weight={current_weight_b:.2f}")
        
        await asyncio.sleep(2) # Wait 2 seconds before the next update

    print("Cross-fade complete. Rock focus established.")
    
    # Wait for the remaining duration before the session ends
    await asyncio.sleep(10) 


async def generate_music_session(duration: int, initial_prompts: list, initial_config: types.LiveMusicGenerationConfig):
    """
    Manages the connection, configuration, generation, and termination of the 
    Lyria RealTime session, integrating the steering task. (Same as Ex 2 structure)
    """
    audio_writer = AudioFileWriter(OUTPUT_FILENAME)
    audio_writer.open()

    try:
        async with client.aio.live.music.connect(model=MUSIC_MODEL) as session:
            
            async with asyncio.TaskGroup() as tg:
                
                audio_task = tg.create_task(receive_audio(session, audio_writer))
                steering_task = tg.create_task(steer_music_task(session))

                print("Setting initial configuration and prompts...")
                await session.set_weighted_prompts(prompts=initial_prompts)
                await session.set_music_generation_config(config=initial_config)

                await session.play()
                print(f"Generation started. Will run for {duration} seconds...")

                await asyncio.sleep(duration)

                await session.stop()
                print("Generation stopped by timer.")
                
                audio_task.cancel()
                steering_task.cancel()

    except Exception as e:
        print(f"An unexpected error occurred during the session: {e}")
    finally:
        audio_writer.close()


async def main():
    """Defines the parameters for Exercise 3: Dynamic Prompt Weighting."""
    
    # Initial state must match the starting weights in steer_music_task
    initial_prompts = [
        types.WeightedPrompt(text='Ambient, Spacey Synths, Ethereal Ambience', weight=1.5),
        types.WeightedPrompt(text='Garage Rock, Crunchy Distortion, Funk Drums', weight=0.1),
    ]
    
    initial_config = types.LiveMusicGenerationConfig(
        bpm=110,
        temperature=1.0,
        density=0.5,
        music_generation_mode=types.MusicGenerationMode.QUALITY
    )
    
    await generate_music_session(
        duration=GENERATION_DURATION_SECONDS,
        initial_prompts=initial_prompts,
        initial_config=initial_config
    )

if __name__ == "__main__":
    if not os.getenv("GEMINI_API_KEY"):
        print("CRITICAL: GEMINI_API_KEY environment variable not set.")
    else:
        asyncio.run(main())
