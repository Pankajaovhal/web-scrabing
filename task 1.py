import requests
from bs4 import BeautifulSoup
import json
url="https://www.imdb.com/india/top-rated-indian-movies/"
sample=requests.get(url)
soup=BeautifulSoup(sample.text,"html.parser") 
def scrap_top_list():
    tbody=soup.find("tbody",class_="lister-list")        
    title=tbody.find_all("tr")
    movie_name=[]
    year_of_realease=[]
    movie_urls=[]
    movie_ratings=[]
    for i in title:
        movie=i.find("td",class_="titleColumn").a.get_text()
        movie_name.append(movie)

        year_released=i.find('td',class_="titleColumn").span.get_text()
        year_of_realease.append(year_released)
        # print(year_of_realease)

        imdb_rating=i.find('td',class_="ratingColumn imdbRating").strong.get_text()
        movie_ratings.append(imdb_rating)
        # print(movie_ratings)

        link=i.find('td',class_="titleColumn").a['href']
        movie_link="https://www.imdb.com"+link
        movie_urls.append(movie_link)
        # print(movie_urls)

    # details={'name':'','year':'','rating':'','url':''}
    Top_movies=[]
    # details={}
    for j in range(len(movie_name)):
        details={}
        details['position']=j+1
        details['name']=str(movie_name[j])
        year_released=(year_of_realease[j][1:5])
        details['year']=int(year_released)
        details['rating']=float(movie_ratings[j])
        details['url']=str(movie_urls[j])
        Top_movies.append(details)
        # print(Top_movies)
        with open("movie_data.json","w") as a:
            json.dump(Top_movies,a,indent=4)
            a.close()
        with open("movie_data.json","r") as f:
            b=json.load(f)
            # print(b)
scrap_top_list()

# task 2th

scrapped=scrap_top_list()
def group_by_year(movies):
    years=[]
    for i in movies:
        year=i['year']
        if year not in years:
            years.append(year)
    movie_dict={i:[]for i in years}
    for i in movies:
        year=i['year']
        for x in movie_dict:
            if str(x)==str(year):
                movie_dict[x].append(i)
    # return movie_dict
    with open("group_by_years.json","w") as p:
        json.dump(movie_dict,p,indent=3)
        p.close()
    with open("group_by_years.json","r") as q:
        c=json.load(q)
        # print(c)
group_by_year(scrapped)


# task 3rd

arg=group_by_year(scrapped)
def group_by_decade(movies):
    moviedec={}
    list1=[]
    for index in movies:
        print(index)
        mod=index%10
        decade=index-mod
        if decade not in list1:
            list1.append(decade)
    list1.sort(list1)
    for i in list1:
        moviedec[i]=[]
    for i in moviedec:
        dec10=i+9
        for x in movies:
            if x<=dec10 and x>=i:
                for v in movies[x]:
                    moviedec.append(v)
    return(moviedec)
group_by_decade(arg)

# tast 4th

def scrap_movie_details(movie_url):
    page= requests.get(movie_url)
    soup= BeautifulSoup(page.text,'html.parser')

    title_div=soup.find('div',class_="title_wrapper").h1.get_text()
    movie_name=''
    for i in title_div:
        if '(' not in i:
            movie_name=(movie_name+i).strip()
        else:
            break
    sub_div=soup.find('div',class_="subtext")
    runtime=sub_div.find('time').get_text().strip()
    runtime_hour=int(runtime[0])*60
    if 'min' in sub_div:
        runtime_minutes=int(movie_runtime[3:].strip('min'))
        movie_runtime=runtime_hour+runtime_minutes
    else:
        movie_runtime=runtime_hour
    
    gerner=sub_div.find_all('a')
    gerner.pop()
    movie_gerner=[i.get_text() for i in gerner]

    summary=soup.find('div',class_="plot_summary")

    movie_bio=summary.find('div',class_="summary_text").get_text().strip()

    director=summary.find('div',class_="credit_summary_item")
    director_list=director.find_all('a')
    movie_director=[i.get_text().strip() for i in director_list]
scrap_movie_details(url)