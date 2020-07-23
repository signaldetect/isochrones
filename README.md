# Isochrones

Builds an isochrone map for found objects within the specified city.

## Installing and running

```sh
docker pull nats
docker run -d --name msgs -p 4222:4222 -p 6222:6222 -p 8222:8222 nats
git clone https://github.com/signaldetect/isochrones.git
cd isochrones/
. _cli/setup.sh
export TOMTOM_KEY=<YOUR TOMTOM API KEY>
. _cli/start.sh
```

## Using request

Endpoint:

`GET /api/isochrones.pbf?<parameters>`

Parameters:

* `place` is a place (city) name, e.g. "New York City, NY, USA"

* `facility` is a facility name/type, e.g. "Subway station"

* `trip_time` is a trip (walking) time from a facility, in minutes, e.g. "5"

Note: The process of building a map takes some time, therefore the endpoint
response may take a long time, so just wait for the file to start downloading.

## Using simple CLI

* install system:

```sh
. _cli/setup.sh
```

* start system:

```sh
. _cli/start.sh
```

* stop system:

```sh
. _cli/stop.sh
```

* terminate system and `supervisor`:

```sh
. _cli/terminate.sh
```

* restart system:

```sh
. _cli/restart.sh
```

* terminate and then start system:

```sh
. _cli/restart.sh --hard
```

* view status of system:

```sh
. _cli/status.sh
```
