from cards import make_draw_area, make_table, place


def drawScreen(myname, playerId):
    drawArea = make_draw_area(80, 22)
    table = make_table(50, 15)
    drawing = place(table, drawArea, 3, 3)
    if playerId == "1":
        drawing = place("4", drawing, 1, 11)
        drawing = place("3", drawing, 28, 2)
        drawing = place("2", drawing, 56, 11)
    if playerId == "2":
        drawing = place("1", drawing, 1, 11)
        drawing = place("4", drawing, 28, 2)
        drawing = place("3", drawing, 56, 11)
    if playerId == "3":
        drawing = place("2", drawing, 1, 11)
        drawing = place("1", drawing, 28, 2)
        drawing = place("4", drawing, 56, 11)
    if playerId == "4":
        drawing = place("3", drawing, 1, 11)
        drawing = place("2", drawing, 28, 2)
        drawing = place("1", drawing, 56, 11)

    drawing = place(myname, drawing, 25, 20)
    table = make_table(16, 4)
    drawing = place(table, drawing, 60, 3)
    table = make_table(10, 4)
    drawing = place(table, drawing, 60, 3)
    drawing = place(make_table(16, 1), drawing, 60, 8)
    drawing = place(make_table(16, 8), drawing, 60, 10)

    drawing = place("Spælarir──┬", drawing, 61, 3)
    drawing = place("Ping", drawing, 72, 3)
    drawing = place("├Trumfur───┴─────┤", drawing, 60, 8)
    drawing = place("├Stigatava───────┤", drawing, 60, 10)
    drawing = place("│Vit     Tit     │", drawing, 60, 11)
    return drawing
