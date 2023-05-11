workers = 4
max_requests = 1000
timeout = 30
bind = "0.0.0.0:8001"
preload_app = True
accesslog = "/var/log/gunicorn/foodswipe/access.log"
errorlog = "/var/log/gunicorn/foodswipe/error.log"
