import multiprocessing

workers = 1  # Use a single worker to limit memory usage
worker_class = 'sync'
timeout = 120  # Increase the timeout to 120 seconds to handle long-running requests
