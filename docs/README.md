
# Basic docker config


## Easiest option: docker compose

Navigate to docker/ and run:

`docker-compose up`

This sets up everything.

Then, open with a brouser the url: `http://<host>/init` and fillout the setup form. After this, the server is ready.

## Generic deployment
Pull with `docker pull franspaco/moviles1`

Run with

`sudo docker run --name <some-name> --env MONGO_HOST=<MONGODB_HOST> -p 80:80 -d franspaco/moviles1`


Optional:
`--link <mongo_container>`
`--restart always`

## Azure deployment

Requires a mongo container.

`docker run --name <some-name> --env MONGO_HOST=<MONGODB_HOST> -p 80:80 -d franspaco/moviles1`

Demo of run currently being used:

`docker run --name srvr1 --env MONGO_HOST=mongo-restart -p 80:80 --restart always --link mongo-restart -d franspaco/moviles1`


## Env vars:

* HOST: the host for the server (default: 0.0.0.0)
* PORT: the port to listen to (default: 80)
* MONGO_HOST: host of the mongo database (default: localhost)
* MONGO_PORT: port of the mongo database (default: 27017)


# Set up:

Open up the address of the server. It should respond "Hello world"

Go to `http://<host>/init` and fill out the form.
