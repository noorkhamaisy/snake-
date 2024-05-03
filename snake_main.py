import game_parameters
from game_display import GameDisplay
from snake import Snake
from apple import Apple
from bomb import Bomb


def initial(gd):
    x, y = game_parameters.WIDTH // 2, game_parameters.HEIGHT // 2
    game_snake = Snake(3, (x, y))
    game_snake.coordinates.remove((x,y))
    game_snake.get_coordinates().append((x, y-2))
    game_snake.get_coordinates().append((x, y - 1))
    game_snake.get_coordinates().append((x, y))
    for snake_cord in game_snake.get_coordinates():
        gd.draw_cell(snake_cord[0], snake_cord[1], 'black')
    bomb_data = game_parameters.get_random_bomb_data()
    game_bomb = Bomb((bomb_data[0], bomb_data[1]), bomb_data[2], bomb_data[3])
    cord = game_bomb.get_location()
    gd.draw_cell(cord[0], cord[1], "red")
    apple1_data = game_parameters.get_random_apple_data()
    apple1 = Apple((apple1_data[0], apple1_data[1]), apple1_data[2])
    apple1_location = apple1.get_location()
    gd.draw_cell(apple1_location[0], apple1_location[1], "green")
    apple2_data = game_parameters.get_random_apple_data()
    apple2 = Apple((apple2_data[0], apple2_data[1]), apple2_data[2])
    apple2_location = apple2.get_location()
    gd.draw_cell(apple2_location[0], apple2_location[1], "green")
    apple3_data = game_parameters.get_random_apple_data()
    apple3 = Apple((apple3_data[0], apple3_data[1]), apple3_data[2])
    apple3_location = apple3.get_location()
    gd.draw_cell(apple3_location[0], apple3_location[1], "green")
    return game_snake, game_bomb, [apple1, apple2, apple3]


def snake_move(snake, movekey, prevmove):
    if movekey == "Up" and not(prevmove == "Down"):
        snake.move("Up")
    if movekey == "Down" and not(prevmove == "Up"):
        snake.move("Down")
    if movekey == "Right" and not(prevmove == "Left"):
        snake.move("Right")
    if movekey == "Left" and not(prevmove == "Right"):
        snake.move("Left")


def checking(location, lst):
    for i in range(len(lst)):
        if location == lst[i]:
            return i
    return -1


def get_new_apple_location(bad_coordinates):
    new_data = game_parameters.get_random_apple_data()
    while (new_data[0], new_data[1]) in bad_coordinates:
        new_data = game_parameters.get_random_apple_data()
    return new_data


def get_new_bomb_location(bad_coordinates):
    new_data = game_parameters.get_random_bomb_data()
    while (new_data[0], new_data[1]) in bad_coordinates:
        new_data = game_parameters.get_random_bomb_data()
    return new_data


def check_snake_collisions(snake, apples, bomb, score_list):
    if snake.get_head() == bomb.get_location():
        return True
    if len(snake.get_coordinates()) != len(set(snake.get_coordinates())):
        return True
    if snake.get_head()[0] < 0 or snake.get_head()[0] >= game_parameters.WIDTH or snake.get_head()[1] < 0 or \
            snake.get_head()[1] >= game_parameters.HEIGHT:
        return True
    check = checking(snake.get_head(), [apple.get_location() for apple in apples])
    if check != -1:
        score_list[0] += apples[check].get_score()
        apples.remove(apples[check])
        snake.add_length(3)
    return False


def check_bomb_collisions(snake, apples, bomb, bomb_counter_list):
    if bomb_counter_list[0] > bomb.get_time() + bomb.get_radius() + 1:
        new_bomb_data = get_new_bomb_location([*snake.get_coordinates(), *[apple.get_location() for apple in apples]])
        bomb.change_data(*new_bomb_data)
        bomb_counter_list[0] = 1
    radius = bomb_counter_list[0] - (bomb.get_time() + 1)
    if len(set(snake.get_coordinates()).intersection(set(bomb.explosion(radius)))) > 0:
        return True
    apples_copy = apples[:]
    for apple in apples_copy:
        if apple.get_location() in bomb.explosion(radius):
            apples.remove(apple)
    return False


def complete_missing_apples(apples, bad_coordinates):
    # assuming bad_coordinates are all in the board, and there are no duplicates
    while len(apples) < 3 and len(bad_coordinates) < game_parameters.WIDTH * game_parameters.HEIGHT:
        new_apple_data = get_new_apple_location(bad_coordinates)
        new_apple = Apple((new_apple_data[0], new_apple_data[1]), new_apple_data[2])
        apples.append(new_apple)
        bad_coordinates.append(new_apple.get_location())


def get_occupied_locations(snake, apples, bomb, bomb_counter_list):
    radius = bomb_counter_list[0] - (bomb.get_time() + 1)
    occupied_dict = dict()
    snake_coordinates = snake.get_coordinates()
    apple_coordinates = [a.get_location() for a in apples]
    explosion_coordinates = bomb.explosion(radius)
    for coord in snake_coordinates:
        if coord[0] >= 0 and coord[0] < game_parameters.WIDTH and coord[1] >= 0 and coord[1] < game_parameters.HEIGHT:
            occupied_dict[coord] = "black"
    for coord in apple_coordinates:
        if coord[0] >= 0 and coord[0] < game_parameters.WIDTH and coord[1] >= 0 and coord[1] < game_parameters.HEIGHT:
            occupied_dict[coord] = "green"
    for coord in explosion_coordinates:
        if coord[0] >= 0 and coord[0] < game_parameters.WIDTH and coord[1] >= 0 and coord[1] < game_parameters.HEIGHT:
            if radius < 0:
                occupied_dict[coord] = "red"
            else:
                occupied_dict[coord] = "orange"
    return occupied_dict

def checkmoves(prevmove, nextmove):
    if prevmove == "Down" and nextmove == "Up":
        return False
    elif prevmove == "Left" and nextmove == "Right":
        return False
    elif prevmove == "Up" and nextmove == "Down":
        return False
    elif prevmove == "Right" and nextmove == "Left":
        return False
    else:return True

def main_loop(gd: GameDisplay) -> None:
    # _____________________________ INITIALIZING THE GAME ____________________________________________
    score = [0]
    bomb_count = [1]
    gd.show_score(score[0])
    x, y = (game_parameters.WIDTH // 2), (game_parameters.HEIGHT // 2)
    move = "Up"
    prevmove = "Up"
    game_snake, game_bomb, apple_lst = initial(gd)
    gd.end_round()
    end_game = False

    while not end_game:
        # ______________________________ INPUT FROM USER __________________________________________
        key_clicked = gd.get_key_clicked()
        prevmove = move
        if key_clicked is not None and checkmoves(prevmove, key_clicked):
            move = key_clicked

        # ______________________________ MOVING THE SNAKE __________________________________________
        snake_move(game_snake, move, prevmove)

        # ____________________________ CHECKING SNAKE COLLISIONS ___________________________________
        snake_collision = check_snake_collisions(game_snake, apple_lst, game_bomb, score)
        bomb_collision = check_bomb_collisions(game_snake, apple_lst, game_bomb, bomb_count)
        end_game = end_game or snake_collision or bomb_collision


        # ____________________________ INCREMENT ___________________________________
        bomb_count[0] += 1

        # ____________________________ CHECKING BOMB COLLISIONS ___________________________________
        bomb_collision = check_bomb_collisions(game_snake, apple_lst, game_bomb, bomb_count)
        end_game = end_game or bomb_collision


        # ____________________________ ADDING MISSING APPLES ___________________________________
        complete_missing_apples(apple_lst,
                                list(get_occupied_locations(game_snake, apple_lst, game_bomb, bomb_count).keys()))

        # ____________________________________ DRAW BOARD ___________________________________________
        occupied_locations = get_occupied_locations(game_snake, apple_lst, game_bomb, bomb_count)
        for coord in occupied_locations:
            gd.draw_cell(coord[0], coord[1], occupied_locations[coord])
        gd.show_score(score[0])

        # ____________________________________ GAME END ___________________________________________

        if len(occupied_locations) == game_parameters.WIDTH * game_parameters.HEIGHT:
            end_game = True

        # ____________________________________ END ROUND ___________________________________________
        gd.end_round()
