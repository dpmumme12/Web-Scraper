from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from urllib import parse
from urllib import robotparser



def index(request):
    # Checks with the websites robots.txt to make sure the info being scraped is allowed
    rp = robotparser.RobotFileParser()
    rp.set_url("https://www.imdb.com/robots.txt")
    rp.read()
    if rp.can_fetch("*", "https://www.imdb.com/chart/top/?ref_=nv_mv_250"):
        url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"

        uClient = urlopen(url)
        page_html = uClient.read()
        uClient.close()

        page_soup = soup(page_html, "html.parser")

        containers = page_soup.findAll("tr")

        imdb_topTen = []

        # Goes through the parsed html and creates an accessible dictionary to use
        for i in range(1,11):
            info = {
                "image": containers[i].find("img")['src'],
                "title": containers[i].a.find_next("a").text,
                "rating": containers[i].strong.text,
                "year": containers[i].find("td",{"class":"titleColumn"}).span.text
            }

            imdb_topTen.append(info)

    # Checks with the websites robots.txt to make sure the info being scraped is allowed
    rp = robotparser.RobotFileParser()
    rp.set_url("https://www.rottentomatoes.com/robots.txt")
    rp.read()
    if rp.can_fetch("*", "https://www.rottentomatoes.com/top/bestofrt/"):
        url = "https://www.rottentomatoes.com/top/bestofrt/"

        uClient = urlopen(url)
        page_html = uClient.read()
        uClient.close()

        page_soup = soup(page_html, "html.parser")

        table = page_soup.find("table",{"class":"table"})
        containers = table.findAll("tr")

        tomato_topTen = []
        
        # Goes through the parsed html and creates an accessible dictionary to use
        for i in range(1,11):
            info = {
                "title": containers[i].a.text.strip(),
                "rating": containers[1].find("span",{"class":"tMeterScore"}).text.strip('\xa0'),
            }

            tomato_topTen.append(info)
    
    return render(request, "pricechecker/index.html",{
        "imdb_topTen": imdb_topTen,
        "tomato_topTen": tomato_topTen
    })

def search(request):
    if (request.method == "POST"):
        #gets the users movie search query
        query = request.POST.get("query")
        #parses imdb to get results for the query
        base_url = "https://www.imdb.com/search/title/?"
        my_url = base_url + parse.urlencode({"title": query})

        rp = robotparser.RobotFileParser()
        rp.set_url("https://www.imdb.com/robots.txt")
        rp.read()
        #Checks robots.txt file to see if they allow the page to be scraped
        if rp.can_fetch("*", my_url):
            uClient = urlopen(my_url)
            page_html = uClient.read()
            uClient.close()

            page_soup = soup(page_html, "html.parser")

            containers = page_soup.findAll("div", {"class": "lister-item mode-advanced"})

            results = []


            for i in range(10):
                image = containers[i].img
                image = soup(str(image), "html.parser")
                try:
                    info = {
                        'movie_id': i,
                        'movie_img': image.find("img")['loadlate'],
                        'title': containers[i].a.find_next("a").text,
                        'year': containers[i].span.find_next("span").text,
                        'imdbRating':  containers[i].strong.text,
                        'summary': containers[i].find("p",{"class":"text-muted"}).find_next("p",{"class":"text-muted"}).text.strip()
                    }
                except:
                    info = {
                        'movie_id': i,
                        'movie_img': image.find("img")['loadlate'],
                        'title': containers[i].a.find_next("a").text,
                        'year': containers[i].span.find_next("span").text,
                        'imdbRating':  "no rating",
                        'summary': containers[i].find("p",{"class":"text-muted"}).find_next("p",{"class":"text-muted"}).text.strip()
                    }

         
                try:
                    info["metascore"] = containers[i].find("div",{"class":"inline-block ratings-metascore"}).span.text.strip()
                except:
                    info["metascore"] = "no score"


                rp = robotparser.RobotFileParser()
                rp.set_url("https://www.yahoo.com/robots.txt")
                rp.read()

                title = containers[i].a.find_next("a").text
                base_url = "https://search.yahoo.com/search?"
                my_url = base_url + parse.urlencode({"p": title})

                if rp.can_fetch("*", my_url):
    
                    uClient = urlopen(my_url)
                    page_html = uClient.read()
                    uClient.close()

                    page_soup = soup(page_html, "html.parser")

                    try:
                        info["tomato_score"] = page_soup.find("span",{"class":"rottenTomatoes"}).text
                    except:
                        info["tomato_score"] = "no score"

                results.append(info)

            return render(request, "pricechecker/search.html", {
                "movies": results
            })