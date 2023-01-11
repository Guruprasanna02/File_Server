#Since mysql container takes time to start completely, we need to wait for few seconds

until nc -z -v -w30 db 3306
do
  echo "Waiting for database connection..."
  # wait for 5 seconds before check again
  sleep 5
done

python setupdb.py

python server.py
