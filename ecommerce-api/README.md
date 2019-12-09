# E-Commerce API

Flask REST API for e-commerce with product catalog, shopping cart, and Stripe payments.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Add STRIPE_API_KEY to .env
python app.py
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /products | List all products |
| POST | /products | Create product |
| GET | /products/`<id>` | Get product |
| POST | /cart | Add item to cart |
| GET | /cart | View cart |
| DELETE | /cart/`<id>` | Remove cart item |
| POST | /orders | Create order from cart |
| POST | /checkout | Process Stripe payment |

## Examples

```bash
# List products
curl http://localhost:5008/products

# Add to cart
curl -X POST http://localhost:5008/cart \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'

# View cart
curl http://localhost:5008/cart
# {"items": [{"product": "Flask Book", "quantity": 2, "price": 29.99}], "total": 59.98}

# Create order
curl -X POST http://localhost:5008/orders \
  -H "Content-Type: application/json" \
  -d '{}'

# Checkout with Stripe
curl -X POST http://localhost:5008/checkout \
  -H "Content-Type: application/json" \
  -d '{"order_id": 1, "token": "tok_visa"}'
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| STRIPE_API_KEY | Stripe secret key |
| SECRET_KEY | Flask secret key |
