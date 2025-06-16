# to buid docker image run
docker build --no-cache . -t user/message

# to run docker container run
docker run -p 3000:3000 -v "/c/Users/ultra/message-storage":"/app/storage" -d user/message

# follow the link
http://localhost:3000