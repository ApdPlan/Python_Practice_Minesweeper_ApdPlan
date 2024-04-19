#!/usr/bin/env python3

from random import randint
from re import search
from re import IGNORECASE

invisible_spaces_list = [" "] * 100
player_visible_spaces_list = ["+"] * 100
visible_spaces_string = ""
list_of_mines = [""] * 10
early_end = [False]
player_input = ''
mine_markers_list = [""] * 10 
spread_verification = set()


def create_player_grid(visible_spaces_string, game_continues):
    i = 0
    visible_spaces_string = ""
    while i < 100:
        if (i == 0):
            visible_spaces_string += "  0 1 2 3 4 5 6 7 8 9 \n0|"
        elif ((i % 10) == 0):
            visible_spaces_string += "\n" + str(int(i/10)) + "|"
        if (game_continues == True):
            visible_spaces_string += str(player_visible_spaces_list[i]) + "|"
        else:
            visible_spaces_string += str(invisible_spaces_list[i]) + "|"
        i += 1
    return(visible_spaces_string)


def print_grid(visible_spaces_string, game_continues):
    visible_spaces_string = create_player_grid(visible_spaces_string, game_continues)
    print(visible_spaces_string)


def spreading_search(players_chosen_location, spread_verification ):
    spread_surrounding_spots = (-10, -1, 1, 10)
    for i in spread_surrounding_spots:
        if (players_chosen_location + i) in spread_verification:
            pass
        else:
            if (players_chosen_location + i) >= 0 and (players_chosen_location + i) <= 99 :
                if ((players_chosen_location+10)%10 == 0 and i == -1):
                    pass
                elif ((players_chosen_location+10)%10 == 9 and i == 1):
                    pass
                elif invisible_spaces_list[players_chosen_location + i] == " ":
                    spread_verification.add(players_chosen_location + i)
                    spreading_search(players_chosen_location+i, spread_verification)
                else:
                    spread_verification.add(players_chosen_location + i)


def marking_mine(marked_mines, game_continues, players_chosen_location):
        print("marking mine")
        m = search('\d\d', players_chosen_location)
        m_after_int = int(m.group())
        if(player_visible_spaces_list[int(m.group())] == "m"):
            marked_mines -= 1
            player_visible_spaces_list[int(m.group())] = "+"
            mine_markers_list.remove(m_after_int)
        elif(player_visible_spaces_list[int(m.group())] == "+"):
            marked_mines += 1
            player_visible_spaces_list[int(m.group())] = "m"
            mine_markers_list.append(m_after_int)
        print_grid(visible_spaces_string, game_continues)
        return(marked_mines)


def location_search(game_continues, players_chosen_location):
        players_chosen_location = int(players_chosen_location)
        if player_visible_spaces_list[int(players_chosen_location)] == "m" :
            print("Marked spaces cannot be searched.")
            return(game_continues)
        if invisible_spaces_list[int(players_chosen_location)] == "*" :
            early_end[0] = True
            game_continues = False
        elif invisible_spaces_list[players_chosen_location] == " " :
            spread_verification.add(players_chosen_location)
            spreading_search(players_chosen_location, spread_verification)
            player_visible_spaces_list[int(players_chosen_location)] = \
                    invisible_spaces_list[int(players_chosen_location)]
            for i in spread_verification:
                player_visible_spaces_list[i] = invisible_spaces_list[i]
            print_grid(visible_spaces_string, game_continues)
        elif invisible_spaces_list[int(players_chosen_location)] > 0 :
            player_visible_spaces_list[int(players_chosen_location)] = \
                    invisible_spaces_list[int(players_chosen_location)]
            print_grid(visible_spaces_string, game_continues)
        return(game_continues)


def main_game_loop():
    game_continues = True
    #This section adds mines to the invisible grid & create a list of mine positions
    mines = 0
    while (mines < 10):
        mine_position = randint(0 , 99)
        if invisible_spaces_list[mine_position] == "*" :
            pass
        else:
            invisible_spaces_list[mine_position] = "*"
            list_of_mines[mines] = mine_position
            mines += 1
    #This section sets up initial text for first start of the game
    print_grid(visible_spaces_string, game_continues)
    print("10 mines have been placed. Try to mark them without setting them off")
    print("Search an area to gather info on the surrounding spaces")
    print("(Warning: searching an area that contains a mine will lead to a game over)")    
    #Set the number of mines for each space near a mine
    i = 0
    while (i < 10):
        current_position = list_of_mines[i]
        n = 0
        mine_surroundings_check = (-11, -10, -9, -1, 1, 9, 10, 11)
        for n in mine_surroundings_check:
            if ((current_position + n) <= 99 and (current_position + n) >= 0):
                if((list_of_mines[i]+10)%10 == 0 and (n == -1 or n == -11 or n == 9) ):
                    pass
                elif((list_of_mines[i]+10)%10 == 9 and (n == 1 or n == -9 or n == 11) ):
                    pass
                elif ((invisible_spaces_list[current_position + n]  == " ")):
                   invisible_spaces_list[current_position + n] = 1
                elif (invisible_spaces_list[current_position + n]  == "*"):
                   pass
                else:
                   copy_var = int(invisible_spaces_list[current_position + n])
                   copy_var += 1
                   invisible_spaces_list[current_position + n] = copy_var
        i += 1
    set_comparison = gameplay_loop()
    return(set_comparison)


def gameplay_loop():
    game_continues = True
    marked_mines = 0 #int, number of mines that have been marked by player
    while (game_continues):
        players_chosen_location = input("Enter the row number followed by the \
                                        column number to search that location. \
                                        Add an m in front to mark a mine: ")  
        if (bool(search('\d\d\d', players_chosen_location)) == True):
            print("could not recognize input, please try again")
            continue
        if (bool(search('\D\D', players_chosen_location)) == True):
            print("could not recognize input, please try again")
            continue
        if ((bool(search('\D', players_chosen_location)) == True) and \
                    (bool(search(r'm', players_chosen_location, IGNORECASE)) == False)):
            print("could not recognize input, please try again")
            continue
        if(players_chosen_location.find("m") > -1 or \
                   players_chosen_location.find("M") > -1):
            if ((bool(search('\d', players_chosen_location)) == False)):
                print("could not recognize input, please try again")
                continue
            else:
                marked_mines = marking_mine(marked_mines, game_continues, players_chosen_location)
        else:
            game_continues = location_search(game_continues, players_chosen_location)
        if(marked_mines >= 10):
            print("10 mines have been marked. Do you want to end the game? If \
                  any mines are marked incorrectly the player will lose.")
            player_input = input("Enter 'y' to end the game. Enter a space \
                                 number to remove that marker.")
            if(player_input == 'y'):
                print("End of the game")
                a = set(mine_markers_list)
                a.remove("")
                b = set(list_of_mines)
                set_comparison = a.union(b)
                game_continues = False
                return(set_comparison)
                break
            else:
                marked_mines -= 1
                player_visible_spaces_list[int(player_input)] = "+"
                print_grid(visible_spaces_string, game_continues)


application_running = True
while (application_running):    
    set_comparison = main_game_loop()
    if (early_end[0] == False):
        if (len(set_comparison) > 10):
            print("\n You lost,Game over")
            game_continues = False
            print_grid(visible_spaces_string, game_continues)
        else:
            print("\n You win")
    else:
        print("\n You lost,Game over")
        game_continues = False
        print_grid(visible_spaces_string, game_continues)
    player_input = input("Do you wish to continue? y/n?: ")
    while(True): 
        if (player_input.find("y") > -1):
            print("Starting a new game")
            application_running = True
            list_of_mines.clear()
            list_of_mines = [""] * 10
            player_visible_spaces_list.clear()
            player_visible_spaces_list = ["+"] * 100
            invisible_spaces_list.clear()
            invisible_spaces_list = [" "] * 100
            spread_verification.clear()
            break
        elif(player_input.find("n") > -1):
            print("Ending program")
            application_running = False
            break
        else:
            print("Input not unerstood. Please try again.")


#Notes
#mines have been previously confirmed at 0 and 99
