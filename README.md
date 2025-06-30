# Hermes

A

1. Build docker compose

```bash
docker compose build
```

2. Run docker compose

```bash
docker compose up -d
```

3. Run migrations

```bash
docker compose exec backend edgy migrate
```

4. Create .env file with:

```
OPENAI_API_KEY=your_openai_api_key
```

5. Add products into API
   1. Go to API docs:
      - API: http://localhost:8000/docs
   2. Use the `/products/` endpoint to add product or `/products/bulk` to add many products.
   3. Click `/products/embedding` to generate embeddings for the products.


Additional Links:

API: http://localhost:8000/docs

APP: http://localhost:3000/
