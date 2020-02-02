#/bin/bash
sudo docker exec -it $(sudo docker inspect --format="{{.Id}}" "${PWD##*/}_api_1") python client.py
