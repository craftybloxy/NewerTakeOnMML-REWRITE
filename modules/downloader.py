import subprocess

def run_downloader(urls):
    """
    Downloads songs from the given Spotify URLs using the spotify-web-downloader command-line tool.

    Args:
        urls (str or list of str): A single URL or a list of URLs to download.
    """
    # Convert a single URL to a list
    if isinstance(urls, str):
        urls = [urls]

    command = ['spotify-web-downloader', '--template-folder-album', '{album_artist} - {album}'] + urls

    try:
        # Start the process
        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
            # Read and display output line by line
            for stdout_line in process.stdout:
                print(stdout_line, end='')  # Print stdout line by line
            
            # Read and display error line by line
            for stderr_line in process.stderr:
                print(stderr_line, end='')  # Print stderr line by line
            
            # Wait for the process to complete and get the return code
            return_code = process.wait()
            print(f"\nReturn Code: {return_code}")

            # Check if the command was successful
            if return_code != 0:
                print(f"Command failed with return code {return_code}")
    except Exception as e:
        print(f"An error occurred while running the command: {e}")

if __name__ == '__main__':
    run_downloader("https://open.spotify.com/track/0ll8uFnc0nANY35E0Lfxvg?si=86ac6189c5264021")
