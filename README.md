### Running locally

- Copy the contents of [`.env.example`](./src/.env.example) into `.env`
- Replace `OPENWEATHER_API_KEY` with your key
- Run `docker compose up weather-app` from project root**

**You may need to change `host.docker.internal` to `localhost` for endpoints if you're using Windows,
e.g.: 
> MINIO_ENDPOINT: http://host.docker.internal:9000 -> http://localhost:9000\
> DYNAMODB_ENDPOINT: http://host.docker.internal:8000 -> http://localhost:8000