import json
import time
import requests


PHOTON_URL = "https://photon.komoot.io/api/"
OSRM_TABLE_URL = "https://router.project-osrm.org/table/v1/driving/"
OUTPUT_FILE = "distance_matrix.json"

# Rough bounding box around India: min_lon, min_lat, max_lon, max_lat.
# It also covers parts of neighbouring countries, so results are
# additionally filtered by country code below.
INDIA_BBOX = "68.1,6.5,97.5,37.1"
COUNTRY_CODE = "IN"

# If OSRM has to move a point further than this to reach a road,
# warn the user that the location may be wrong.
SNAP_WARNING_METRES = 1000


def parse_place_line(answer):
    """Parse 'Name | address or place description'. Returns (name, query) or None."""
    if "|" not in answer:
        print("Use this format: Name | address or place description")
        return None

    name, query = answer.split("|", 1)
    name = name.strip()
    query = query.strip()

    if not name or not query:
        print("Please provide both a name and a place description.")
        return None

    return name, query


def ask_for_place(prompt):
    """Keep asking until the user gives a valid 'Name | description' line."""
    while True:
        parsed = parse_place_line(input(prompt).strip())
        if parsed:
            return parsed


def search_india(session, query, bias=None):
    """Search Photon for a place in India. Returns up to 5 Indian matches."""
    params = {
        "q": query,
        "limit": 10,          # ask for extra, because we filter some out
        "lang": "en",
        "bbox": INDIA_BBOX,   # hard limit to India's bounding box
    }

    # Soft hint: prefer results near this point (does not exclude others).
    if bias is not None:
        params["lon"], params["lat"] = bias

    response = session.get(PHOTON_URL, params=params, timeout=30)
    response.raise_for_status()
    features = response.json().get("features", [])

    # The bounding box also includes bits of Nepal, Bangladesh, Pakistan, etc.
    indian = [
        feature for feature in features
        if feature.get("properties", {}).get("countrycode") == COUNTRY_CODE
    ]
    return indian[:5]


def describe(feature):
    """Build a readable one-line label for a Photon result."""
    properties = feature.get("properties", {})
    parts = [
        properties.get(key)
        for key in (
            "name", "street", "district", "city",
            "county", "state", "postcode"
        )
    ]
    # dict.fromkeys removes duplicates while keeping order.
    return ", ".join(dict.fromkeys(part for part in parts if part))


def geocode(session, name, query, bias=None):
    """Search for a place in India and let the user choose a match."""

    while True:
        features = search_india(session, query, bias)

        if not features:
            print(f"No matches found in India for '{query}'.")
            query = input(
                "Try a simpler or more specific name "
                "(e.g. 'IISER Bhopal' or 'Chhatrapati Shivaji Terminus Mumbai'): "
            ).strip()
            continue

        print(f"\nChoose the correct match for {name}:")

        for index, feature in enumerate(features, start=1):
            label = describe(feature)
            print(f"{index}. {label or feature.get('properties')}")

        choice = input(
            "Enter the matching number, or 0 to search again: "
        ).strip()

        if choice == "0":
            query = input(
                "Enter a different place name (adding the city helps): "
            ).strip()
            continue

        if not choice.isdigit() or not 1 <= int(choice) <= len(features):
            print("Please enter one of the listed numbers.")
            continue

        feature = features[int(choice) - 1]
        longitude, latitude = feature["geometry"]["coordinates"]

        print("Selected:", describe(feature) or name)
        print("Latitude:", latitude)
        print("Longitude:", longitude)

        return float(longitude), float(latitude)


def shortest_round_trip(distance_matrix):
    """
    Exact Held-Karp TSP solver.
    Location 0 is the depot. Returns a route of matrix indices and its
    total distance in metres.
    """
    location_count = len(distance_matrix)

    if location_count == 1:
        return [0, 0], 0.0

    stop_count = location_count - 1

    # Exact TSP gets expensive quickly because the number of combinations
    # grows exponentially.
    if stop_count > 18:
        raise ValueError(
            f"There are {stop_count} non-depot stops. "
            "This exact solver is limited to 18 stops. "
            "For larger routes, we should switch to an approximate or "
            "specialized routing solver."
        )

    # dp[(visited_stops_mask, last_stop)] = (distance, previous_stop)
    dp = {}

    # Start at depot (index 0), then travel to one stop.
    for stop in range(1, location_count):
        mask = 1 << (stop - 1)
        dp[(mask, stop)] = (distance_matrix[0][stop], 0)

    # Build shortest paths through every subset of stops.
    for mask in range(1, 1 << stop_count):
        for last_stop in range(1, location_count):
            state = (mask, last_stop)

            if state not in dp:
                continue

            current_distance, _ = dp[state]

            for next_stop in range(1, location_count):
                next_bit = 1 << (next_stop - 1)

                if mask & next_bit:
                    continue

                next_mask = mask | next_bit
                candidate = (
                    current_distance
                    + distance_matrix[last_stop][next_stop]
                )
                next_state = (next_mask, next_stop)

                if (
                    next_state not in dp
                    or candidate < dp[next_state][0]
                ):
                    dp[next_state] = (candidate, last_stop)

    # Add the return leg to the depot.
    all_stops_mask = (1 << stop_count) - 1
    best_total = None
    best_last_stop = None

    for last_stop in range(1, location_count):
        total = (
            dp[(all_stops_mask, last_stop)][0]
            + distance_matrix[last_stop][0]
        )

        if best_total is None or total < best_total:
            best_total = total
            best_last_stop = last_stop

    # Reconstruct the route from the saved previous stops.
    reversed_route = []
    mask = all_stops_mask
    last_stop = best_last_stop

    while last_stop != 0:
        reversed_route.append(last_stop)
        previous_stop = dp[(mask, last_stop)][1]
        mask ^= 1 << (last_stop - 1)
        last_stop = previous_stop

    route = [0] + list(reversed(reversed_route)) + [0]
    return route, best_total


def main():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "LOCUS-Routing/1.0 (contact: abc@gmail.com)"
    })

    print("Enter each place as: Name | address or place description")
    print("Include the city for better matches, e.g. 'Depot | IISER Bhopal'")
    print("or 'Gateway | Gateway of India, Mumbai'. India only.")
    print("The first location is the depot.")
    print("Press Enter on a blank line when you have entered all stops.\n")

    depot_name, depot_query = ask_for_place("Depot: ")
    places = [(depot_name, depot_query)]
    used_names = {depot_name}

    while True:
        answer = input("Next stop (blank to finish): ").strip()

        if not answer:
            break

        parsed = parse_place_line(answer)
        if not parsed:
            continue

        name, query = parsed

        # Coordinates are stored by name, so names must be unique.
        if name in used_names:
            print(f"'{name}' is already used. Please pick a different name.")
            continue

        used_names.add(name)
        places.append((name, query))

    if len(places) < 2:
        raise ValueError("Enter a depot and at least one stop.")

    names = [name for name, _ in places]
    coordinates = {}
    bias = None  # first search has no location hint

    for index, (name, query) in enumerate(places):
        print(f"\nSearching for {name}: {query}")
        coordinates[name] = geocode(session, name, query, bias)

        # After the depot is chosen, use it as a soft hint so ambiguous
        # names (e.g. "Railway Station") rank closer places first.
        if bias is None:
            bias = coordinates[name]

        if index < len(places) - 1:
            time.sleep(1)  # be polite to the public service

    coordinate_string = ";".join(
        f"{coordinates[name][0]},{coordinates[name][1]}"
        for name in names
    )

    url = OSRM_TABLE_URL + coordinate_string
    response = session.get(
        url,
        params={"annotations": "distance"},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()

    if data.get("code") != "Ok":
        raise RuntimeError(f"OSRM routing failed: {data}")

    print("\n--- Road access checks ---")
    for name, waypoint in zip(names, data["sources"]):
        snap = waypoint["distance"]
        warning = "  <-- check this location" if snap > SNAP_WARNING_METRES else ""
        print(f"{name}: {snap:.1f} metres from the snapped road point{warning}")

    raw_distances = data["distances"]

    if any(distance is None for row in raw_distances for distance in row):
        raise ValueError(
            "At least one pair has no driving route. "
            "Check the locations or their road access."
        )

    # Keep metres for solving; round only for display.
    route_indices, total_metres = shortest_round_trip(raw_distances)

    print("\n--- Road Distance Matrix (km) ---")
    print(f"{'From / To':<32}", end="")
    for index in range(len(names)):
        print(f"{index:>10}", end="")
    print()

    for row_index, row in enumerate(raw_distances):
        print(f"{names[row_index]:<32}", end="")
        for distance in row:
            print(f"{distance / 1000:>10.2f}", end="")
        print()

    print("\n--- Shortest round trip found ---")
    print(" -> ".join(names[index] for index in route_indices))
    print(f"Total distance: {total_metres / 1000:.2f} km")

    # Save both the matrix and the route so the same data can be used later
    # when we build the QUBO.
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            {
                "locations": names,
                "coordinates_lon_lat": coordinates,
                "distances_km": [
                    [round(distance / 1000, 2) for distance in row]
                    for row in raw_distances
                ],
                "source": "OSRM public driving Table API",
                "depot": names[0],
                "shortest_route": [
                    names[index] for index in route_indices
                ],
                "shortest_route_distance_km": round(
                    total_metres / 1000, 2
                ),
            },
            file,
            indent=2,
        )

    print(f"\nSaved {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
