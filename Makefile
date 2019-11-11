build:
	docker build -t wg-gesucht .

run: build
	docker run -it \
	-e username="${username}" \
	-e password="${password}" \
	-e application_id="${application_id}" \
	-e title1="${title1}" \
	-e title2="${title2}" \
	-e debug_wg_gesucht="false" \
	wg-gesucht
