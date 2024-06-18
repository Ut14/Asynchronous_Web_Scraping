
# Asynchronous Web Scraping Project

This project scrapes websites for metadata, social media links, payment gateways, tech stack, and more. It categorizes the website content using a pre-trained model and saves the results in a CSV file named `Result.csv`.

## Project Structure

- `Asynchronous_web_scraping.py`: The main Python script that performs the web scraping and data processing.
- `website_list.csv`: A CSV file containing the list of websites to be scraped.
- `Result.csv`: The output CSV file where the scraped data and analysis results are saved.
- `requirements.txt`: A file listing all the Python dependencies needed for the project.


## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/Ut14/web_scraping_project.git
2. Navigate to the project directory:
   ```sh
   cd web_scraping_project
3. Install the required Python packages:
   ```sh
    pip install -r requirements.txty-project
    ```
    
## Usage/Examples

1. Ensure you have the `website_list.csv` file in the project   directory. This file should contain the list of websites you want to scrape.

2. Run the script:
    ```sh
    python Asynchronous_web_scraping.py
    ```
3. After the script completes, the results will be saved in `Result.csv`.


## Features

### Main Functions
- extract_social_media_links(soup): Extracts social media links - from the website content.
- extract_meta_tags(soup): Extracts meta title and description from the website content.
- detect_payment_gateways(soup): Detects payment gateways used on the website.
- detect_tech_stack(soup): Identifies the tech stack used on the website.
- extract_website_language(soup): Determines the language of the website.
- categorize_website(soup, classifier, categories): Categorizes the website content using a pre-trained text classification model.
- fetch_website(session, website): Asynchronously fetches the website content.
- process_websites_async(websites, classifier, categories
- Processes the list of websites asynchronously and extracts relevant data.
- process_websites(websites): Starts the async event loop and processes the websites.

### Model and Categories
The script uses the facebook/bart-large-mnli model from the transformers library for text classification.
The possible categories for website content include:
- Blog
- News
- Ecommerce
- Portfolio
- Education
- Adult
- Forums
- Social networking and messaging
- Law and government
- Food
- Computer and technology
- Photography
- Health and fitness
- Games
- Sports
- Streaming services


## Example Directory Structure

```rust
web_scraping_project/
├── Asynchronous_web_scraping.py
├── requirements.txt
├── website_list.csv
└── Result.csv
```


## License

This project is licensed under the MIT License.

```less

Make sure to replace `https://github.com/Ut14/web_scraping_project.git` with the actual URL of your GitHub repository. This `README.md` provides a clear overview of the project, its requirements, how to install and run it, and what each main function does.
```

