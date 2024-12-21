import subprocess
import os

def extract_frames(input_video, output_dir, fps=None):
    """
    Extracts frames from a video using FFmpeg.
    
    Args:
        input_video (str): Path to the input video file.
        output_dir (str): Directory to save the extracted frames.
        fps (int, optional): Frames per second to extract. If None, extracts all frames.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Construct the FFmpeg command
    output_pattern = os.path.join(output_dir, "output_%04d.png")
    if fps:
        command = [
            "ffmpeg", "-i", input_video, "-vf", f"fps={fps}", output_pattern
        ]
    else:
        command = [
            "ffmpeg", "-i", input_video, output_pattern
        ]
    
    # Run the command
    try:
        subprocess.run(command, check=True)
        print(f"Frames extracted successfully to {output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    except FileNotFoundError:
        print("FFmpeg is not installed or not found in the system PATH.")

def assemble_frames_to_video(input_dir, output_video, fps=30):
    """
    Assembles frames into a video using FFmpeg.
    
    Args:
        input_dir (str): Directory containing the frames (e.g., `frames`).
        output_video (str): Path to the output video file (e.g., `output.mp4`).
        fps (int): Frames per second for the output video.
    """
    # Construct the FFmpeg command
    input_pattern = os.path.join(input_dir, "output_%04d.png")
    command = [
        "ffmpeg", "-framerate", str(fps), "-i", input_pattern, "-pix_fmt", "yuv420p", output_video
    ]
    
    # Run the command
    try:
        subprocess.run(command, check=True)
        print(f"Video assembled successfully: {output_video}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    except FileNotFoundError:
        print("FFmpeg is not installed or not found in the system PATH.")


# Example usage
if __name__ == "__main__":
    # input_video = "resources/bad_apple.mp4"  # Path to your MP4 file
    # output_dir = "frames"     # Directory to save the frames
    
    # extract_frames(input_video, output_dir)

    input_dir = "processed"           # Directory containing the frames
    output_video = "output.mp4"    # Output video file
    fps = 30                       # Frames per second for the video
    
    assemble_frames_to_video(input_dir, output_video, fps)

