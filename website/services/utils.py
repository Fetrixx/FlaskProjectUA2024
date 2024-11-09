def extract_video_id(url):
    """Extrae el ID del video de una URL de YouTube."""
    if "youtu.be" in url:
        return url.split("/")[-1]
    elif "youtube.com/watch?v=" in url:
        return url.split("v=")[-1]
    return None