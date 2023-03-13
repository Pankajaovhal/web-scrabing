from bs4 import BeautifulSoup 
import requests
import json
import pprint
url="https://www.imdb.com/india/top-rated-indian-movies/"
page=requests.get(url)
soup=BeautifulSoup(page.text,"html.parser")


def scrap_top_list():
    main_div=soup.find("div",class_="lister")
    tbody=main_div.find("tbody",class_="lister-list")
    trs=tbody.find_all("tr")


    movie_r=[]
    movie_n=[]
    year_release=[]
    m_urls=[]
    m_rating=[]

    for tr in trs:
        position=tr.find("td",class_="titleColumn").get_text().strip()
        rank=""
        for i in position:
            if "." not in i:
                rank=rank+i
            else:
                break
        movie_r.append(rank)


        title=tr.find("td",class_="titleColumn").a.get_text()
        movie_n.append(title)

        y=tr.find("td",class_="titleColumn").span.get_text()
        
        year_release.append(y)
    

        mr=tr.find("td",class_="ratingColumn imdbRating").strong.get_text()
        m_rating.append(mr)

        link=tr.find("td",class_="titleColumn").a["href"]
        m_l="https://www.imdb.com"+link
        m_urls.append(m_l)

    top_movies=[]
    d={}
    for i in range(len(movie_r)):
        d["position"]=int(movie_r[i])
        d["name"]=str(movie_n[i])
        year_release[i]=year_release[i][1:5]
        d["year"]=int(year_release[i])
        d["rating"]=float(m_rating[i])
        d["url"]=m_urls[i]
        top_movies.append(d)
        d={}
    return top_movies

    # with open("sree","w")as f:
    #     json.dump(top_movies,f,indent=4)



# import pprint
# pprint.pprint(scrap_top_list())

scrapped=scrap_top_list()
def group_by_year(movies):
    years=[]
    for i in movies:
        year=i["year"]
        if year not in years:
            years.append(year)
    # return years
    movie_dict={i:[] for i in years}
    for i in movies:
        year=i["year"]
        for x in movie_dict:
            if str(x)==str(year):
                movie_dict[x].append(i)


        # with open("task2.json","w")as f:
        #     json.dump(movie_dict,f,indent=3)
    return movie_dict
# pprint.pprint(group_by_year(scrapped))
group_by_year(scrapped)

dec_arg=group_by_year(scrapped)
def group_by_decade(movies):
    moviedec={}
    list1=[]
    for i in  movies:
        print(i)
        mod=i%10
        decade=i-mod
        # print(decade)
        if decade not in list1:
            list1.append(decade)
    list1.sort()

          
    for i in list1:
        moviedec[i]=[]
    for i in moviedec:
        dec10=i+9
        for x in movies:
            if x <=dec10 and x>=i:
                for v in movies[x]:
                    moviedec[i].append(v)
    with open("task3.json","w")as f:
        json.dump(moviedec,f,indent=4)
        return moviedec
        
pprint.pprint(group_by_decade(dec_arg))

# def scrap_movie_details(movie_url):
#     page= requests.get(movie_url)
#     soup= BeautifulSoup(page.text,'html.parser')

#     title_div=soup.find('div',class_="title_wrapper").h1.get_text()
#     movie_name=''
#     for i in title_div:
#         if '(' not in i:
#             movie_name=(movie_name+i).strip()
#         else:
#             break
#     sub_div=soup.find('div',class_="subtext")
#     runtime=sub_div.find('time').get_text().strip()
#     runtime_hour=int(runtime[0])*60
#     if 'min' in sub_div:
#         runtime_minutes=int(movie_runtime[3:].strip('min'))
#         movie_runtime=runtime_hour+runtime_minutes
#     else:
#         movie_runtime=runtime_hour
#     return movie_runtime
#     # gerner=sub_div.find_all('a')
# print(scrap_movie_details(url))