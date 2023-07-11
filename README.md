# Docker Practice


## nginx container
### run docker container
```bash
docker run --rm -p 80:80 --name goodkub -d nginx
```

### edit file inside docker
index file at `/usr/share/nginx/html`
```bash
docker exec -it goodkub bash
```

## Make dev environment
```bash
docker run --rm --name devkub -v ${pwd}:/app -t -d -w app python:3.9 bash
```