import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

load_dotenv()

def analyze_review_sentiments(dealerreview):
    url=os.environ['WATSON_URL']
    text=dealerreview
    api_key=os.environ['WATSON_API_KEY']
    features={"sentiment":{}}
    version='2020-08-01'
    return_analyzed_text=True

    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
    version=version,
    authenticator=authenticator
    )
    natural_language_understanding.set_service_url(url)
    return natural_language_understanding.analyze(text=text,return_analyzed_text=return_analyzed_text, features=features).get_result()


def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except Exception as e:
        print(e)
        return 
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def post_request(url,json_payload, **kwargs):
    print(kwargs)
    print("POST from {} ".format(url))
    try:
        response = requests.post(url,params=kwargs,json=json_payload)
        print(response.text, "hello")
        return json.loads(response.text)
    except Exception as e:
        print(e)
        return

def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result["rows"]

        for dealer in dealers:
            dealer_doc = dealer["doc"]
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, dealerId=kwargs['dealer_id'])
    if json_result:
        reviews = json_result["docs"]
        for review in reviews:
            review_obj = DealerReview(
                dealership=review['dealership'],
                name=review['name'],
                purchase=review['purchase'],
                review=review['review'],
                purchase_date=review['purchase_date'],
                car_make=review['car_make'],
                car_model=review['car_model'],
                car_year=review['car_year'],
                sentiment=analyze_review_sentiments(review['review']),
                id=review['_id'],
            )
            results.append(review_obj)
    return results


