# OpenAPI Traffic Validator

CLI Tool that validates an OpenAPI specification against a live application using [Newman](https://github.com/postmanlabs/newman). Optionally generates the OpenAPI spec from code using [NightVision](https://www.nightvision.net/).

## Cheatsheet

```bash
api-validator yolo \
    --config-file config.yml \
    --swagger-file juice-shop.yml \
    --server http://localhost:3000 \
    --app-name juice-shop
```

It will generate a file called [./summary.md](./summary.md) in the current directory.

You can split it up into smaller parts too:

```bash
# Install prerequisites
api-validator install

# Extract an API with NightVision
api-validator generate \
  --server https://api.example.com \
  --output openapi-spec.yml

# Convert from OpenAPI to Postman collection
api-validator convert \
  --server http://localhost:3000 \
  --swagger-file examples/nv-juice-shop.yml \
  --postman-file examples/collection.json

# Skip postman request
api-validator exclude postman-request \
  --postman-file examples/collection.json \
  --config-file examples/config.yml \
  --app-name juice-shop

# Run newman
api-validator validate \
  --postman-file examples/collection.json \
  --output-dir examples/newman-data \
  --app-name juice-shop

# Generate a markdown report
api-validator report \
  --data-dir examples/newman-data \
  --output-file examples/juice-shop-summary.md \
  --config-file examples/config.yml
```
