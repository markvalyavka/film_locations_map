import folium
import geopy
import json


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

    Function to analyze valid lines and save them in a proper form.
    dict{ *year* : { (*film_name*, *location*), ...  } }

    """
    film_dict = {}

    while lines_set:
        try:
            film, location = lines_set.pop().split("			")
            film_name = film[film.index("\""):film.index("(") - 1]
            film_year = int(film[film.index("(") + 1:film.index(")")])
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

    if year in film_dict:
        while film_dict[year] and len(closest_film_lst) < 100:
            try:
                film = film_dict[year].pop()
                film_loc_obj = geolocator.geocode(film[1])
                film_loc = film_loc_obj.latitude, film_loc_obj.longitude
                closest_film_lst.append((film[0], film_loc))
            except:
                continue
    else:
        return None

    closest_film_lst.sort(key=lambda elm: abs(elm[1][0] - location[0]) + abs(elm[1][1] - location[1]))
    closest_film_set = set(closest_film_lst[0:10])

    return closest_film_set


def create_map(closest_film_set, location, year):
    """ (set) -> (None)

    Function to create .html file with map of 10 closest
    films to user location.
    """

    map = folium.Map(location=location)
    film_locations = folium.FeatureGroup(name="Film Locations")
    film_locations.add_child(folium.Marker(location=list(location),
                                           popup="YOU",
                                           icon=folium.Icon(color="green")))
    while closest_film_set:
        film = closest_film_set.pop()
        film_locations.add_child(folium.Marker(location=[film[1][0], film[1][1]],
                                               popup=film[0],
                                               icon=folium.Icon(color="red")))

    map.add_child(film_locations)
    map.add_child(folium.GeoJson(data=json.load(open("world_population.json", encoding="utf-8-sig")),
                                 name="World Population",
                                 style_function=lambda x: {
                                     'fillColor': 'green' if x["properties"]["POP2005"] <= 10000000
                                         else 'orange' if x["properties"]["POP2005"] <= 20000000
                                         else 'red'}))

    map.add_child(folium.GeoJson(data=json.load(open("states.geojson", encoding="utf-8-sig")),
                                 name="US States",
                                 style_function=lambda x: {
                                     'fillColor': 'purple' if int(x["properties"]["STATEFP"]) % 2 == 0
                                         else 'yellow'}))

    map.add_child(folium.LayerControl())
    map.save('map_{year}.html'.format(year=year))


if __name__ == "__main__":

    film_year = int(input("Please enter a year you would like to have a map for: "))
    location_coordinates = (input("Please enter your location (format: lat, long): "))
    location_coordinates = tuple([float(coord.strip()) for coord in location_coordinates.split(",")])
    print("Analyzing data...")
    closest_films_set = find_closest_films(film_year, location_coordinates)
    if closest_films_set is not None:
        create_map(closest_films_set, location_coordinates, film_year)
        print("Check your map by opening map_{film_year}.html file".format(film_year=film_year))
    else:
        print("Couldn't find any films for that year. Try another one.")
