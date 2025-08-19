from django.shortcuts import render
from .forms import MyForm
from .models import PhishingURL
import requests
from bs4 import BeautifulSoup
import re
import math
import numpy as np
import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
import re
import math
import numpy as np
import joblib
from keras.models import load_model
import decimal
from django.http import HttpResponse

# Load the machine learning model
model = load_model('Models/model.h5')

# Load the scaler
scaler = joblib.load('Models/scaler.h5')

# Create your views here.
def features3(request):
    return render(request,'features3.html')

def perform_prediction(url):
    # Get the input URL from the request object
    # url = request.GET.get('url', '')

    # Fetch the HTML content of the website
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()

    # Calculate various features of the website
    url_length = len(url)
    body_length = len(text)
    num_digits = sum([1 for char in text if char.isdigit()])
    special_chars = sum([1 for char in text if not char.isalnum() and not char.isspace()])
    num_images = len(soup.find_all('img'))
    num_links = len(soup.find_all('a'))
    num_params = len(re.findall(r'\?.*=', url))
    num_percent20 = url.count('%20')
    num_at = url.count('@')
    has_http = 1 if 'http://' in url else 0
    has_https = 1 if 'https://' in url else 0
    has_ip = 1 if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url) else 0
    script_length = sum([len(script.get_text()) for script in soup.find_all('script')])
    sscr = script_length / body_length if body_length > 0 else 0
    bscr = body_length / url_length if url_length > 0 else 0
    entropy = sum([-1 * (text.count(char) / body_length) * (math.log(text.count(char) / body_length)) for char in set(text)]) if body_length > 0 else 0
    num_titles = len(soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']))
    dse = (num_images + num_links) / num_titles if num_titles > 0 else 0
    dsr = num_links / body_length if body_length > 0 else 0
    sbr = num_images / num_links if num_links > 0 else 0

    # Check if the URL is live
    try:
        requests.head(url, timeout=5)
        url_is_live = 1
    except requests.exceptions.ConnectionError:
        url_is_live = 0

    # Scale the features and predict the label using the machine learning model
    features = np.array([body_length, bscr, dse, dsr, entropy, has_http, has_https, has_ip, num_digits, num_images, num_links, num_params, num_titles, num_percent20, num_at, sbr, script_length, special_chars, sscr, url_is_live, url_length])
    features = scaler.transform(features.reshape(1, -1))
    # Get the predicted probabilities for each class
    probs = model.predict(features)

    # Calculate the predicted class based on the highest probability
    predicted_class = np.argmax(probs)

    # Use the predicted class to determine whether the URL is safe or unsafe
    if predicted_class == 0:
        # The URL is unsafe
        unsafe_percentage =  100
        safe_percentage = 100 - unsafe_percentage
        
    else:
        # The URL is safe
        unsafe_percentage = probs[0][predicted_class] 
        safe_percentage = 100 - unsafe_percentage
        
    # Format the predicted probabilities as percentages with higher precision
    decimal.getcontext().prec = 100
    formatted_safe = "{:.2%}".format(decimal.Decimal(str(safe_percentage/100)))
    formatted_unsafe = "{:.2%}".format(decimal.Decimal(str(unsafe_percentage/100)))

    # Pass the predicted probabilities and their formatted percentages to the template
    context = {
        'predicted_safe': safe_percentage,
        'predicted_unsafe': unsafe_percentage,
        'formatted_safe': formatted_safe,
        'formatted_unsafe': formatted_unsafe,
        'link': url
    }

    return context



def my_view3(request):
    try:
        if request.method == 'POST':
            form = MyForm(request.POST)
            if form.is_valid():
                # Get the URL entered by the user
                url = form.cleaned_data['url']
                # Perform prediction using the URL
                prediction = perform_prediction(url)
                # Render the template with the prediction
                context =  prediction 
                phishing_url = PhishingURL(url=url)
                phishing_url.save()
                return render(request, 'result.html', context=context)
            else:
                # Form data is invalid, render an error message
                return render(request, 'result.html', {'prediction': 'Invalid form data.'})
        else:
            # Return a default response for GET requests
            return HttpResponse("This is my_view3.")
    except Exception as e:
        # Return an error message as an HttpResponse object
        return HttpResponse("An error occurred: " + str(e))