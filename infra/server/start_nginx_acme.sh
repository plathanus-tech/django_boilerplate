#!/bin/sh
set -e

echo "Creating the shared network..."
docker network create shared

echo "Starting nginx-proxy..."
docker run --detach \
  --name nginx-proxy \
  --publish 80:80 \
  --publish 443:443 \
  --volume certs:/etc/nginx/certs \
  --volume vhost:/etc/nginx/vhost.d \
  --volume html:/usr/share/nginx/html \
  --volume /var/run/docker.sock:/tmp/docker.sock:ro \
  --volume ./infra/nginx/conf.d/custom_proxy.conf:/etc/nginx/conf.d/custom_proxy.conf \
  --volume ./infra/nginx/conf.d/fallback_server.conf:/etc/nginx/conf.d/fallback_server.conf \
  --volume staticfiles:/usr/share/nginx/static \
  --network shared \
  nginxproxy/nginx-proxy

echo "Starting nginx-proxy-acme..."
docker run --detach \
  --name nginx-proxy-acme \
  --volumes-from nginx-proxy \
  --volume /var/run/docker.sock:/var/run/docker.sock:ro \
  --volume acme:/etc/acme.sh \
  --env "DEFAULT_EMAIL=leandrodesouzadev@gmail.com" \
  --network shared \
  nginxproxy/acme-companion
