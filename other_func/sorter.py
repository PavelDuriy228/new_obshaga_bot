async def sort_list0 (users):
    worder_users ={}
    #print(users)
    for user in users:
        worder_users[user[0]] = user[1]
    # Сортировка словаря по значениям
    sorted_worder_users = dict(sorted(worder_users.items(), key=lambda item: item[1]))
    # Вывод отсортированного словаря
    # print(sorted_worder_users)
    text = ''
    i=1
    for name, count in sorted_worder_users.items():
        text +=f"{i}. {name}:  {count}\n"
        i+=1
    return text