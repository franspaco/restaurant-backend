
# Basic docker config


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