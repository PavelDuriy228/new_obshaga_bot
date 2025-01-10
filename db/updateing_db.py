from config import wks, bot, user_id_adm
from db import get_value_by_condition, User, get_all

async def reader ():
    print ("----- Функция reader была вызвана ----")
    mess= "Обновление БД - было совершено"
    #Отпарвление сообщении админу об обновлении БД
    await bot.send_message(user_id_adm, mess)
    # список листов
    sheet_names = wks.worksheets()   
    places = await  get_all(
        table= "Starst", column="place"
    )
    for sheet in sheet_names:                
        name_sheet = sheet.title
        print (f"----Был открыт лист -{str(name_sheet)}")
        cur_wks = wks.worksheet(name_sheet)
        # Получение названия таблицы для БД
        name_sheet = str(name_sheet).strip()

        # Получение названия всех колонок с мероприятиями в переменной title,
        # путем среза юзерских колонок 
        title = sheet.row_values(1)        
        title = title[5:]

        rows = cur_wks.get_all_values()
        rows = rows[1:]

        u_code_strsti = await get_value_by_condition(
            table= "Starst",
            column="unic_kod", 
            condition_column="place",
            condition_value=name_sheet
        )
        if u_code_strsti:            
            for row in rows :
                name = f"{str(row[1]).strip()}: {str(row[2]).strip()}"
                print(f"name: {name}")
                all_count = 0
                row= row[5:]
                comment = ""
                for i in range(len(title)):
                    zasl= title[i]
                    count = row[i]
                    if count!="" or count!='0': 
                        all_count= all_count + int(count)
                        if comment=="": comment= f"{zasl}: {count};"
                        else : comment= f"{comment}\n{zasl}: {count};"
                print()
                
                print (f"comment: \n{comment}")
                print(f"---ful: {all_count}")
                print (row)
                print("--------------------------------------")
                user = User ()
                await user.set_other_atributs(name = name, unic_kod=None, tg_user_id=None)
                
                if user.unic_kod is None or user.unic_kod == -1:
                    print("___Такого пользователя нет в базе__")
                    await user.register_user(
                        name=name, count_b=all_count, 
                        comment=comment,
                        unic_c_stars=u_code_strsti
                    )
                    await user.add_to_db()
                else:
                    if user.comment != comment:
                        await user.set_comment(
                            new_com=comment
                        )
                        await user.set_bals(
                            new_bals= all_count
                        )
        else: 
            print(f"Такого старосты нет в базе, зврегистрированные старосты\n{places}")
            print(f"\nЛисты в книге:\n{sheet_names}\n")