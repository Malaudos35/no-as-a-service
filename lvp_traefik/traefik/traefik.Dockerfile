FROM traefik

RUN mkdir -p ./letsencrypt
RUN touch ./letsencrypt/acme.json
RUN chmod 600 ./letsencrypt/acme.json


