import psycopg2
import getpass

def fillPerson():
    print "Start: person"
    person = getStuff(IMDbConnStr, "SELECT id, name, gender, birthdate, deathdate, height FROM person")

    cur = conn.cursor()
    
    for p in person:
        id = p[0]
        name = p[1][:50] #Take only 50 first characters, because there are some weird long names from dump
        gender = p[2]
        birthdate = p[3]
        deathdate = p[4]
        
        cur.execute("INSERT INTO person(id, name, gender, dateofbirth, dateofdeath) VALUES(%s, %s, %s, %s, %s)",
            [id, name, gender, birthdate, deathdate])
            
    cur.close()
    
    print "Finish: person"
    
def fillMovie():
    print "Start: movie"
    movie = getStuff(IMDbConnStr, "SELECT id, title, language, releasedate FROM movie")
    
    cur = conn.cursor()
    
    for m in movie:
        id = m[0]
        title = m[1]
        language = m[2]
        releaseDate = m[3]
        
        cur.execute("INSERT INTO movie(id, dateofrelease, title, language) VALUES(%s, %s, %s, %s)",
            [id, releaseDate, title, language])
    
    cur.close()
    
    print "Finish: movie"
    
def fillActorDirector():
    print "Start: actor/director"
    involved = getStuff(IMDbConnStr, "SELECT personid, movieid, role FROM involved")
    
    cur = conn.cursor()
    
    for i in involved:
        personId = i[0]
        movieId = i[1]
        role = i[2]
        
        if role == "actor":
            cur.execute("INSERT INTO actorin(movieid, personid) VALUES(%s, %s)", [movieId, personId])
        elif role == "director":
            cur.execute("INSERT INTO directorof(movieid, personid) VALUES(%s, %s)", [movieId, personId])
                
    cur.close()
    
    print "Finish: actor/director"
    
def fillRefersto():
    print "Start: refersto"
    movieref = getStuff(IMDbConnStr, "SELECT fromid, toid FROM movieref")
    
    cur = conn.cursor()
    
    for mr in movieref:
        fromId = mr[0]
        toId = mr[1]
        
        cur.execute("INSERT INTO refersto(fromid, toid) VALUES(%s, %s)", [fromId, toId])
        
    cur.close()
    
    print "Finish: refersto"
    
def fillRates():
    print "Start: rates"
    ratings = getStuff(IMDbConnStr, "SELECT DISTINCT ratings.user, ratings.movieid, ratings.rating FROM ratings")
    
    cur = conn.cursor()
    
    for r in ratings:
        user = r[0]
        movieId = r[1]
        rating = r[2]
        
        cur.execute("INSERT INTO rates(movieid, email, value) VALUES(%s, %s, %s)", [movieId, user, rating])
        
    cur.close()
    
    print "Finish: rates"
    
def fillGenre():
    print "Start: genre"
    genre = getStuff(IMDbConnStr, "SELECT DISTINCT genre FROM genre")
    
    cur = conn.cursor()
    
    for g in genre:
        genre = g[0]
        
        cur.execute("INSERT INTO genre(name) VALUES(%s)", [genre])
        
    cur.close()
    
    print "Finish: genre"
    
def fillIs():
    print "Start: is"
    genre = getStuff(IMDbConnStr, "SELECT DISTINCT movieid, genre FROM genre")
    
    cur = conn.cursor()
    
    for g in genre:
        movieid = g[0]
        genre = g[1]
        
        cur.execute("INSERT INTO \"is\"(name, movieid) VALUES(%s, %s)", [genre, movieid])
        
    cur.close()
    
    print "Finish: is"
    
def getStuff(connStr, query):
    conn = psycopg2.connect(connStr)
    cur = conn.cursor()
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

    
username = "postgres"
password = getpass.getpass()

dbsConnStr = "dbname=DBCourse user=%s password=%s" % (username, password)
IMDbConnStr = "dbname=imdb user=%s password=%s" % (username, password)

conn = psycopg2.connect(dbsConnStr)
    
fillPerson()
fillMovie()
fillActorDirector()
fillRefersto()
fillRates()
fillGenre()
fillIs()

conn.commit()
conn.close()