import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
bind = "0.0.0.0:10000"
timeout = 120  # aumento do timeout para 120 segundos
worker_class = "gevent"