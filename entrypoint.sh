
if [ ! -d "restaurant-backend"]; then
    git clone https://github.com/franspaco/restaurant-backend.git
fi

cd restaurant-backend
flask run --port 80 --host $HOST