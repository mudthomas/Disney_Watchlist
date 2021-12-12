old_list = open('half_animated.txt', 'r')
checked_list = open('half_animated_oldlist.md', 'w')

for line in old_list:
    checked_list.write('- [ ] '+line)

old_list.close()
checked_list.close()