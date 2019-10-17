from django.shortcuts import render, redirect
from .models import Movie, Person, PersonMovie, Genre
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def all_movies(request):
    movies = Movie.objects.all().order_by('year')


    return render(request, 'movies.html', {
        "movies_app": movies
    })

def movie_det(request, mov_id):
    movie = Movie.objects.get(pk=mov_id)
    genre = movie.genre.filter()
    roles = PersonMovie.objects.filter(movie_id=mov_id)


    return render(request, 'movie_details.html', {
        'movie': movie,
        'genre': genre,
        'roles': roles
    })

def persons_list(request):
    persons = Person.objects.all()

    return render(request, 'persons.html', {
        'persons': persons
    })

@csrf_exempt
def edit_person(request, p_id):


    if request.method == 'GET':
        person = Person.objects.get(pk=p_id)

        return render(request, 'edit_person.html', {
            'person': person
        })

    elif request.method == 'POST':
        if request.POST['action'] == 'update':
            f_name = request.POST['first_name']
            l_name = request.POST['last_name']

            if f_name and l_name:
                p = Person.objects.get(pk=p_id)
                p.first_name = f_name
                p.save()
                p.last_name = l_name
                p.save()
                return render(request, 'edit_person.html', {
                    'person': p
                })
        if request.POST['action'] == 'return_list':
            return redirect(persons_list)

@csrf_exempt
def add_person(request):

    if request.method == 'GET':
        return render(request, 'add_person.html', {})


    elif request.method == 'POST':
        f_name = request.POST['first_name']
        l_name = request.POST['last_name']
        Person.objects.create(first_name=f_name, last_name=l_name)
        return redirect(persons_list)

@csrf_exempt
def edit_movie(request, m_id):


    if request.method == 'GET':
        movie = Movie.objects.get(pk=m_id)
        genre = movie.genre.filter()
        roles = PersonMovie.objects.filter(movie_id=m_id)

        return render(request, 'edit_movie.html', {
            'movie': movie,
            'genre': genre,
            'roles': roles
        })

    elif request.method == 'POST':

        if request.POST['action'] == 'update':
            title = request.POST['title']
            year = int(request.POST['year'])
            d_last_name = request.POST['director_2']
            s_last_name = request.POST['screenplay_ln']
            rating = float(request.POST['rating'])

            m = Movie.objects.get(pk=m_id)
            g = m.genre.filter()
            m.title = title
            m.save()
            m.year = year
            m.save()
            if rating > 0 and rating <= 10:
                m.rating = rating
                m.save()
            else:
                return ('<html>Rating has to be between 0 and 10')

            d = Person.objects.get(last_name=d_last_name)
            m.director_id = d.id
            m.save()

            s = Person.objects.get(last_name=s_last_name)
            m.screenplay_id = s.id
            m.save()

            starring = PersonMovie.objects.filter(movie_id=m_id)

            return render(request, 'edit_movie.html', {
                'movie': m,
                'genre': g,
                'roles': starring
            })

        if request.POST['acton'] == 'genre_save':
            genre_id = request.POST['genre_id']
            genre = request.POST['genre']
            m = Movie.objects.get(pk=m_id)



            starring = PersonMovie.objects.filter(movie_id=m_id)

            return render(request, 'edit_movie.html', {
                'movie': m,
                'genre': g,
                'roles': starring
            })

        if request.POST['action'] == 'star_save':
            role_id = request.POST['role_id']
            star_last_name = request.POST['star_ln']
            m = Movie.objects.get(pk=m_id)
            g = m.genre.filter()
            p = Person.objects.get(last_name=star_last_name)

            star = PersonMovie.objects.get(pk=role_id)

            star.person_id = p.id
            star.save()


            starring = PersonMovie.objects.filter(movie_id=m_id)


            return render(request, 'edit_movie.html', {
                'movie': m,
                'genre': g,
                'roles': starring
            })

        if request.POST['action'] == 'return_list':
            return redirect(all_movies)







