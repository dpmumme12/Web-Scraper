## Web Scraper

### ==Description==</h3>
This is a movie searcher that uses Imdb and Rotten Tomato data to search for and display movies with their ratings and description. It utilizes python's BeautifulSoup moduel to scrape the websites for data and python's robotparser module to make sure it ahere's to each stite's robot.txt file. You can see a link to the demo at the bottom of this page, enjoy!

### ==Files and directories==
- `ratings` - Main application directory.
  - `static/ratings` - Contains all static files.
    - `styles.css` - Contains all the css for the app.
  - `template/ratings` - Contains all html files for the app.
    - `layout.html` - The base template that all other templates extend.
    - `index.html` - Main template or "homepage".
    - `search.html` - The search results page that displays a list of movies with their ratings and descriptions from the query.
  - `urls.py` - Contains all the urls for the app.
  - `views.py` - Contains all the views for the app.
- `scraper` - Project directory.

Demo link https://movie-ratings-scraper.herokuapp.com/