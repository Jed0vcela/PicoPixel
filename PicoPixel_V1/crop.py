import starquake

def crop(bitmap, x, y, width=32, height=8):
    temp = bitmap[y:y+height]
    return [line[x:x+width] for line in temp]


def show_bitmap(bitmap):
    for line in bitmap:
        print(line)


cropped = crop(starquake.bitmap, 50, 10)
show_bitmap(cropped)
