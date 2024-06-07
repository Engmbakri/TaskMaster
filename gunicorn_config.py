import multiprocessing
import os

workers = 1  # Use a single worker to limit memory usage
worker_class = 'sync'
timeout = 120  # Increase the timeout to 120 seconds to handle long-running requests

# Bind to the port specified in the PORT environment variable
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
