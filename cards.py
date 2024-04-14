from termcolor import colored


def show_my_cards(hand_string: str):
    suits = {'S': '♠', 'C': '♣', 'H': '♥', 'D': '♦'}
    cards = hand_string.split(':')[1].replace(' ', '').split(',')
    output = " "
    for card in cards:
        output += "╭────"
    output += "─────╮\n"
    for card in cards[:]:
        if card[1] == 'D' or card[1] == 'H':
            if card[0] == 'T':
                output += " | " + colored("10", 'red')
            else:
                output += " | " + colored(card[0], 'red') + " "
        else:
            if card[0] == 'T':
                output += " | 10"
            else:
                output += " | " + card[0] + " "
    output += "      │\n"

    for card in cards:
        output += " | "
        if card[1] == 'D' or card[1] == 'H':
            output += colored(suits[card[1]], 'red') + " "
        else:
            output += suits[card[1]] + " "
    output += "      │"
    return output


def make_full_size_card(card: str):
    # Returns a 10 x 7 card
    suits = {'S': '♠', 'C': '♣', 'H': '♥', 'D': '♦'}
    output =  f"╭────────╮\n│ "
    if card[1] == 'D' or card[1] == 'H':
        if card[0] == 'T':
            output += colored("10", 'red')
        else:
            output += colored(card[0], 'red') + " "
    else:
        if card[0] == 'T':
            output += "10"
        else:
            output += card[0] + " "
    output += "     │\n│ "
    if card[1] == 'D' or card[1] == 'H':
        output += colored(suits[card[1]], 'red')
    else:
        output += suits[card[1]]
    output += "      │\n│        │\n│      "
    if card[1] == 'D' or card[1] == 'H':
        output += colored(suits[card[1]], 'red')
    else:
        output += suits[card[1]]
    output += " │\n│     "
    if card[1] == 'D' or card[1] == 'H':
        if card[0] == 'T':
            output += colored("10", 'red')
        else:
            output += " " + colored(card[0], 'red')
    else:
        if card[0] == 'T':
            output += "10"
        else:
            output += " " + card[0]
    output += " │\n╰────────╯"
    return output


def make_table(size_x: int, size_y: int):
    output = "╭" + "─"*size_x + "╮\n"
    for i in range(size_y):
        output += "│" + " "*size_x + "│\n"
    output += "╰" + "─" * size_x + "╯\n"
    return output

def make_draw_area(size_x: int, size_y: int):
   return ("x" * size_x + "\n") * size_y

#print(make_full_size_card("TD"))
#print(make_full_size_card("9C"))

#print(make_table(50, 15))


def place(what: str, on_where: str, where_x: int, where_y: int) -> str:
    # Split the target string into lines
    lines = on_where.split('\n')

    # Split what we want to place into lines
    what_lines = what.split('\n')

    # Determine the number of lines and the length of the longest line in `what`
    num_lines = len(what_lines)
    max_length = max(len(line) for line in what_lines)

    # Replace the specified area in `on_where` with `what`
    for i in range(num_lines):
        if i + where_x >= len(lines):
            # If `what` extends beyond the number of lines in `on_where`, stop.
            break
        line = lines[i + where_x]

        # Ensure the line is long enough to receive `what`
        if len(line) < where_y + max_length:
            line = line.ljust(where_y + max_length)

        # Use slicing to insert the new content
        line = line[:where_y] + what_lines[i] + line[where_y + len(what_lines[i]):]
        lines[i + where_x] = line

    # Join the lines back into a full string
    new_on_where = '\n'.join(lines)
    return new_on_where


#drawArea = make_draw_area(80, 22)
#print(drawArea)
#table = make_table(50, 15)
#drawing = place(table, drawArea, 2, 4)
#print(drawing)


b = """
                                Hans
          ╭──────────────────────────────────────────────╮
          │                                              │
          │                  ╭────────╮                  │
          │                  │ 8      │                  │
          │                  │ ♣      │                  │
          │                  │        │                  │
          │      ╭────────╮  │      ♣ │  ╭────────╮      │
          │      │ 9      │  │      8 │  │ 8      │      │
          │      │ ♠      │  ╰────────╯  │ ♣      │      │ 
Jóhannnus │      │        │      ⬅       │        │      │ Per
          │      │      ♠ │  ╭────────╮  │      ♣ │      │ 
          │      │      9 │  │ 8      │  │      8 │      │
          │      ╰────────╯  │ ♣      │  ╰────────╯      │
          │                  │        │                  │
          │                  │      ♣ │                  │
          │                  │      8 │                  │
          │                  ╰────────╯                  │
          │                                              │
          ╰──────────────────────────────────────────────╯ 
                                Tróndur
           ╭────╭────╭────╭────╭────╭────╭────╭─────────╮
           | 10 | K  | 8  | Q  | J  | 8  | 9  | 8       │
           | ♥  | ♠  | ♦  | ♣  | ♣  | ♠  | ♠  | ♣       │
"""

c= """
                                Hans
          ╭──────────────────────────────────────────────╮
          │                                              │
          │                  ╭────────╮                  │
          │                  │ 8      │                  │
          │                  │ ♣      │                  │
          │                  │        │                  │
          │      ░░░░░░░░░░  │      ♣ │  ╭────────╮      │
          │      ░░░░░░░░░░  │      8 │  │ 8      │      │
          │      ░░░░░░░░░░  ╰────────╯  │ ♣      │      │ 
Jóhannnus │      ░░░░░░░░░░      ⬅       │        │      │ Per
          │      ░░░░░░░░░░  ╭────────╮  │      ♣ │      │ 
          │      ░░░░░░░░░░  │ 8      │  │      8 │      │
          │      ░░░░░░░░░░  │ ♣      │  ╰────────╯      ┆
          │                  │        │                  ┆
          │                  │      ♣ │                  │
          │                  │      8 │                  │
          │                  ╰────────╯                  │
          │                                              │
          ╰──────────────────────────────────────────────╯ 
                                Tróndur
           ╭────╭────╭────╭────╭────╭────╭────╭─────────╮
           | 10 | K  | 8  | Q  | J  | 8  | 9  | 8       │
           | ♥  | ♠  | ♦  | ♣  | ♣  | ♠  | ♠  | ♣       │

"""

c= """
                                Hans
          ╭──────────────────────────────────────────────╮
          │                                              │
          │                  ░░░░░░░░░░                  │
          │                  ░░░░░░░░░░                  │
          │                  ░░░░░░░░░░                  │
          │                  ░░░░░░░░░░                  │
          │      ░░░░░░░░░░  ░░░░░░░░░░  ░░░░░░░░░░      │
          │      ░░░░░░░░░░  ░░░░░░░░░░  ░░░░░░░░░░      │
          │      ░░░░░░░░░░  ░░░░░░░░░░  ░░░░░░░░░░      │ 
Jóhannnus │      ░░░░░░░░░░      ⬅       ░░░░░░░░░░      │ Per
          │      ░░░░░░░░░░  ░░░░░░░░░░  ░░░░░░░░░░      │ 
          │      ░░░░░░░░░░  ░░░░░░░░░░  ░░░░░░░░░░      │
          │      ░░░░░░░░░░  ░░░░░░░░░░  ░░░░░░░░░░      ┆
          │                  ░░░░░░░░░░                  ┆
          │                  ░░░░░░░░░░                  │
          │                  ░░░░░░░░░░                  │
          │                  ░░░░░░░░░░                  │
          │                                              │
          ╰──────────────────────────────────────────────╯ 
                                Tróndur
           ╭────╭────╭────╭────╭────╭────╭────╭─────────╮
           | 10 | K  | 8  | Q  | J  | 8  | 9  | 8       │
           | ♥  | ♠  | ♦  | ♣  | ♣  | ♠  | ♠  | ♣       │

"""



#print(c)
