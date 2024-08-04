# amarillo-gtfs-generator
Generate GTFS from carpools as standalone (Docker) service.

This service complements the Amarillo application, creating GTFS and GTFS-RT data from the enhanced Amarillo carpool files. 
It is a non-public backend service called from the Amarillo FastAPI application.
You can run it as part of docker compose, or separately using the instructions below.

# Overview

 ![Amarillo GTFS generation overview](/docs-overview-diagram.png)

# Usage

## 1. Configuration

### Create `data/stop_sources.json`

Example contents:
```json
[
    {"url": "https://datahub.bbnavi.de/export/rideshare_points.geojson", "vicinity": 50},
    {"url": "https://data.mfdz.de/mfdz/stops/stops_zhv.csv", "vicinity": 50},
    {"url": "https://data.mfdz.de/mfdz/stops/parkings_osm.csv", "vicinity": 500}
]
```

### Add region files `data/region`

File name should be `{region_id}.json`.

Example (`by.json`):
```json
{"id": "by", "bbox": [ 8.97, 47.28, 13.86, 50.56]}
```
For each region a separate GTFS zip file will be created in `/data/gtfs`, only containing the trips that intersect the region's bounding box.

### Add agency files `data/agency`

File name should be `{agency_id}.json`.

Example (`mfdz.json`):
```json
{
  "id": "mfdz",
  "name": "MITFAHR|DE|ZENTRALE",
  "url": "http://mfdz.de",
  "timezone": "Europe/Berlin",
  "lang": "de",
  "email": "info@mfdz.de"
}
```
The generator will use this data to populate agency.txt in the GTFS output.

### Uvicorn configuration

`amarillo-gtfs-generator` uses `uvicorn` to run. Uvicorn can be configured as normal by passing in arguments such as `--port 8002` to change the port number.

## 2. Install the gtfs-exporter plugin for Amarillo

This is a separate service and not used by Amarillo by default. You should use the  [amarillo-gtfs-exporter plugin](https://github.com/mfdz/amarillo-gtfs-exporter) which creates endpoints for `/region/{region_id}/gtfs` and `/region/{region_id}/gtfs-rt` on your Amarillo instance. These will serve the GTFS zip files from `data/gtfs`, or if they do not exist yet, they will call the configured generator and cache the results.

## 3. Add carpools to Amarillo

Use Amarillo's `/carpool` endpoint to create new carpools. The generator listens to file system events in the `/data/enhanced` folder to recognize newly added or deleted carpools. It will also discover existing carpools on startup. GTFS generation happens automatically on startup, at midnight on a schedule, and by sending a GET request to a `/region/{region_id}/gtfs` or `/region/{region_id}/gtfs-rt` endpoint.

Amarillo will use its configured enhancer to create enhanced carpool files. They will get picked up by the generator and they will be included in the next batch of generated GTFS data. Changes to carpools will be reflected immediately in the GTFS-RT output.

<!-- Q: how immediately? -->

# Run with uvicorn

- Python 3.10 with pip
- python3-venv

Create a virtual environment `python3 -m venv venv`.

Activate the environment and install the dependencies `pip install -r requirements.txt`.

Run `uvicorn amarillo_gtfs_generator.gtfs_generator:app`. 

In development, you can use `--reload`. 

# Run with docker
You can download a container image from the [MFDZ package registry](https://github.com/orgs/mfdz/packages?repo_name=amarillo-gtfs-generator).

Example command:
```bash
docker run -it --rm --name amarillo-gtfs-generator -p 8002:80 -e TZ=Europe/Berlin -v $(pwd)/data:/app/data amarillo-gtfs-generator```