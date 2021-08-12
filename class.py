def add_book( name, short_name, tel_link, year, sem):
    f = open("book.txt", "a")
    f.write( name + '|' + short_name + '|' + tel_link + '|' + str(year) + '|' + str(sem) )
    f.write('\n')
    f.close()

def find_book(book_name):
    f = open('book.txt')
    books = f.read().split('\n')
    books.pop()

    for book in books:
        name, short_name, link, year, sem= book.split('|')
        if(name.lower()==book_name.lower() or book_name.lower()==short_name.lower()):
            return f"Book Name : {name} \nTelegram Link: {link}\n"

    f.close()
    return 'Book not found'

def show_sem(q_year, q_sem):

    if (int(q_sem)<0 and int(q_sem)>2) or (int(q_year)<0 and int(q_year)>4):
        return 'invalid search'

    f = open('book.txt')
    books = f.read().split('\n')
    books.pop()

    yr=''
    sm=''

    if(q_year=='1'):yr='1st'
    elif(q_year=='2'):yr='2nd'
    elif(q_year=='3'):yr='3rd'
    elif(q_year=='4'):yr='4th'

    if(q_sem=='1'):sm='1st'
    elif(q_sem=='2'):sm='2nd'

    ret = ''
    for book in books:
        name, short_name, link, year, sem= book.split('|')
        if q_year==year and q_sem==sem:
            ret += f"Book Name : {name} \nTelegram Link: {link}\n\n"

    if ret=='':
        ret = 'Books not published yet'
    else:
        ret = f"The books for {yr}-year and {sm}-semister\n\n" + ret

    f.close()
    return ret


def del_book(book_name):
    f = open('book.txt')
    books = f.read().split('\n')
    books.pop()
    f.close()

    i = 0
    for book in books:
        name, short_name, link, year, sem= book.split('|')
        if(name.lower()==book_name.lower() or book_name.lower()==short_name.lower()):
            books.pop(i)
            break
        i+=1    

    f = open('book.txt','w')
    for book in books:
        f.write(book+'\n')
    
    return 'Work done'

add_book("Programing with C"               , "C programing", "https://t.me/sustcse2019/7", 1, 1)
add_book("Discrete Math"                   , "DM"          , "https://t.me/sustcse2019/2", 1, 1)
add_book("Fundamentals of Eletric Circuits", "EEE-1//1"    , "https://t.me/sustcse2019/3", 1, 1)
add_book("Matrix"                          , "Marix"       , "https://t.me/sustcse2019/6", 1, 1)
add_book("Linear Algebra"                  , "LA"          , "https://t.me/sustcse2019/5", 1, 1)


add_book("Data Structure"                       , "DS"                    , "https://t.me/sustcse2019/9" , 1, 2)
add_book("Electronic Devices and Circuit Theory", "EEE-1//2"              , "https://t.me/sustcse2019/13", 1, 2)
add_book("Calculus"                             , "Thomas Calculus"       , "https://t.me/sustcse2019/10", 1, 2)
add_book("Calculus"                             , "Das Mukherjee Calculus", "https://t.me/sustcse2019/11", 1, 2)
add_book("Fundamentals of Physics"              , "Physics"               , "https://t.me/sustcse2019/14", 1, 2)


# add_book("Java" , "JV" , "www.telegram.com", 2,1 )


# show_all_book()
# print(find_book('calculus'))
# print(show_sem('1','2'))
# del_book('calculus')


help_command

# @client.command()
# async def embed(ctx):
#     embed=discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/", 
#         description="This is an embed that will show how to build an embed and the different components", 
#         color=0xFF5733)
#     await ctx.send(embed=embed)