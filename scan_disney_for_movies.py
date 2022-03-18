def inOldFridgeList(title):
    for i in range(len(old_fridge_data)):
        if title == old_fridge_data[i][0]:
            return True
    return False


def inNewFridgeList(title):
    for i in range(len(new_fridge_data)):
        if title == new_fridge_data[i][0]:
            return True
    return False


def inIgnoreList(title):
    for i in range(len(ignored_data)):
        if title == ignored_data[i][0]:
            return True
    return False


oldfile = open('disney.txt', 'r')
cleanfile = open('disney_clean.txt', 'w')
unlisted = open('unlisted.txt', 'w')

old_fridge_list = open('old_fridge_list.txt', 'r')
old_fridge_data = []
for line in old_fridge_list:
    data = line.split('\t')
    if len(data) == 3:
        title = data[0]
        is_watched = data[1] == 'Y'
        year = data[2].split('\n')[0]
        old_fridge_data.append([title, is_watched, year])

new_fridge_list = open('new_fridge_list.txt', 'r')
new_fridge_data = []
for line in new_fridge_list:
    data = line.split('\t')
    if len(data) == 3:
        title = data[0]
        is_watched = data[1] == 'Y'
        year = data[2].split('\n')[0]
        new_fridge_data.append([title, is_watched, year])

ignored_list = open('ignored.txt', 'r')
ignored_data = []
for line in ignored_list:
    data = line.split('\t')
    if len(data) == 3:
        title = data[0]
        is_watched = data[1] == 'Y'
        year = data[2].split('\n')[0]
        ignored_data.append([title, is_watched, year])

live_action_list = []
documentaries_list = []
animated_list = []
half_animated_list = []

badchars = ['‡', '†', '§', '*']
for line in oldfile:
    data = line.split('\t')
    if(len(data)) == 1:
        print(line)
        cleanfile.write(line)
    elif len(data) >= 3:
        movie_type, title, date = data[0], data[1], data[2]
        for char in badchars:
            temp = title.split(char)
            title = ' '.join(temp)
        title = title.split("[")[0]
        title = title.strip()
        try:
            year = date.split(', ')[1]
            if len(year) >= 4:
                year = year[:4]
        except:
            print(' ')
        cleanfile.write(movie_type+'\t'+title+'\t('+year+')\n')
        if movie_type == 'L' and not inIgnoreList(title):
            live_action_list.append([title, False, year])
        elif (movie_type == 'D' or movie_type == 'N') and not inIgnoreList(title):
            documentaries_list.append([title, False, year])
        else:
            if not inOldFridgeList(title) and not inNewFridgeList(title) and not inIgnoreList(title):
                print(title)
                if movie_type == "A":
                    animated_list.append([title, False, year])
                elif movie_type == "H":
                    half_animated_list.append([title, False, year])

if len(animated_list) > 0:
    unlisted.write("-- Animated --\n")
    for movie in animated_list:
        unlisted.write(movie[0]+'\tN\t('+movie[2]+')\n')

if len(half_animated_list) > 0:
    unlisted.write("\n-- Half Animated --\n")
    for movie in half_animated_list:
        unlisted.write(movie[0]+'\tN\t('+movie[2]+')\n')

if len(live_action_list) > 0:
    unlisted.write("-- Live Action --\n")
    for movie in live_action_list:
        unlisted.write(movie[0]+'\tN\t('+movie[2]+')\n')

if len(documentaries_list) > 0:
    unlisted.write("\n-- Documentaries --\n")
    for movie in documentaries_list:
        unlisted.write(movie[0]+'\tN\t('+movie[2]+')\n')

oldfile.close()
cleanfile.close()
unlisted.close()

old_fridge_list.close()
new_fridge_list.close()
ignored_list.close()