
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

# Source File: solution_exercise_3.py
# Description: Solution for Exercise 3
# ==========================================

# --- Exercise 2 Solution ---
# Using the base script structure defined above.

OUTPUT_FILENAME = 'generated_track_ex2_steering.wav'
GENERATION_DURATION_SECONDS = 40 

async def steer_music_task(session):
    """
    Task to send real-time configuration updates to the model.
    """
    print("\n--- Steering Task Initialized ---")
    
    # Wait 15 seconds into the track
    await asyncio.sleep(15)
    print("TIME 15s: Changing BPM and Scale...")
    
    # Configuration Update 1: Change to a faster tempo and a different scale
    new_config_1 = types.LiveMusicGenerationConfig(
        bpm=150, # Drastic increase
        scale=types.Scale.B_MAJOR_A_FLAT_MINOR,
        density=0.9,
        temperature=1.5 # Increase temperature for more unpredictable output
    )
    
    await session.set_music_generation_config(config=new_config_1)
    
    # CRITICAL: Must reset context for BPM/Scale changes to take effect
    await session.reset_context() 
    print("Context reset. Expecting an abrupt transition.")
    
    # Wait another 15 seconds
    await asyncio.sleep(15)
    print("TIME 30s: Returning to original tempo and key...")
    
    # Configuration Update 2: Revert to a calmer state
    new_config_2 = types.LiveMusicGenerationConfig(
        bpm=100,
        scale=types.Scale.C_MAJOR_A_MINOR,
        density=0.5,
        temperature=1.0
    )
    
    await session.set_music_generation_config(config=new_config_2)
    await session.reset_context()
    print("Context reset. Returning to calm.")


async def generate_music_session(duration: int, initial_prompts: list, initial_config: types.LiveMusicGenerationConfig):
    """
    Manages the connection, configuration, generation, and termination of the 
    Lyria RealTime session, integrating the steering task.
    """
    audio_writer = AudioFileWriter(OUTPUT_FILENAME)
    audio_writer.open()

    try:
        async with client.aio.live.music.connect(model=MUSIC_MODEL) as session:
            
            async with asyncio.TaskGroup() as tg:
                
                # 1. Start the background tasks
                audio_task = tg.create_task(receive_audio(session, audio_writer))
                steering_task = tg.create_task(steer_music_task(session)) # <-- Integrated Steering

                # 2. Send initial configuration
                print("Setting initial configuration and prompts...")
                await session.set_weighted_prompts(prompts=initial_prompts)
                await session.set_music_generation_config(config=initial_config)

                # 3. Start streaming music
                await session.play()
                print(f"Generation started. Will run for {duration} seconds...")

                # 4. Wait for the specified duration
                await asyncio.sleep(duration)

                # 5. Stop the generation and close the session gracefully
                await session.stop()
                print("Generation stopped by timer.")
                
                # Cancel tasks
                audio_task.cancel()
                steering_task.cancel()

    except Exception as e:
        print(f"An unexpected error occurred during the session: {e}")
    finally:
        audio_writer.close()


async def main():
    """Defines the parameters for Exercise 2: Real-Time Configuration Steering."""
    
    # Initial calm state for contrast
    initial_prompts = [
        types.WeightedPrompt(text='Ambient Chillout', weight=1.0),
        types.WeightedPrompt(text='Synth Pads', weight=0.5),
    ]
    
    initial_config = types.LiveMusicGenerationConfig(
        bpm=100,
        temperature=1.0,
        density=0.5,
        scale=types.Scale.C_MAJOR_A_MINOR,
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
