# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape data from a website
def scrape_data(url):
    # Send a GET request to the URL
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return []

    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Print the parsed HTML for debugging purposes (optional)
    # print(soup.prettify())

    # Find relevant data; adjust the selector based on the website structure
    # Here we will look for all headings (h2) and their corresponding links
    sections = soup.find_all('h2')  # Look for h2 tags

    # Extract data from each section
    data = []
    for section in sections:
        title = section.text.strip() if section else 'No Title'  # Get the title
        # Try to find a link associated with the title, this might vary based on the site
        link = section.find('a')['href'] if section.find('a') else 'No Link'  # Modify based on the website's HTML structure
        
        # Append the data to the list
        data.append({'Title': title, 'Link': link})

    return data

# Function to save scraped data to a CSV file
def save_to_csv(data, filename):
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data)
    
    # Save the DataFrame to a CSV file
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Main function to execute the scraping process
def main():
    # Specify the URL of the website to scrape
    url = 'https://aws.amazon.com/what-is/data-science/'  # Replace with the actual URL you want to scrape
    
    # Call the scrape_data function
    scraped_data = scrape_data(url)
    
    # Check if data was scraped successfully
    if scraped_data:
        # Specify the filename to save the data
        filename = 'scraped_data.csv'
        
        # Call the save_to_csv function
        save_to_csv(scraped_data, filename)
    else:
        print("No data found.")

# Entry point of the program
if __name__ == '__main__':
    main()
