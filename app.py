from flask import Flask, render_template, request
import requests
import urllib.parse

app = Flask(__name__)

# Replace with your actual API keys
amazon_api_key = ""
flipkart_api_key = ''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        amazon_results = fetch_amazon_data(query)
        flipkart_results = fetch_flipkart_data(query)
        
        amazon_count = len(amazon_results)
        flipkart_count = len(flipkart_results)
        
        return render_template('results.html', 
                               amazon_results=amazon_results, 
                               flipkart_results=flipkart_results,
                               amazon_count=amazon_count,
                               flipkart_count=flipkart_count)
    return render_template('index.html')

def fetch_amazon_data(query):
    url = "https://real-time-amazon-data.p.rapidapi.com/search"
    querystring = {
        "query": urllib.parse.quote(query),
        "page": "1",
        "country": "US",
        "sort_by": "RELEVANCE",
        "product_condition": "ALL"
    }
    headers = {
        "x-rapidapi-key": amazon_api_key,
        "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    
    if response.status_code == 200:
        data = response.json().get("data", {}).get("products", [])
        
        # Debug print statement to show raw data
        
        
        products = []
        query_lower = query.lower()
        
        for item in data:
            title = item.get('product_title', '').lower()
            
            # Debug print statement to show each title
            
            # Sequential matching for title
            if not all(word in title for word in query_lower.split()):
                continue
            
            price_str = item.get('product_price', '0')
            price = ''.join(filter(str.isdigit, price_str)) if price_str else '0'
            product = {
                'title': item.get('product_title', ''),
                'price': price,
                'mrp': item.get('product_original_price', ''),
                'rating': item.get('product_star_rating', ''),
                'image_url': item.get('product_photo', ''),
                'product_url': item.get('product_url', '')
            }
            products.append(product)
        
        # Debug print statement to show filtered products
       
        return products
    else:
        # Print error response for debugging
        
        return []


def fetch_flipkart_data(query):
    url = "https://real-time-flipkart-api.p.rapidapi.com/product-search"
    querystring = {"q": urllib.parse.quote(query), "page": "1", "sort_by": "popularity"}
    headers = {
        "x-rapidapi-key": flipkart_api_key,
        "x-rapidapi-host": "real-time-flipkart-api.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        formatted_products = []
        query_lower = query.lower()
        
        for product in products:
            title = product.get('title', '').lower()
            brand = product.get('brand', '').lower()
            
            # Debug print statements to understand matching logic
          
            
            # Check if query is completely in title or brand contains query
            if query_lower in title or query_lower in brand:
                
                price_str = str(product.get('price', '0'))
                price = ''.join(filter(str.isdigit, price_str)) if price_str else '0'
                images = product.get('images', [])
                formatted_product = {
                    'title': product.get('title', ''),
                    'brand': product.get('brand', ''),
                    'price': price,
                    'mrp': product.get('mrp', ''),
                    'rating': product.get('rating', {}).get('average', ''),
                    'image_url': images[0] if images else None,
                    'product_url': product.get('url', '')
                }
                formatted_products.append(formatted_product)
        
        # Debug print the results
      
        return formatted_products
    else:
        # Print error response for debugging
       
        return []

if __name__ == '__main__':
    app.run(debug=True)
