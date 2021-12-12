oldfile = open('disney.txt', 'r')
cleanfile = open('disney_clean.txt', 'w')
live_action = open('live_action.txt', 'w')
animated = open('animated.txt', 'w')
half_animated = open('half_animated.txt', 'w')
documentaries = open('documentaries.txt', 'w')
old_list = open('oldlist.txt', 'w')

def addToOldList(string):
    old_list.write(string)

def addToNewList(type, string):
    if type == 'A':
        animated.write(string)
    elif type == 'H':
        half_animated.write(string)

badchars = ['‡', '†', '§', '*']
for line in oldfile:
        data = line.split('\t')
        if(len(data)) == 1:
            cleanfile.write(line)
            live_action.write(line)
            animated.write(line)
            documentaries.write(line)
            old_list.write(line)
        elif len(data) >= 3:
            type, title, date = data[0], data[1], data[2]
            for char in badchars:
                temp = title.split(char)
                title = ' '.join(temp)
            title = title.strip()
            try:
                year = date.split(', ')[1]
                if len(year) >= 4:
                    year = year[:4]
            except:
                print(' ')
            cleanfile.write(type+'\t'+title+'\t('+year+')\n')
            if type == 'L':
                live_action.write(title+'\t('+year+')\n')
            elif type == 'D' or type == 'N':
                documentaries.write(title+'\t('+year+')\n')
            else:
                try:
                    if int(year) > 2016:
                        addToNewList(type, title+'\t('+year+')\n')
                    else:
                        while True:
                            print(type+'\t'+title+'\t('+year+')\n')
                            watched = input("""
                                Is this on the old list?
                                (Y/N): """)
                            if watched == "Y" or watched == "y":
                                addToOldList(title+'\t('+year+')\n')
                                break
                            elif watched == "N" or watched == "n":
                                addToNewList(type, title+'\t('+year+')\n')
                                break
                except:
                    print(' ')
oldfile.close()
cleanfile.close()
live_action.close()
animated.close()
documentaries.close()
old_list.close()