### Running locally

- Copy the contents of [`.env.example`](./src/.env.example) into `.env`
- Replace `OPENWEATHER_API_KEY` with your key
- Run `docker compose up weather-app` from project root[^1]

[^1]: You may need to change `host.docker.internal` to `localhost` for endpoints in `docker-compose.yaml` if you're using Windows, e.g. `http://host.docker.internal:9000` -> `http://localhost:9000`
