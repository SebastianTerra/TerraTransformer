from moviepy.editor import VideoFileClip

def convert_mp4_to_gif(input_video_path, output_gif_path):
    """
    Converts an MP4 video file to a GIF.

    :param input_video_path: Path to the input MP4 video file
    :param output_gif_path: Path where the output GIF will be saved
    """
    try:
        # Load the video file
        clip = VideoFileClip(input_video_path)

        # Convert video to GIF and save
        clip.write_gif(output_gif_path)

        print(f"GIF created successfully at: {output_gif_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_video_path = "./extract.mp4"  # Replace with your video file path
output_gif_path = "output_video.gif"  # Replace with desired GIF file path
convert_mp4_to_gif(input_video_path, output_gif_path)
