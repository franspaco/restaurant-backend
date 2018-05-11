
app_dir="app"

if [ ! -d "$app_dir" ]; then
        git clone https://github.com/franspaco/restaurant-backend.git "$app_dir"
        cd "$app_dir"
else
        cd "$app_dir"
        git pull origin master
fi


#defaults
export MONGO_HOST=${MONGO_HOST:-"localhost"}
export MONGO_PORT=${MONGO_PORT:-"27017"}
