pip3 install -r requirements.txt
docker compose -f docker-compose.yml up -d --build
docker logs server -f