workers = 4
max_requests = 1000
timeout = 30
bind = "0.0.0.0:8002"
preload_app = True
accesslog = "/home/ubuntu/dev/foodswipe/BackEnd/logs/gunicorn/access.log"
errorlog = "/home/ubuntu/dev/foodswipe/BackEnd/logs/gunicorn/error.log"