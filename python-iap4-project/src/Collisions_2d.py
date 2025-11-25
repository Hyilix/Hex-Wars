# Various 2D collisions
# Shout-out to https://www.jeffreythompson.org/collision-detection/ for the formulas

# Point in Triangle collision. It is expected that the Triangle is passed as an array of 3 tuples
def point_trig(point : tuple[int, int], trig : list[tuple[int, int]]):
    print(f"Point: {point}")
    print("Trig points:")
    for p in trig:
        print(f"{p}");

    (x1, y1) = trig[0]
    (x2, y2) = trig[1]
    (x3, y3) = trig[2]
    (px, py) = point

    trig_area = abs( (x2-x1)*(y3-y1) - (x3-x1)*(y2-y1) )

    area_1 = abs( (x1-px)*(y2-py) - (x2-px)*(y1-py) )
    area_2 = abs( (x2-px)*(y3-py) - (x3-px)*(y2-py) )
    area_3 = abs( (x3-px)*(y1-py) - (x1-px)*(y3-py) )

    total_area = area_1 + area_2 + area_3

    return trig_area == total_area
