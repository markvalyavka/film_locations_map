import folium

# m = folium.Map(location=[45.5236, -122.6750])
# m.save('index.html')


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

print(get_film_year_and_location(read_file()))