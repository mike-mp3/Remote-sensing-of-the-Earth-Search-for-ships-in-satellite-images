FROM redis:7.4.2

ARG REDIS_PASSWORD

RUN mkdir -p /usr/src/redis
WORKDIR /usr/src/redis

RUN echo "bind 0.0.0.0" > ./redis.conf && \
    echo "requirepass $REDIS_PASSWORD" >> ./redis.conf && \
    echo "appendonly yes" >> ./redis.conf && \
    echo "appendfsync everysec" >> ./redis.conf

CMD ["redis-server", "./redis.conf"]
