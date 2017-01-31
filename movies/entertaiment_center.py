import media
import fresh_tomatoes

# Movie information
lala_land = media.Movie("La La Land", "American romantic musical comedy-drama film",
                        "https://upload.wikimedia.org/wikipedia/en/a/ab/La_La_Land_%28film%29.png",
                        "https://www.youtube.com/watch?v=DBUXcNTjviI")

zootopia = media.Movie("Zootopia", "3D computer-animated comedy-adventure film",
                       "https://upload.wikimedia.org/wikipedia/en/e/ea/Zootopia.jpg",
                       "https://www.youtube.com/watch?v=ns9kL1JILeo")

ghostbusters = media.Movie("Ghost Busters", "The story of four women who start a ghost-catching business in New York City",
                           "https://upload.wikimedia.org/wikipedia/en/3/32/Ghostbusters_2016_film_poster.png",
                           "https://www.youtube.com/watch?v=w3ugHP-yZXw")

toy_story = media.Movie("Toy Story", "A story of a boy and his toys that come to life",
                        "http://upload.wikimedia.org/wikipedia/en/1/13/Toy_Story.jpg",
                        "https://www.youtube.com/watch?v=vwyZH85NQC4")
#print(toy_story.storyline)

avatar = media.Movie("Avatar", "A marine on an alien planet",
                     "http://upload.wikimedia.org/wikipedia/id/b/b0/Avatar-Teaser-Poster.jpg",
                     "http://www.youtube.come/watch?v=-9ceBgWV8io")

school_of_rock = media.Movie("School of Rock", "Storyline",
                             "http://upload.wikimedia.org/wikipedia/en/1/11/School_of_Rock_Poster.jpg",
                             "htps://www.youtube.com/watch?v=3PsUJFEBC74")

# Make a list of movies
movies = [lala_land, zootopia, ghostbusters, toy_story, avatar, school_of_rock]

# Pass the list to open_Movies_pages
fresh_tomatoes.open_movies_page(movies)
