from src import get_path, get_input_file_content
from src.prepare_outline import prepare_podcast_outline
from src.generate_podcast import generate_podcast_from_script

input_file_path, input_file_name = get_path()
print(f"Processing file: {input_file_path}")

print("Preparing Podcast script based on file content...", end="", flush=True)
file_content = get_input_file_content(input_file_path)
podcast_outline = prepare_podcast_outline(raw_input=file_content,name=input_file_name)
print("\rPreparing Podcast script based on file content — ✅ Done")

print("Generating Podcast MP3 File...", end="", flush=True)
generated_file = generate_podcast_from_script(podcast_outline, out_name=input_file_name)
print("\rGenerating Podcast MP3 File — ✅ Done")
print(f"Generated podcast file: {generated_file}")
