import random
from typing import Literal

from .data_hdlr import load_stats, save_stats, repair_game, DEFAULT_STATS

GAME_CHOICE = Literal["Rock", "Paper", "Scissors"]

def main_menu() -> Literal["1", "2", "3", "4", "5"]:
    """Displays the main menu of the game."""
    while True:
        user_input = input("\n"
                       "Choose an Option\n"
                       "\n"
                       "[1] Play a Game\n"
                       "[2] View Stats\n"
                       "[3] Reset Stats\n"
                       "[4] Repair Game\n"
                       "[5] Exit\n")
        
        if user_input == "1":
            while True:
                user_choice = input("\n"
                                    "Enter an option( Rock, Paper or Scissors ): ").capitalize()
                ai_choice = random.choice(["Rock", "Paper", "Scissors"])
                
                if user_choice in ["Rock", "Paper", "Scissors"]:
                    compute_and_display_result(user_choice, ai_choice)
                    play_again = input("\n"
                                       "Do you want to play again? Y[Yes] or N[No]: ").capitalize()
                    if play_again in ["Y", "Yes"]:
                        continue
                    
                    elif play_again in ["N", "No"]:
                        main_menu()
                        
                    else:
                        print("\n"
                              "Invalid Input! Please try again.")
                    
                else:
                    print("\n"
                          "Invalid Input! Please try again.")
        
        elif user_input == "2":
            stats = load_stats()
            print("\n"
                  f"Wins: {stats["wins"]}\n"
                  f"Losses: {stats["losses"]}\n"
                  f"Ties: {stats["ties"]}\n"
                  f"Games Played: {stats["games_played"]}")
            input("\n"
                  "Press any key to continue...")
            main_menu()
        
        elif user_input == "3":
            save_stats(DEFAULT_STATS)
            print("\n"
                  "Your stats has been successfully reset!")
            input("\n"
                  "Press any key to continue...")
            main_menu()
        
        elif user_input == "4":
            repair_game()
        
        elif user_input == "5":
            print("\n"
                  "Shutting down..."
                  "\n")
            quit()
        
        else:
            print("\nInvalid Input! Please try again.")
            

def compute_and_display_result(user_choice: GAME_CHOICE, ai_choice: GAME_CHOICE) -> None:
    """Computes the winner of the game and displays the result."""
    
    stats = load_stats()
    
    if user_choice == "Rock" and ai_choice == "Paper":
        print("\n"
              f"You chose {user_choice}\n"
              f"AI chose {ai_choice}\n"
              "\n"
              "You Lost!")
        stats["losses"] += 1
        stats["games_played"] += 1
        save_stats(stats)
        
    elif user_choice == "Rock" and ai_choice == "Scissors":
        print("\n"
              f"You chose {user_choice}\n"
              f"AI chose {ai_choice}\n"
              "\n"
              "You Won!")
        stats["wins"] += 1
        stats["games_played"] += 1
        save_stats(stats)
        
    elif user_choice == "Paper" and ai_choice == "Rock":
        print("\n"
              f"You chose {user_choice}\n"
              f"AI chose {ai_choice}\n"
              "\n"
              "You Won!")
        stats["wins"] += 1
        stats["games_played"] += 1
        save_stats(stats)
        
    elif user_choice == "Paper" and ai_choice == "Scissors":
        print("\n"
              f"You chose {user_choice}\n"
              f"AI chose {ai_choice}\n"
              "\n"
              "You Lost!")
        stats["losses"] += 1
        stats["games_played"] += 1
        save_stats(stats)
        
    elif user_choice == "Scissors" and ai_choice == "Rock":
        print("\n"
              f"You chose {user_choice}\n"
              f"AI chose {ai_choice}\n"
              "\n"
              "You Lost!")
        stats["losses"] += 1
        stats["games_played"] += 1
        save_stats(stats)
        
    elif user_choice == "Scissors" and ai_choice == "Paper":
        print("\n"
              f"You chose {user_choice}\n"
              f"AI chose {ai_choice}\n"
              "\n"
              "You Won!")
        stats["wins"] += 1
        stats["games_played"] += 1
        save_stats(stats)
        
    else:
        print("\n"
              f"You chose {user_choice}\n"
              f"AI chose {ai_choice}\n"
              "\n"
              "It's a Tie!")
        stats["ties"] += 1
        stats["games_played"] += 1
        save_stats(stats)
            

def display_welcome_screen():
    print("\n"
          "-------------------------------------------")
    print("Welcome to the Rock, Paper & Scissors Game!")
    print("-------------------------------------------")

def main():
    display_welcome_screen()
    main_menu()