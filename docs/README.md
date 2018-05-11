
# Deployment
The server is deployed using docker. It lives in the image [franspaco/moviles2](https://hub.docker.com/r/franspaco/moviles2/) which is based on [tiangolo/uwsgi-nginx-flask](https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask/).

This image provides a flask+uwsgi+nginx instalaltion onto which the app is inserted.

## Easiest option: docker compose
Navigate to `docker/` where `docker-compose.yml` resides and run:

`docker-compose up`

This sets up everything.

## Generic deployment

It is recommended to use a mongo container, see [Mongo in DockerHub](https://hub.docker.com/_/mongo/).

Pull with `docker pull franspaco/moviles2`

Run with

`sudo docker run --name <some-name> --env MONGO_HOST=<MONGODB_HOST> -p 80:80 -d franspaco/moviles2`


Optional:
`--link <mongo_container>`
`--restart always`

### Azure deployment

`docker run --name <some-name> --env MONGO_HOST=<MONGODB_HOST> -p 80:80 -d franspaco/moviles2`

Example. The configuration currently running for the demo.

`docker run --name srvr1 --env MONGO_HOST=mongo-restart -p 80:80 --restart always --link mongo-restart -d franspaco/moviles2`


## Env vars:

* HOST: the host for the server (default: 0.0.0.0)
* PORT: the port to listen to (default: 80)
* MONGO_HOST: host of the mongo database (default: localhost)
* MONGO_PORT: port of the mongo database (default: 27017)


# Set up:

Open up the address of the server. It should respond "Hello world"

Go to `http://<host>/init` and fill out the setup form. After this, the server is ready.
