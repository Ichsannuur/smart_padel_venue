# Simple Web Scraper

A simple Python web scraper using requests and BeautifulSoup for extracting data from websites.

## Features

-   🔍 **Text Content Scraping**: Extract text from HTML elements using CSS selectors
-   🔗 **Link Extraction**: Get all links from a webpage with their URLs and text
-   📊 **Table Scraping**: Extract HTML tables into pandas DataFrames
-   🖼️ **Image Scraping**: Get image URLs and alt text
-   ⚙️ **Custom Selectors**: Use custom CSS selectors for specific scraping needs
-   💾 **Data Export**: Save data to JSON and CSV formats
-   🤖 **Respectful Scraping**: Built-in delays and proper headers

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from scraper import SimpleScraper

# Create scraper instance
scraper = SimpleScraper()

# Scrape text content
quotes = scraper.scrape_text_content("https://quotes.toscrape.com/", ".quote .text")
print(quotes)

# Scrape links
links = scraper.scrape_links("https://quotes.toscrape.com/")
print(links)
```

### Running Examples

Run the provided examples to see the scraper in action:

```bash
python examples.py
```

## Usage Examples

### 1. Simple Text Scraping

```python
from scraper import SimpleScraper

scraper = SimpleScraper()
url = "https://quotes.toscrape.com/"

# Get all quotes
quotes = scraper.scrape_text_content(url, '.quote .text')
authors = scraper.scrape_text_content(url, '.quote .author')

for quote, author in zip(quotes, authors):
    print(f'"{quote}" - {author}')
```

### 2. Custom Multi-Element Scraping

```python
scraper = SimpleScraper()
url = "https://quotes.toscrape.com/"

selectors = {
    'quotes': '.quote .text',
    'authors': '.quote .author',
    'tags': '.tag'
}

data = scraper.scrape_custom(url, selectors)
scraper.save_to_json(data, 'scraped_data.json')
```

### 3. Table Scraping

```python
scraper = SimpleScraper()
url = "https://example.com/data-table"

# Scrape table into pandas DataFrame
df = scraper.scrape_table(url, 'table.data-table')
scraper.save_to_csv(df, 'table_data.csv')
```

## API Reference

### SimpleScraper Class

#### Methods

-   `get_page(url)`: Fetch and parse a webpage
-   `scrape_text_content(url, selector)`: Extract text from elements
-   `scrape_links(url, selector='a')`: Extract links
-   `scrape_table(url, table_selector='table')`: Extract tables as DataFrame
-   `scrape_images(url, img_selector='img')`: Extract image information
-   `scrape_custom(url, selectors)`: Use custom selectors
-   `save_to_json(data, filename)`: Save data to JSON
-   `save_to_csv(data, filename)`: Save DataFrame to CSV

#### Parameters

-   `delay`: Delay between requests (default: 1.0 seconds)

## Best Practices

1. **Be Respectful**: Always check `robots.txt` and respect rate limits
2. **Use Delays**: Don't overwhelm servers with rapid requests
3. **Handle Errors**: Websites can change or be unavailable
4. **User Agent**: Use appropriate user agent strings
5. **Legal Compliance**: Ensure you have permission to scrape

## Common CSS Selectors

```css
.class-name        /* Elements with specific class */
/* Elements with specific class */
#id-name          /* Element with specific ID */
tag-name          /* All elements of a tag type */
[attribute]       /* Elements with an attribute */
parent > child    /* Direct child elements */
ancestor descendant; /* Descendant elements */
```

## Troubleshooting

### Common Issues

1. **Empty Results**: Check if CSS selectors are correct
2. **Request Blocked**: Website might be blocking automated requests
3. **Slow Performance**: Increase delay between requests
4. **Memory Issues**: Process data in chunks for large datasets

### Debugging Tips

```python
# Debug: Print page structure
soup = scraper.get_page(url)
print(soup.prettify()[:1000])  # First 1000 chars

# Debug: Test selectors
elements = soup.select('your-selector')
print(f"Found {len(elements)} elements")
```

## Legal and Ethical Considerations

-   Always respect `robots.txt`
-   Don't overload servers with requests
-   Check website terms of service
-   Consider reaching out for API access instead
-   Be mindful of copyright and data privacy laws

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.
