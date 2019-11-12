build:
	docker build -t wg-gesucht .

run: build
	docker run -d --env-file ./env-file --name=wg-gesucht wg-gesucht
