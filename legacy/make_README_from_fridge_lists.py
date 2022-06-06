
old_list1 = open('old_fridge_list.txt', 'r')
old_list2 = open('new_fridge_list.txt', 'r')
checked_list = open('README.md', 'w')

for line in old_list1:
    data = line.split('\t')
    if len(data) == 3:
        title = data[0]
        is_watched = data[1] == 'Y'
        year = data[2].split('\n')[0]
        if is_watched:
            checked_list.write('- [x] '+title+'\t('+year+")\n")
        else:
            checked_list.write('- [ ] '+title+'\t('+year+")\n")
    else:
        checked_list.write(line)

for line in old_list2:
    data = line.split('\t')
    if len(data) == 3:
        title = data[0]
        is_watched = data[1] == 'Y'
        year = data[2].split('\n')[0]
        if is_watched:
            checked_list.write('- [x] '+title+'\t('+year+")\n")
        else:
            checked_list.write('- [ ] '+title+'\t('+year+")\n")
    else:
        checked_list.write(line)

old_list1.close()
old_list2.close()
checked_list.close()
