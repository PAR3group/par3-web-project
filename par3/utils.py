SHAFT_MULTIPLIER = {
    "driver": 1.5,
    "wood5": 1.8,
    "utility4": 2.2,
    "iron7": 3.1
}


def convert_distance(distance, unit):

    if unit == "yd":
        return distance * 0.9144

    return distance


def convert_speed(speed, unit):

    if unit == "mph":
        return speed * 0.44704

    return speed


def recommend_shaft_weight(
    gender,
    height,
    weight,
    distance,
    multiplier
):

    if gender == "male":
        divisor = 10
    else:
        divisor = 11

    shaft = ((height + distance) / divisor) * multiplier

    if weight <= 55:
        shaft -= 5

    elif weight > 75:
        shaft += 5

    return round(shaft)


def recommend_flex(speed):

    if speed <= 31:
        return "L"

    elif speed <= 35:
        return "A"

    elif speed <= 40:
        return "R"

    elif speed <= 47:
        return "S"

    else:
        return "X"


def recommend_flex_by_distance(distance):

    if distance <= 170:
        return "L"

    elif distance <= 190:
        return "A"

    elif distance <= 220:
        return "R"

    elif distance <= 260:
        return "S"

    else:
        return "X"