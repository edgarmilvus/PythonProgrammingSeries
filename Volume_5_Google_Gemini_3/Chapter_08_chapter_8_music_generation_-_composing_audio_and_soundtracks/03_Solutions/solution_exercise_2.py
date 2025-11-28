
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

# Source File: solution_exercise_2.py
# Description: Solution for Exercise 2
# ==========================================

# --- Exercise 1 Solution ---
# Using the base script structure defined above.

OUTPUT_FILENAME = 'generated_track_ex1_orchestral.wav'
GENERATION_DURATION_SECONDS = 45 

async def generate_music_session(duration: int, initial_prompts: list, initial_config: types.LiveMusicGenerationConfig):
    """
    Manages the connection, configuration, generation, and termination of the 
    Lyria RealTime session (Static Version).
    """
    audio_writer = AudioFileWriter(OUTPUT_FILENAME)
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
    """Defines the parameters for Exercise 1: Prompt Engineering."""
    
    # EXERCISE 1 MODIFICATION (Focus: Orchestral Score)
    
    # Define the desired musical style
    initial_prompts = [
        types.WeightedPrompt(text='Rich Orchestration', weight=1.5),
        types.WeightedPrompt(text='Cello', weight=1.0),
        types.WeightedPrompt(text='Ethereal Ambience', weight=0.7),
        types.WeightedPrompt(text='Subdued Melody', weight=0.4),
    ]
    
    # Define the musical structure and quality
    initial_config = types.LiveMusicGenerationConfig(
        bpm=90, # Slower tempo for dramatic effect
        temperature=0.8, # Lower temperature for predictability and coherence
        density=0.3, # Sparser arrangement
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
