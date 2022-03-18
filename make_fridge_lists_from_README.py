old_list = open('README.md', 'r')
checked_list1 = open('old_fridge_list.txt', 'w')
checked_list2 = open('new_fridge_list.txt', 'w')
checked_list1.write("-- Gamla listan --\n")
checked_list2.write("-- Nya listan --\n")

new_flag = False
for line in old_list:
    if line == '-- Nya listan --\n':
        new_flag = True
    elif line[0] == '-':
        movie_is_watched = line[3] == 'x'
        data = line[6:].split('\t')
        title = data[0]
        if len(data) == 2:
            year = data[1][1:5]
            if movie_is_watched:
                new_line = title + "\tY\t" + year + "\n"
            else:
                new_line = title + "\tN\t" + year + "\n"
            if new_flag:
                checked_list2.write(new_line)
            else:
                checked_list1.write(new_line)
    else:
        if new_flag:
            checked_list2.write(line)
        else:
            checked_list1.write(line)

old_list.close()
checked_list1.close()
checked_list2.close()
