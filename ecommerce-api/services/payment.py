import stripe
import os

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_placeholder')


def create_checkout_session(order_id, total, success_url, cancel_url):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f'Order #{order_id}',
                    },
                    'unit_amount': int(total * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return session
    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


def handle_webhook(payload, sig_header, webhook_secret):
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        return event
    except ValueError:
        return None
    except stripe.error.SignatureVerificationError:
        return None
