from django.shortcuts import render, reverse
import requests
from bs4 import BeautifulSoup
import re
import math
import numpy as np
import joblib
from .forms import MyForm
from keras.models import load_model
from .forms import WebsiteForm
# Load the machine learning model
model = load_model('Models/model.h5')

# Load the scaler
scaler = joblib.load('Models/scaler.h5')
# Create your views here.
def features1(request):
    return render(request,'features1.html')


def store(request):
    if request.method == 'POST':
        form = WebsiteForm(request.POST)
        if form.is_valid():
            form.save()
            return reverse('success_page')
    else:
        form = WebsiteForm()
    return render(request, 'my_template.html', {'form': form})
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
    prediction = model.predict(features)
    prediction = prediction


    # Map the predicted label to a human-readable string
    if np.array_equal(prediction, np.array([[1., 0., 0., 0., 0.]])):
        label = "Benign"
    elif np.array_equal(prediction, np.array([[0., 0., 1., 0., 0.]])):
        label = "Malware"
    elif np.array_equal(prediction, np.array([[0., 0., 0., 1., 0.]])):
        label = "Phishing"
    elif np.array_equal(prediction, np.array([[0., 0., 0., 0., 1.]])):
        label = "Spam"
    elif np.array_equal(prediction, np.array([[0., 1., 0., 0., 0.]])):
        label = "Defacement"
    else:
        label = "Unknown"

    prediction_dict = {
        0: "Benign",
        1: "Defacement",
        2: "Malware",
        3: "Phishing",
        4: "Spam"
    }

    prediction = prediction_dict[np.argmax(prediction)]

    return prediction

def my_view1(request):
    try:
        if request.method == 'POST':
            form = WebsiteForm(request.POST)
            if form.is_valid():
                # Get the URL entered by the user
                url = form.cleaned_data['url']
                website = form.save(commit=False)
                website.save()
                # Perform prediction using the URL
                prediction = perform_prediction(url)
                # Render the template with the prediction
                context = {'label': prediction}
                return render(request, 'prediction.html', context=context)
            else:
                # Form data is invalid, render an error message
                return render(request, 'prediction.html', {'label': 'Invalid form data.'})
        
    except Exception as e:
        return render(request, 'prediction.html', context={'label':str(e)})
