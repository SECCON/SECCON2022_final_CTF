UID := $(shell id -u)
GID := $(shell id -g)

migrate:
	docker-compose -f docker-compose.yml exec -w /app app python3 manage.py migrate

seed:
	docker-compose -f docker-compose.yml exec -w /app app python3 manage.py loaddata witchquiz/datas/*.json

up:
	env UID=$(UID) GID=$(GID) docker-compose -f docker-compose.yml up -d

build:
	docker-compose build

setrounddata:
	docker-compose -f docker-compose.yml exec -Tw /app app python3 manage.py shell < set_rounddata.py
