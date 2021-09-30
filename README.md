# Bookspot

A Book Store

## Development

The only dependencies for this project should be docker and docker-compose.

### Quick Start

Starting the project with hot-reloading enabled
(the first time it will take a while):

```bash
docker-compose up -d
```

And navigate to http://localhost/

### Rebuilding containers:

```
docker-compose build
```

### Bringing containers down:

```
docker-compose down
```

## Testing

To run tests,
```bash
docker-compose run --rm api sh -c "python -m pytest"
```
