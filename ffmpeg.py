import subprocess

# Define the FFmpeg command
command = [
    'ffmpeg',
    '-framerate', '30',
    '-i', 'edges/frame_%04d.png',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    'edges.mp4'
]

command2 = [
    'ffmpeg',
    '-framerate', '30',
    '-i', 'processed/frame_%04d.png',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    'processed.mp4'
]

command3 = [
    'ffmpeg',
    '-i', 'edges.mp4',
    '-i', 'processed.mp4',
    '-filter_complex', '[0][1]hstack=inputs=2',
    '-c:v', 'libx264',
    '-crf', '23',
    '-preset', 'fast',
    'row.mp4'
]

# Run the command
# subprocess.run(command)
subprocess.run(command2)
# subprocess.run(command3)
