# No as a Service

A lightweight REST API that returns random responses for common situations:

- **No** — reasons to decline a request
- **Hire Me** — reasons to hire someone
- **Date Me** — date suggestions

Built with Flask and designed for simple Docker-based deployment.

## API Endpoints

| Endpoint | Description | Languages |
| --- | --- | --- |
| `GET /api/no/{lang}` | Returns a reason to say no | `fr`, `en`, `es` |
| `GET /api/hireme/{lang}` | Returns a reason to hire someone | `fr`, `en`, `es` |
| `GET /api/dateme/{lang}` | Returns a date suggestion | `fr` |

### Example

```bash
curl http://localhost:5000/api/no/en
```

```json
{
  "reason": "I already have other plans."
}
```

Unsupported languages return an HTTP `404` response:

```json
{
  "error": "Language not supported"
}
```

## Getting Started

### Local Installation

```bash
git clone https://github.com/Malaudos35/no-as-a-service.git
cd no-as-a-service

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
cd code
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

The application will be available at:

```text
http://localhost:5000
```

### Docker

Build and run the application locally:

```bash
docker build -f naas.Dockerfile -t no-as-a-service .
docker run --rm -p 5000:5000 no-as-a-service
```

### Docker Compose

The provided Compose configuration is designed for deployment behind Traefik.

Create the required external network:

```bash
docker network create traefik_networks
```

Configure the domain in `.env`:

```env
URL=example.com
```

Start the service:

```bash
docker compose up --build -d
```

## Adding Content

Responses are stored as JSON arrays under:

```text
code/reason/
code/hireme/
code/dateme/
```

To add a language, create a file using its ISO language code:

```text
code/reason/de.json
```

Example:

```json
[
  "I am not available today.",
  "Maybe another time."
]
```

Restart the application after changing a response file.

## Technology Stack

- Python
- Flask
- Gunicorn
- Docker
- Traefik

## Contributing

Contributions are welcome. Feel free to open an issue or submit a pull request for new responses, languages, tests, or improvements.

## License

No license is currently specified. Add a `LICENSE` file before distributing or reusing this project.
