import resource
import sys
import plex
import os
from dotenv import load_dotenv

load_dotenv()

MEMORY_LIMIT = os.getenv('MEMORY_LIMIT')

# Set the order_by parameter to 'aired' or 'added'
order_by = 'added'
download_movies = True
download_series = True
# Set the number of latest movies to download
limit = 10

# Create a directory to save the backgrounds
background_dir = "plex_backgrounds"

def memory_limit_half():
    """Limit max memory usage to half."""
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    # Convert KiB to bytes, and divide in two to half
    resource.setrlimit(resource.RLIMIT_AS, (int(get_memory() * 1024 / MEMORY_LIMIT), hard))

def get_memory():
    with open('/proc/meminfo', 'r') as mem:
        free_memory = 0
        for i in mem:
            sline = i.split()
            if str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
                free_memory += int(sline[1])
    return free_memory  # KiB

if __name__ == '__main__':
    memory_limit_half()
    try:
        # Download the latest movies according to the specified order and limit
        if download_movies:
            plex.download_latest_media(order_by, limit, 'movie')

        # Download the latest TV series according to the specified order and limit
        if download_series:
            plex.download_latest_media(order_by, limit, 'tv')
    except MemoryError:
        sys.stderr.write('\n\nERROR: Memory Exception\n')
        sys.exit(1)