from pytube import YouTube

def get_video_title(video_url):
    try:
        yt = YouTube(video_url)
        return yt.title
    except Exception as e:
        print("Error:", e)
        return None

# Example usage:
video_url = "https://www.youtube.com/watch?v=dD_xNmePdd0&ab_channel=SamuelChan"
video_title = get_video_title(video_url)
if video_title:
    print("Title of the video:", video_title)
else:
    print("Failed to retrieve the video title.")
