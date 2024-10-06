cd backend
daphne --verbosity 2 -b 0.0.0.0 -p 8001 comments_spa.asgi:application