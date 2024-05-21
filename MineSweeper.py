#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import randint
from re import search
from re import IGNORECASE


class Board():
    def  __init__(self):
        self.invisible_spaces_list = [" "] * 100
        self.player_visible_spaces_list = ["+"] * 100
        self.list_of_mines = [""] * 10
        self.visible_spaces_string = ""
        self.early_end = [False]
        self.mine_markers_list = [""] * 10 
        self.spread_verification = set()


def create_player_grid(field, game_continues):
    i = 0
    field.visible_spaces_string = ""
    while i < 100:
        if (i == 0):
            field.visible_spaces_string += "  0 1 2 3 4 5 6 7 8 9 \n0|"
        elif ((i % 10) == 0):
            field.visible_spaces_string += "\n" + str(int(i/10)) + "|"
        if (game_continues == True):
            field.visible_spaces_string += str(field.player_visible_spaces_list[i]) + "|"
        else:
            field.visible_spaces_string += str(field.invisible_spaces_list[i]) + "|"
        i += 1
    return  (field.visible_spaces_string)


def print_grid(field, game_continues):
    field.visible_spaces_string = create_player_grid(field, game_continues)
    print(field.visible_spaces_string)


def spreading_search(field, players_chosen_location  ):
    spread_surrounding_spots = (-10, -1, 1, 10)
    for i in spread_surrounding_spots:
        if (players_chosen_location + i) in field.spread_verification:
            pass
        else:
            if (players_chosen_location + i) >= 0 and (players_chosen_location + i) <= 99 :
                if ((players_chosen_location+10)%10 == 0 and i == -1):
                    pass
                elif ((players_chosen_location+10)%10 == 9 and i == 1):
                    pass
                elif field.invisible_spaces_list[players_chosen_location + i] == " ":
                    field.spread_verification.add(players_chosen_location + i)
                    spreading_search(field, players_chosen_location+i)
                else:
                    field.spread_verification.add(players_chosen_location + i)


def marking_mine(field, marked_mines, game_continues, players_chosen_location):
        print("marking mine")
        m = search('\d\d', players_chosen_location)
        m_after_int = int(m.group())
        if(field.player_visible_spaces_list[int(m.group())] == "m"):
            marked_mines -= 1
            field.player_visible_spaces_list[int(m.group())] = "+"
            field.mine_markers_list.remove(m_after_int)
        elif(field.player_visible_spaces_list[int(m.group())] == "+"):
            marked_mines += 1
            field.player_visible_spaces_list[int(m.group())] = "m"
            field.mine_markers_list.append(m_after_int)
        print_grid(field, game_continues)
        return(marked_mines)


def location_search(field, game_continues, players_chosen_location):
        players_chosen_location = int(players_chosen_location)
        if field.player_visible_spaces_list[int(players_chosen_location)] == "m" :
            print("Marked spaces cannot be searched.")
            return(game_continues)
        if field.invisible_spaces_list[int(players_chosen_location)] == "*" :
            field.early_end[0] = True
            game_continues = False
        elif field.invisible_spaces_list[players_chosen_location] == " " :
            field.spread_verification.add(players_chosen_location)
            spreading_search(field, players_chosen_location)
            field.player_visible_spaces_list[int(players_chosen_location)] = \
                    field.invisible_spaces_list[int(players_chosen_location)]
            for i in field.spread_verification:
                field.player_visible_spaces_list[i] = field.invisible_spaces_list[i]
            print_grid(field, game_continues)
        elif field.invisible_spaces_list[int(players_chosen_location)] > 0 :
            field.player_visible_spaces_list[int(players_chosen_location)] = \
                    field.invisible_spaces_list[int(players_chosen_location)]
            print_grid(field, game_continues)
        return(game_continues)


def main_game_loop(field):
    game_continues = True
    #This section adds mines to the invisible grid & create a list of mine positions
    mines = 0
    while (mines < 10):
        mine_position = randint(0 , 99)
        if field.invisible_spaces_list[mine_position] == "*" :
            pass
        else:
            field.invisible_spaces_list[mine_position] = "*"
            field.list_of_mines[mines] = mine_position
            mines += 1
    #This section sets up initial text for first start of the game
    print_grid(field, game_continues)
    print("10 mines have been placed. Try to mark them without setting them off")
    print("Search an area to gather info on the surrounding spaces")
    print("(Warning: searching an area that contains a mine will lead to a game over)")    
    #Set the number of mines for each space near a mine
    i = 0
    while (i < 10):
        current_position = field.list_of_mines[i]
        n = 0
        mine_surroundings_check = (-11, -10, -9, -1, 1, 9, 10, 11)
        for n in mine_surroundings_check:
            if ((current_position + n) <= 99 and (current_position + n) >= 0):
                if((field.list_of_mines[i]+10)%10 == 0 and (n == -1 or n == -11 or n == 9) ):
                    pass
                elif((field.list_of_mines[i]+10)%10 == 9 and (n == 1 or n == -9 or n == 11) ):
                    pass
                elif ((field.invisible_spaces_list[current_position + n]  == " ")):
                   field.invisible_spaces_list[current_position + n] = 1
                elif (field.invisible_spaces_list[current_position + n]  == "*"):
                   pass
                else:
                   copy_var = int(field.invisible_spaces_list[current_position + n])
                   copy_var += 1
                   field.invisible_spaces_list[current_position + n] = copy_var
        i += 1
    set_comparison = gameplay_loop(field)
    return(set_comparison)


def gameplay_loop(field):
    player_input = ''
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
                marked_mines = marking_mine(field, marked_mines, game_continues, players_chosen_location)
        else:
            game_continues = location_search(field, game_continues, players_chosen_location)
        if(marked_mines >= 10):
            print("10 mines have been marked. Do you want to end the game? If \
                  any mines are marked incorrectly the player will lose.")
            player_input = input("Enter 'y' to end the game. Enter a space \
                                 number to remove that marker.")
            if(player_input == 'y'):
                print("End of the game")
                a = set(field.mine_markers_list)
                a.remove("")
                b = set(field.list_of_mines)
                set_comparison = a.union(b)
                game_continues = False
                return(set_comparison)
                break
            else:
                marked_mines -= 1
                field.player_visible_spaces_list[int(player_input)] = "+"
                print_grid(field, game_continues)


def main():
    player_input = ''
    field = Board()
    application_running = True
    while (application_running):    
        set_comparison = main_game_loop(field)
        if (field.early_end[0] == False):
            if (len(set_comparison) > 10):
                print("\n You lost,Game over")
                game_continues = False
                print_grid(field, game_continues)
            else:
                print("\n You win")
        else:
            print("\n You lost,Game over")
            game_continues = False
            print_grid(field, game_continues)
        player_input = input("Do you wish to continue? y/n?: ")
        while(True): 
            if (player_input.find("y") > -1):
                print("Starting a new game")
                application_running = True
                field.list_of_mines.clear()
                field.list_of_mines = [""] * 10
                field.player_visible_spaces_list.clear()
                field.player_visible_spaces_list = ["+"] * 100
                field.invisible_spaces_list.clear()
                field.invisible_spaces_list = [" "] * 100
                field.spread_verification.clear()
                break
            elif(player_input.find("n") > -1):
                print("Ending program")
                application_running = False
                break
            else:
                print("Input not unerstood. Please try again.")


main()


#Notes
#mines have been previously confirmed at 0 and 99