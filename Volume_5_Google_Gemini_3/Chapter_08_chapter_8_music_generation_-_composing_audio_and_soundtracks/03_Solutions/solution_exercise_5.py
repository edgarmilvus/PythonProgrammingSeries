
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

# Source File: solution_exercise_5.py
# Description: Solution for Exercise 5
# ==========================================

# --- Exercise 4 Solution ---
# Using the base script structure defined above.

GENERATION_DURATION_SECONDS = 30 
# OUTPUT_FILENAME is now passed dynamically

async def receive_audio(session, audio_writer: AudioFileWriter):
    """
    Background task to continuously receive and process incoming audio chunks.
    (Included again for completeness, same as base script)
    """
    print("Audio receiver task started.")
    try:
        async for message in session.receive():
            if (message.server_content and 
                message.server_content.audio_chunks and 
                message.server_content.audio_chunks[0].data):
                
                audio_data = message.server_content.audio_chunks[0].data
                audio_writer.write_chunk(audio_data)
                
            await asyncio.sleep(10**-12) 
            
    except asyncio.CancelledError:
        print("Audio receiving task cancelled.")
    except Exception as e:
        print(f"An error occurred in receive_audio: {e}")

async def generate_music_session(duration: int, output_filename: str, initial_prompts: list, initial_config: types.LiveMusicGenerationConfig):
    """
    Manages the connection, configuration, generation, and termination of the 
    Lyria RealTime session for static generation (Task A/B).
    """
    audio_writer = AudioFileWriter(output_filename) 
    audio_writer.open()

    try:
        async with client.aio.live.music.connect(model=MUSIC_MODEL) as session:
            async with asyncio.TaskGroup() as tg:
                
                audio_task = tg.create_task(receive_audio(session, audio_writer))

                print("Setting initial configuration and prompts...")
                await session.set_weighted_prompts(prompts=initial_prompts)
                await session.set_music_generation_config(config=initial_config)

                await session.play()
                print(f"Generation started. Will run for {duration} seconds...")

                await asyncio.sleep(duration)

                await session.stop()
                print("Generation stopped by timer.")
                
                audio_task.cancel()

    except Exception as e:
        print(f"An unexpected error occurred during the session: {e}")
    finally:
        audio_writer.close()


async def main():
    """Defines the parameters for Exercise 4: Technical Configuration Deep Dive."""
    
    base_prompts = [
        types.WeightedPrompt(text='Lo-Fi Hip Hop, Rhodes Piano, Tight Groove', weight=1.0),
    ]
    
    # --- Task A: High Guidance / High Density (Adherence and Complexity) ---
    print("\n--- Running Task A: High Guidance/Density (lofi_A.wav) ---")
    config_a = types.LiveMusicGenerationConfig(
        bpm=90,
        guidance=5.5, # High guidance: Model sticks strictly to "Lo-Fi Hip Hop"
        density=0.9,  # High density: Busy, many notes/sounds
        brightness=0.3, # Low brightness: Muffled, characteristic Lo-Fi sound
        music_generation_mode=types.MusicGenerationMode.QUALITY
    )
    await generate_music_session(
        duration=GENERATION_DURATION_SECONDS,
        output_filename='lofi_A.wav',
        initial_prompts=base_prompts,
        initial_config=config_a
    )

    # Wait briefly before starting the next session
    await asyncio.sleep(2)
    
    # --- Task B: Low Guidance / Low Density / High Diversity (Creativity and Sparseness) ---
    print("\n--- Running Task B: Low Guidance/Diversity (lofi_B.wav) ---")
    config_b = types.LiveMusicGenerationConfig(
        bpm=90,
        guidance=1.5, # Low guidance: Model is free to wander from the prompt
        density=0.2,  # Low density: Very sparse, minimalist
        brightness=0.8, # High brightness: Clearer, higher frequencies emphasized
        music_generation_mode=types.MusicGenerationMode.DIVERSITY # Focus on novelty
    )
    await generate_music_session(
        duration=GENERATION_DURATION_SECONDS,
        output_filename='lofi_B.wav',
        initial_prompts=base_prompts,
        initial_config=config_b
    )

if __name__ == "__main__":
    if not os.getenv("GEMINI_API_KEY"):
        print("CRITICAL: GEMINI_API_KEY environment variable not set.")
    else:
        asyncio.run(main())
