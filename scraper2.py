import requests
from bs4 import BeautifulSoup
import json


class movie_class():
    def __init__(self, title, category, date, link, watched=False):
        self.title = title
        self.category = category
        self.date = date
        self.link = link
        self.watched = watched

    def get_title(self):
        return self.title

    def get_category(self):
        return self.category

    def get_date(self):
        return self.date

    def get_link(self):
        return self.link

    def get_watched(self):
        return self.watched

class movielist_class():
    def __init__(self):
        self.categories = []
        self.movielist = []

    def add_movie(self, movie):
        for i in range(len(categories)):
            if self.categories[i] == movie.get_category():
                self.movielist[i].append(movie)
        else:
            self.categories.append(movie.get_category())
            self.movielist[-1].append(movie)

    def get_categories(self):
        return self.categories

    def get_movies(self):
        return self.movielist

    def is_in_list(self, new_movie):
        for i in range(len(self.categories)):
            if new_movie.get_category == categories[i]:
                for old_movie in self.movielist[i]:
                    if old_movie.get_title() == new_movie.get.title()
                        return True
                break
        return False


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
            category = clean_string(category)
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


    movies = [[] for c in categories]
    # for c in categories:
    #     movies.append([])

    for item in items:

        data = item.find_all(['th', 'td'])
        try:
            link = "https://en.wikipedia.org" + data[0].a.get("href")
            title = data[0].a.get("title")
            title = title.split(" (")[0]
            title = title.split("\n")[0]
            title = clean_string(title)
            date = data[1].text
            date = date.split("\n")[0]
            date = date.split("[")[0]
            date = date.split(" (")[0]
            date = clean_string(date)
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
                    scraped_movie = movie_class(title, categories[i], date, link)
                    movies[i].append(scraped_movie)
                    break
            else:
                print(f"Error for {title}")
        except:
            pass


    if old_list:
        movie_dict_list = old_list.copy()
        for i in range(len(movies)):
            for movie in movies[i]:
                watched_flag = False
                for old_movie in old_list:
                    if old_movie["Category"] == movie.get_category() and old_movie["Title"] == movie.get_title(): #movie is in json
                        if old_movie["Date"] != movie.get_date():
                            old_movie["Date"] = movie.get_date()
                            print(f"Updated date of {movie.get_title()}")
                        if old_movie["Link"] != movie.get_link():
                            old_movie["Link"] = movie.get_link()
                            print(f"Updated link of {movie.get_title()}")
                        break
                else:
                    movie_dict = {'Title': movie.get_title(), 'Date': movie.get_date(), 'Link': movie.get_link(),
                                  'Category': movie.get_category(), 'Watched': movie.get_watched()}
                    movie_dict_list.append(movie_dict)
                    print(f"Added {movie.get_title()} to json.")
    else:
        movie_dict_list = []
        for i in range(len(movies)):
            for movie in movies[i]:
                movie_dict = {'Title': movie.get_title(), 'Date': movie.get_date(), 'Link': movie.get_link(),
                              'Category': movie.get_category(), 'Watched': movie.get_watched()}
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
    return new_movie_list

def get_movie_list():
    try:
        with open('Movies.json', 'r', encoding='UTF-8') as movie_file:
            return json.load(movie_file)
    except Exception:
        try:
            Movies = movies_from_README()
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
            category = clean_string(line.split("# ")[1])
        else:
            line = line.replace("](", "*")
            line = line.replace(")\t(", "*")
            line = line.replace(")\n", "*")
            if len(line.split("[ ]")) > 1:
                data = line[7:-1].split("*")
                scraped_movie = movie_class(clean_string(data[0]),category, clean_string(data[2]), clean_string(data[1]), False)
                movie_dict_list.append(
                    {'Title': scraped_movie.get_title(), 'Date': scraped_movie.get_date(),
                     'Link': scraped_movie.get_link(), 'Category': scraped_movie.get_category(),
                     'Watched': scraped_movie.get_watched()})

            elif len(line.split("[x]")) > 1:
                data = line[7:-1].split("*")
                scraped_movie = movie_class(clean_string(data[0]),category, clean_string(data[2]), clean_string(data[1]), True)
                movie_dict_list.append(
                    {'Title': scraped_movie.get_title(), 'Date': scraped_movie.get_date(),
                     'Link': scraped_movie.get_link(), 'Category': scraped_movie.get_category(),
                     'Watched': scraped_movie.get_watched()})
    old_readme.close()
    return movie_dict_list


def update_movies_from_README(old_movie_list):
    old_readme = open('README.md', 'r')
    category = None
    movie_list = old_movie_list.copy()
    for line in old_readme:
        if len(line.split("# ")) > 1:
            category = clean_string(line.split("# ")[1])
        else:
            line = line.replace("](", "*")
            line = line.replace(")\t(", "*")
            line = line.replace(")\n", "*")
            if len(line.split("[ ]")) > 1: #movie is unwatchced
                data = line[7:-1].split("*")
                scraped_movie = movie_class(clean_string(data[0]), category, clean_string(data[2]), clean_string(data[1]), False)

                for movie in movie_list:
                    if movie["Category"] == scraped_movie.get_category() and movie["Title"] == scraped_movie.get_title() and movie["Date"] == scraped_movie.get_date(): # movie exists
                        if movie["Watched"] == False:
                            break
                        else:
                            movie["Watched"] = False
                            print(f"Changed {scraped_movie.get_title()} to unwatched.")
                            break
                else:
                    movie_list.append({'Title': scraped_movie.get_title(), 'Date': scraped_movie.get_date(),
                                       'Link': scraped_movie.get_link(), 'Category': scraped_movie.get_category(),
                                       'Watched': scraped_movie.get_watched()})

                    print(f"Added {scraped_movie.get_title()} to json. Unwatched.")

            elif len(line.split("[x]")) > 1: #movie is watched
                data = line[7:-1].split("*")
                scraped_movie = movie_class(clean_string(data[0]), category, clean_string(data[2]), clean_string(data[1]), True)
                for movie in movie_list:
                    if movie["Category"] == scraped_movie.get_category() and movie["Title"] == scraped_movie.get_title() and movie["Date"] == scraped_movie.get_date(): #movie exists
                        if movie["Watched"] == True:
                            break
                        else:
                            movie["Watched"] = True
                            print(f"Changed {scraped_movie.get_title()} to watched.")
                            break
                else:
                    movie_list.append({'Title': scraped_movie.get_title(), 'Date': scraped_movie.get_date(),
                                       'Link': scraped_movie.get_link(), 'Category': scraped_movie.get_category(),
                                       'Watched': scraped_movie.get_watched()})
                    print(f"Added {scraped_movie.get_title()} to json. Watched.")
    old_readme.close()
    return movie_list


def clean_string(input_string):
    return_string = input_string
    elements_to_clean = [' ', '\n', '\t']
    while return_string[0] in elements_to_clean:
        return_string = return_string[1:]

    while return_string[-1] in elements_to_clean:
        return_string = return_string[:-1]
    return return_string


def clean_dictionary_strings(input_movies):
    movies = input_movies.copy()
    for movie in movies:
        movie["Title"] = clean_string(movie["Title"])
        movie["Category"] = clean_string(movie["Category"])
        movie["Date"] = clean_string(movie["Date"])

        # movie["Link"]
        # movie["Watched"]
    return movies

if __name__ == "__main__":
    Movies = get_movie_list()
    Movies = clean_dictionary_strings(Movies)
    save_json(Movies)
    print("\nUpdate movies from README.md?")
    while True:
        flag = input("(Yes/No/Cancel): ")
        flag = flag.lower()
        if flag == "y":
            Movies = update_movies_from_README(Movies)
            save_json(Movies)
            break
        elif flag == "n":
            break
    print("\nUpdate movies from wikipedia?")
    while True:
        flag = input("(Yes/No/Cancel): ")
        flag = flag.lower()
        if flag == "y":
            Movies = update_from_web(Movies)
            save_json(Movies)
            break
        elif flag == "n":
            break
    print("\nCheck watched status?")
    while True:
        flag = input("(Yes/No): ")
        flag = flag.lower()
        if flag == "y":
            print("\nAll or False?")
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
    print("\nUpdate README?")
    while True:
        flag = input("(Yes/No): ")
        flag = flag.lower()
        if flag == "y":
            make_README(Movies)
            break
        elif flag == "n":
            break
