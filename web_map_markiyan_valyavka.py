import folium
import geopy

# m = folium.Map(location=[45.5236, -122.6750])
# m.save('index.html')
# geolocator = geopy.Nominatim(user_agent="myGeolocator")
# loc = geolocator.geocode("Las Vegas, Nevada, USA")
# print(loc)

def read_file():
    """ (None) -> (set)

    Function to read valid lines from a file.
    """

    lines_set = set()

    with open("locations.list.txt", "r", encoding="utf-8", errors="ignore") as film_file:
        for line in film_file:
            if line.startswith("\""):
                lines_set.add(line)

    return lines_set

def get_film_year_and_location(lines_set):
    """ (set) -> (dict)

    Function to analyze valid lines and save them in a proper form
    dict{ *year* : { (*film_name*, *location*), ...  } }

    """
    film_dict = {}

    while lines_set:
        try:
            film, location = lines_set.pop().split("			")
            film_name = film[film.index("\""):film.index("(")-1]
            film_year = int(film[film.index("(")+1:film.index(")")])
            if film_year in film_dict:
                film_dict[film_year].add((film_name, location.strip()))
            else:
                film_dict[film_year] = {(film_name, location.strip())}
        except:
            continue

    return film_dict

def find_closest_films(year, location):
    """ (int),(tuple) -> (set)

    Function get a year of a film, user location, and filters 10 closest film.
    """
    film_dict = get_film_year_and_location(read_file())
    closest_film_lst = []
    geolocator = geopy.Nominatim(user_agent="myGeolocator", timeout=10)
    x = 49.83826, 24.02324


    if year in film_dict:
        while film_dict[year] and len(closest_film_lst) < 50:
            try:
                film = film_dict[year].pop()
                film_loc_obj = geolocator.geocode(film[1])
                film_loc = film_loc_obj.latitude, film_loc_obj.longitude
                closest_film_lst.append((film[0], film_loc))
                # print(film[0],film_loc)
            except:
                continue

    closest_film_lst.sort(key = lambda elm: abs(elm[1][0]-x[0])+abs(elm[1][1]-x[1]))
    closest_film_set = set(closest_film_lst[0:10])

    return closest_film_set
print(find_closest_films(2000, 'a'))

