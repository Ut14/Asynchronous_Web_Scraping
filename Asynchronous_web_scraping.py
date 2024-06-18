import nest_asyncio
import requests
from bs4 import BeautifulSoup
import pandas as pd
from transformers import pipeline
import aiohttp
import asyncio
import pymysql
import json

nest_asyncio.apply()

# Function to extract social media links
def extract_social_media_links(soup):
    social_media_links = []
    social_media_domains = ['facebook.com', 'twitter.com', 'linkedin.com', 'instagram.com', 'youtube.com']
    for link in soup.find_all('a', href=True):
        href = link['href']
        if any(domain in href for domain in social_media_domains):
            social_media_links.append(href)
    return social_media_links

# Function to extract meta title and description
def extract_meta_tags(soup):
    meta_title = soup.title.string if soup.title else 'No title'
    meta_description = ''
    if soup.find('meta', attrs={'name': 'description'}):
        meta_description = soup.find('meta', attrs={'name': 'description'})['content']
    elif soup.find('meta', attrs={'property': 'og:description'}):
        meta_description = soup.find('meta', attrs={'property': 'og:description'})['content']
    return meta_title, meta_description

# Function to detect payment gateways
def detect_payment_gateways(soup):
    payment_gateways = []
    payment_keywords = ['paypal', 'stripe', 'razorpay', 'square', 'payu', 'braintree', 'authorize.net', '2checkout', 'adyen', 'worldpay']
    for script in soup.find_all('script', src=True):
        src = script['src']
        if any(keyword in src.lower() for keyword in payment_keywords):
            payment_gateways.append(src)
    return payment_gateways

# Function to detect tech stack (expanded list)
def detect_tech_stack(soup):
    tech_stack = []
    tech_keywords = {
        'jquery': 'jQuery',
        'angular': 'Angular',
        'react': 'React',
        'vue': 'Vue.js',
        'bootstrap': 'Bootstrap',
        'ember': 'Ember.js',
        'backbone': 'Backbone.js',
        'd3': 'D3.js',
        'three': 'Three.js',
        'handlebars': 'Handlebars.js',
        'knockout': 'Knockout.js',
        'meteor': 'Meteor',
        'polymer': 'Polymer',
        'sass': 'Sass',
        'less': 'Less',
        'gulp': 'Gulp',
        'grunt': 'Grunt',
        'webpack': 'Webpack',
        'babel': 'Babel',
        'typescript': 'TypeScript',
        'coffeescript': 'CoffeeScript',
        'pwa': 'Progressive Web App',
        'wordpress': 'WordPress',
        'drupal': 'Drupal',
        'joomla': 'Joomla',
        'magento': 'Magento',
        'shopify': 'Shopify',
        'squarespace': 'Squarespace',
        'wix': 'Wix',
        'ghost': 'Ghost',
        'jekyll': 'Jekyll',
        'django': 'Django',
        'flask': 'Flask',
        'rails': 'Ruby on Rails',
        'laravel': 'Laravel',
        'spring': 'Spring Framework',
        'express': 'Express.js',
        'next': 'Next.js',
        'nuxt': 'Nuxt.js',
        'svelte': 'Svelte',
        'eleventy': 'Eleventy',
        'gatsby': 'Gatsby'
    }
    for script in soup.find_all('script', src=True):
        src = script['src']
        for keyword in tech_keywords:
            if keyword in src.lower():
                tech_stack.append(tech_keywords[keyword])
    return tech_stack

# Function to extract website language
def extract_website_language(soup):
    if soup.html and 'lang' in soup.html.attrs:
        return soup.html['lang']
    return 'Unknown'

# Function to categorize website
def categorize_website(soup, classifier, categories):
    text = soup.get_text(separator=' ', strip=True)
    if len(text) > 0:
        prediction = classifier(text, candidate_labels=categories, multi_label=False)
        return prediction['labels'][0]
    return 'Unknown'

# Asynchronous function to fetch a website
async def fetch_website(session, website):
    try:
        async with session.get(website) as response:
            return await response.text(), website
    except Exception as e:
        print(f"Error fetching {website}: {e}")
        return None, website

# Main function to process a list of websites
async def process_websites_async(websites, classifier, categories):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_website(session, website) for website in websites]
        results = await asyncio.gather(*tasks)
    
    processed_results = []
    for content, website in results:
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            
            social_media_links = extract_social_media_links(soup)
            meta_title, meta_description = extract_meta_tags(soup)
            payment_gateways = detect_payment_gateways(soup)
            tech_stack = detect_tech_stack(soup)
            website_language = extract_website_language(soup)
            category = categorize_website(soup, classifier, categories)
            
            result = {
                'website': website,
                'social_media_links': social_media_links,
                'meta_title': meta_title,
                'meta_description': meta_description,
                'payment_gateways': payment_gateways,
                'tech_stack': tech_stack,
                'website_language': website_language,
                'category': category
            }
            processed_results.append(result)
    return processed_results

# Function to start the async event loop and process websites
def process_websites(websites):
    # Load pre-trained model for text classification
    classifier = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')

    # Define possible categories
    categories = ['blog', 'news', 'ecommerce', 'portfolio', 'education', 'adult', 'forums', 'social networking and messaging', 'law and government', 'food', 'computer and technology', 'photography', 'health and fitness', 'games', 'sports', 'streaming services']
    
    results = asyncio.run(process_websites_async(websites, classifier, categories))
    
    return results

# Read the list of websites from the CSV file
csv_file = 'websites_list.csv'
df = pd.read_csv(csv_file)
websites = df['website_url'].tolist()

results = process_websites(websites)

# MySQL connection details
host = 'localhost'
user = 'root'
password = '12345'
database = 'webscraping'

# Connect to MySQL
connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             db=database,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Create table if not exists
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS websites (
            id INT AUTO_INCREMENT PRIMARY KEY,
            website VARCHAR(255) NOT NULL,
            social_media_links JSON,
            meta_title VARCHAR(500),
            meta_description LONGTEXT,
            payment_gateways JSON,
            tech_stack JSON,
            website_language VARCHAR(50),
            category VARCHAR(50)
        )
        """
        cursor.execute(create_table_sql)

        # Insert data into the table
        insert_sql = """
        INSERT INTO websites (website, social_media_links, meta_title, meta_description, payment_gateways, tech_stack, website_language, category)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        for result in results:
            cursor.execute(insert_sql, (
                result['website'],
                json.dumps(result['social_media_links']),
                result['meta_title'],
                result['meta_description'],
                json.dumps(result['payment_gateways']),
                json.dumps(result['tech_stack']),
                result['website_language'],
                result['category']
            ))

    # Commit changes
    connection.commit()
    print("Data successfully inserted into MySQL table")

except Exception as e:
    print(f"Error: {e}")

finally:
    connection.close()
