import requests
from bs4 import BeautifulSoup
import json


def save_json(movie_list):
    with open('Movies.json', 'w') as movies_file:
        json.dump(movie_list, movies_file)


def scrape_movies(old_list=False):
    r = requests.get(
        'https://en.wikipedia.org/wiki/List_of_Disney_theatrical_animated_feature_films')
    soup = BeautifulSoup(r.content, 'html.parser')

    s = soup.find('div', id='mw-content-text')

    tables = s.find('table', {"class": 'wikitable'})
    items = tables.findAll('tr')

    categories = []
    indicators = []
    for item in items:
        data = item.find_all(['th', 'td'])
        try:
            category = data[0].text
            category = category.split(" (")[0]
            category = category.split("\n")[0]
            category = category.split(",")[0]
            try:
                indicator = data[1].get("style")[11:-1]
            except:
                indicator = data[1].text.split("\n")[0]
            categories.append(category)
            indicators.append(indicator)
        except:
            pass

    for i in range(len(categories)):
        print(f"{categories[i]}: {indicators[i]}")

    tables = s.find('table', {"class": 'wikitable sortable plainrowheaders'})

    items = tables.findAll('tr')

    movies = []
    for c in categories:
        movies.append([])

    for item in items:

        data = item.find_all(['th', 'td'])
        try:
            link = "https://en.wikipedia.org" + data[0].a.get("href")
            title = data[0].a.get("title")
            title = title.split(" (")[0]
            title = title.split("\n")[0]
            date = data[1].text
            date = date.split("\n")[0]
            date = date.split("[")[0]
            date = date.split(" (")[0]

            try:
                indicator = data[3].get("style")[11:-1]
            except:
                try:
                    indicator = data[1].text.split("\n")[3]
                except:
                    indicator = old_indicator
            old_indicator = indicator

            for i in range(len(indicators)):
                if indicator == indicators[i]:
                    movies[i].append([title, date, link])
        except:
            pass

    movie_dict_list = []

    if old_list:
        for i in range(len(movies)):
            for movie in movies[i]:
                watched_flag = False
                if old_list:
                    for old_movie in old_list:
                        if old_movie["Title"] == movie[0] and old_movie["Date"] == movie[1]:
                            watched_flag = old_movie["Watched"]
                            break
                movie_dict = {'Title': movie[0], 'Date': movie[1], 'Link': movie[2],
                              'Category': categories[i], 'Watched': watched_flag}
                movie_dict_list.append(movie_dict)
    else:
        for i in range(len(movies)):
            for movie in movies[i]:
                movie_dict = {'Title': movie[0], 'Date': movie[1],
                              'Link': movie[2], 'Category': categories[i], 'Watched': False}
                movie_dict_list.append(movie_dict)
    return movie_dict_list


def check_if_watched(movie_list, check_all=False):
    if check_all:
        for movie in movie_list:
            print(f"\nHave you watched {movie['Title']} ({movie['Date']}?")
            while True:
                watched_flag = input("(Yes/No/Cancel): ")
                watched_flag = watched_flag.lower()
                if watched_flag == "y":
                    movie['Watched'] = True
                    break
                elif watched_flag == "n":
                    movie['Watched'] = False
                    break
                elif watched_flag == "c":
                    save_json(movie_list)
                    return
    else:
        for movie in movie_list:
            if movie['Watched'] is False:
                print(
                    f"\nHave you watched {movie['Title']} ({movie['Date']})?")
                while True:
                    watched_flag = input("(Yes/No/Cancel): ")
                    watched_flag = watched_flag.lower()
                    if watched_flag == "y":
                        movie['Watched'] = True
                        break
                    elif watched_flag == "n":
                        break
                    elif watched_flag == "c":
                        save_json(movie_list)
                        return
    save_json(movie_list)


def make_README(movie_list):
    new_readme = open('README.md', 'w')
    new_readme.write("This is a checklist of Disney movies me and my wife has watched while eating waffles for Sunday breakfast.\n")
    new_readme.write("The movies are updated by scraping [the wikipedia list of Disney theatrical releases](https://en.wikipedia.org/wiki/List_of_Disney_theatrical_animated_feature_films), retaining the 'watched' status that is updated by hand.\n\n")
    category = None
    for movie in movie_list:
        if not movie['Category'] == category:
            category = movie['Category']
            new_readme.write(f"\n# {category}\n")
        title = movie['Title']
        date = movie['Date']
        link = movie['Link']
        if movie['Watched']:
            new_readme.write("- [x] ")
        else:
            new_readme.write("- [ ] ")
        new_readme.write(f"[{title}]({link})\t({date})\n")
    new_readme.close()


def update_from_web(old_movie_list):
    new_movie_list = scrape_movies(old_movie_list)
    save_json(new_movie_list)
    old_movie_list = new_movie_list


def get_movie_list():
    try:
        with open('Movies.json', 'r', encoding='UTF-8') as movie_file:
            return json.load(movie_file)
    except Exception:
        Movies = scrape_movies()
        save_json(Movies)
        return Movies


def movies_from_README():
    old_readme = open('README.md', 'r')
    category = None
    movie_dict_list = []
    for line in old_readme:
        if len(line.split("# ")) > 1:
            category = line.split("# ")[1]
        else:
            line = line.replace("](", "*")
            line = line.replace(")\t(", "*")
            line = line.replace(")\n", "*")
            if len(line.split("[ ]")) > 1:
                data = line[7:-1].split("*")
                movie_dict_list.append(
                    {'Title': data[0], 'Date': data[2], 'Link': data[1], 'Category': category, 'Watched': False})
            elif len(line.split("[x]")) > 1:
                data = line[7:-1].split("*")
                movie_dict_list.append(
                    {'Title': data[0], 'Date': data[2], 'Link': data[1], 'Category': category, 'Watched': True})
    old_readme.close()
    save_json(movie_dict_list)
    return movie_dict_list


if __name__ == "__main__":
    Movies = get_movie_list()
    print("\nGet movies from README.md?")
    while True:
        flag = input("(Yes/No/Cancel): ")
        flag = flag.lower()
        if flag == "y":
            Movies = movies_from_README()
            save_json(Movies)
            break
        elif flag == "n":
            break
    print("\nUpdate movies from wikipedia?")
    while True:
        flag = input("(Yes/No/Cancel): ")
        flag = flag.lower()
        if flag == "y":
            update_from_web(Movies)
            save_json(Movies)
            break
        elif flag == "n":
            break
    print("\nCheck watched status?")
    while True:
        flag = input("(Yes/No): ")
        flag = flag.lower()
        if flag == "y":
            print("\nAll of False?")
            while True:
                flag = input("(All/False/Cancel): ")
                flag = flag.lower()
                if flag == "a":
                    check_if_watched(Movies, True)
                    break
                elif flag == "f":
                    check_if_watched(Movies)
                    break
                elif flag == "c":
                    break
            break
        elif flag == "n":
            break
    make_README(Movies)
