from flask import Flask, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for sessions

# Sample products
PRODUCTS = [
    {'id': 1, 'name': 'Product 1', 'price': 10.99},
    {'id': 2, 'name': 'Product 2', 'price': 15.49},
    {'id': 3, 'name': 'Product 3', 'price': 7.99},
    {'id': 4, 'name': 'Product 4', 'price': 20.00},
]

@app.route('/')
def home():
    # Ensure the cart exists in the session
    if 'cart' not in session:
        session['cart'] = []
    return render_template('home.html', products=PRODUCTS, cart=session['cart'])

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    # Find the product by ID
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product:
        # Add product to the cart stored in session
        session['cart'].append(product)
        session.modified = True  # Mark the session as modified to save changes
    return redirect(url_for('home'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    # Remove the first occurrence of the product with the given ID
    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == product_id:
            cart.remove(item)
            break
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('home'))

@app.route('/clear_cart')
def clear_cart():
    # Clear the cart
    session['cart'] = []
    session.modified = True
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
