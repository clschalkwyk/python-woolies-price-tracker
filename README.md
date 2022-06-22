# python-woolies-price-tracker

Purpose of this little repo is to collect and track food prices from woolies.co.za
The meat section in particular.

So far, we are just pulling prices whenever the script is run.

$ python main.py

Uses requests to load web pages and BeautifulSoup4 to parse HTMl elements.
Outputs raw HTMl and extracted pricing data as JSON.
