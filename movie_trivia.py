import customtkinter
import random

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("1280x720")

list_of_questions = []
question_index = 0
question_count = 1
correct_answer_count = 0
final_grade = 0.0

def show_leaderboard():
    clear_previous_widgets(root)

    list_of_player_grade_dictionaries = []

    leaderboard = customtkinter.CTkScrollableFrame(root)

    def render_leaderboard():
        leaderboard.pack(pady=20, padx=60, fill="both", expand=True)
    
    root.after(500, render_leaderboard)

    leaderboard_header = customtkinter.CTkLabel(master=root, text="Leaderboard", font=("Roboto", 64))
    leaderboard_header.pack(side="top")

    with open("leaderboard.txt", "r") as file:
    # Read lines and convert each line into a dictionary, then append them to our list
        list_of_player_grade_dictionaries = [eval(line.strip()) for line in file]
    
    print(list_of_player_grade_dictionaries)
    
    for i, player in enumerate(list_of_player_grade_dictionaries):
        player_name = customtkinter.CTkLabel(leaderboard, text=player["name"], font=("Roboto", 32))
        player_name.grid(row=i, column=0, padx=10, pady=5, sticky="w")

        player_grade = customtkinter.CTkLabel(leaderboard, text=player["grade"], font=("Roboto", 32))
        player_grade.grid(row=i, column=1, padx=10, pady=5, sticky="w")

def handle_grade():
    name = name_input.get()
    player_dictionary = {
        "name": name,
        "grade": final_grade
    }

    leaderboard_file = open("leaderboard.txt", "a+")
    leaderboard_file.write(str(player_dictionary))

    print(player_dictionary)

def end_game():
    global final_grade
    final_grade = (correct_answer_count / 10) * 100

    end_game_header_text = customtkinter.CTkLabel(master=game, text="Game Over!", font=("Roboto", 128))
    end_game_header_text.pack(pady=200)

    submit_grade_button = customtkinter.CTkButton(master=game, font=("Roboto", 32), text="Submit Grade", command=handle_grade)
    submit_grade_button.pack(side="bottom")

    global name_input
    name_input = customtkinter.CTkEntry(master=game, font=("Roboto", 32), placeholder_text="Input your name please.", width=400)
    name_input.pack(side="bottom")

    ending_grade_frame = customtkinter.CTkFrame(master=game)
    ending_grade_frame.pack(side="bottom")
    your_grade_text = customtkinter.CTkLabel(master=ending_grade_frame, text="Grade: ", font=("Roboto", 48))
    your_grade_text.pack(side="left")
    your_ending_grade = customtkinter.CTkLabel(master=ending_grade_frame, text=final_grade, font=("Roboto", 48))
    your_ending_grade.pack(side="left")
    percentage_label = customtkinter.CTkLabel(master=ending_grade_frame, text="%", font=("Roboto", 48))
    percentage_label.pack(side="left")

def evaluate_answer(answer):
    print(answer)
    global question_count
    global question_index
    global correct_answer_count

    correct_text = customtkinter.CTkLabel(master=game, text="Correct!!!", font=("Roboto", 32), text_color="green")
    incorrect_text = customtkinter.CTkLabel(master=game, text="Incorrect!!!", font=("Roboto", 32), text_color="red")

    if ":" in answer:
        correct_answer_count += 1
        correct_text.pack(side="bottom")
    else:
        incorrect_text.pack(side="bottom")
    
    question_count += 1
    question_index += 1

    disable_buttons(button_frame)
    game.after(1000, clear_previous_widgets, game)

    #CHANGE TO 10 AFTER TESTING IS DONE
    if question_index == 1:
        game.after(1000, end_game)
    else:
        game.after(1000, display_question)



def get_questions():
    global list_of_questions

    with open("questions.txt", "r") as file:
    # Read lines and convert each line into a dictionary, then append them to our list
        list_of_questions = [eval(line.strip()) for line in file]
    
    random.shuffle(list_of_questions)

def render_buttons(frame):
    list_of_answers = list_of_questions[question_index]["answers"].split(",")

    random.shuffle(list_of_answers)

    print(list_of_answers)

    for answer in list_of_answers:
        if ":" in answer:
            button = customtkinter.CTkButton(master=frame, text=answer[:-1], font=("Roboto", 16), command=lambda a=answer: evaluate_answer(a))
            button.pack(pady=20)
            continue
        
        button = customtkinter.CTkButton(master=frame, text=answer, font=("Roboto", 16), command=lambda a=answer: evaluate_answer(a))
        button.pack(pady=20)

def display_question():
    # Destroy the "Start!" text and display the question
    start_game_text.destroy()

    score_frame = customtkinter.CTkFrame(game)
    score_frame.pack(side="bottom")
    question_count_label = customtkinter.CTkLabel(score_frame, text="Question ", font=("Roboto", 48))
    question_count_label.pack(side="left")
    current_question_number = customtkinter.CTkLabel(score_frame, text=question_count, font=("Roboto", 48))
    current_question_number.pack(side="left")
    maximum_question_count_label = customtkinter.CTkLabel(score_frame, text="/10", font=("Roboto", 48))
    maximum_question_count_label.pack(side="left")

    question_text = customtkinter.CTkLabel(master=game, text=list_of_questions[question_index]["question"], font=("Roboto", 32))
    question_text.pack(pady=15, padx=15)

    global button_frame
    button_frame = customtkinter.CTkFrame(master=game)
    button_frame.pack(pady=20)
    render_buttons(button_frame)

def start_game():
    start_menu.destroy()

    global game
    game = customtkinter.CTkFrame(master=root)
    game.pack(pady=20, padx=60, fill="both", expand=True)

    global start_game_text  # Declare as global to access in `display_question`
    start_game_text = customtkinter.CTkLabel(master=game, text="Start!", font=("Roboto", 128))
    start_game_text.pack(pady=200, padx=200)

    get_questions()

    # Schedule the question to appear after 1 second
    root.after(1000, display_question)

def clear_previous_widgets(frame):
    # Loop through all the children and destroy them
    for widget in frame.winfo_children():
        widget.destroy()

def disable_buttons(frame):
    for button in frame.winfo_children():
        if isinstance(button, customtkinter.CTkButton):
            button.configure(state="disabled")

start_menu = customtkinter.CTkFrame(master=root)
start_menu.pack(pady=20, padx=60, fill="both", expand=True)

title_screen_header = customtkinter.CTkLabel(master=start_menu, text="Movie Trivia", font=("Roboto", 128))
title_screen_header.pack(pady=12, padx=10)

play_button = customtkinter.CTkButton(master=start_menu, text="Play!", font=("Roboto", 64), command=start_game, width=600)
play_button.pack(pady=12, padx=10)

leadeboard_button = customtkinter.CTkButton(master=start_menu, text="Leaderboard", font=("Roboto", 64), command=show_leaderboard, width=600)
leadeboard_button.pack(pady=12, padx=10)

root.mainloop()
