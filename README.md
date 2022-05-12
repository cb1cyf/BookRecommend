# BookRecommend
Project of Big Data Course
## Start Service
```bash
chmod a+x ./bin/start
bash ./bin/start
```
Access address: http://localhost:8888/book-rec/

The full SQL file `book.sql` can be found in the release. Please download it and copy it to `./SQL/book.sql` before starting service.
## Stop Service
```bash
docker-compose stop -f ./bin/docker-compose.yml
```
