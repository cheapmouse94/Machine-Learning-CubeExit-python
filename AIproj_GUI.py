from tkinter import *

global penalty_test, life_penalty_test
class GUI:
    def __init__(self):
        top = Tk()    
        top.title('Reinforcement Learining with Python - by Grzegorz Jakimiuk')
        HEIGHT = 400
        WIDTH = 410

        top.resizable(width=False, height=False)

        canvas = Canvas(top, height=HEIGHT, width=WIDTH)
        canvas.pack()

        gamma_input_area = Entry(top, width = 30)
        gamma_input_area.place(x = 110, y = 80)   
        reward_input_area = Entry(top, width = 30)
        reward_input_area.place(x = 110, y = 120)   
        penalty_input_area = Entry(top, width = 30)
        penalty_input_area.place(x = 110, y = 160) 
        life_penalty_input_area = Entry(top, width=30)
        life_penalty_input_area.place(x = 110, y=200)
        iteration_input_area = Entry(top, width = 30)
        iteration_input_area.place(x = 110, y = 240)

        def gamma_is_float_error():
            try:  
                gamma_test = float(gamma_input_area.get())
                gamma_error_display['text'] = ''
                if gamma_test >= 0 and gamma_test <= 1:
                    return gamma_test
                else:
                    gamma_error_display['text'] = 'The value is not in required range'
                    return False
            except:
                gamma_error_display['text'] = 'Please insert correct value'
                gamma_input_area.delete(0, END)
                print('Wrong value of Gamma')
                return False

        def reward_is_float_error():
            try:
                reward_test = float(reward_input_area.get())
                reward_error_display['text'] = ''
                if reward_test >= 0 and reward_test <= 10000:
                    return reward_test
                else:
                    reward_error_display['text'] = 'The value is not in required range'
                    return False
            except:
                reward_error_display['text'] = 'Please insert correct value'
                reward_input_area.delete(0, END)
                print('Wrong value of Reward')
                return False

        def penalty_is_float_error():
            try:
                penalty_test = float(penalty_input_area.get())
                penalty_error_display['text'] = ''
                if penalty_test >= 0 and penalty_test <= 10000:
                    return penalty_test

                else:
                    penalty_error_display['text'] = 'The value is not in required range'
                    return False
            except:
                penalty_error_display['text'] = 'Please insert correct value'
                penalty_input_area.delete(0, END)
                print('Wrong value of Penalty')
                return False

        def iteration_is_int_error():
            try:
                iteration_test = int(iteration_input_area.get())
                iteration_error_display['text'] = ''
                if iteration_test >= 1000 and iteration_test <= 50000:
                    return iteration_test
                elif type(iteration_test) is float:
                    iteration_error_display['text'] = 'Change value from float to int'
                    return False
                else:
                    iteration_error_display['text'] = 'The value is not in required range'
                    return False
            except:
                iteration_error_display['text'] = 'Please insert correct value'
                iteration_input_area.delete(0, END)
                print('Wrong value of Iteration')
                return False    

        def life_penalty_is_int_error():
            try:
                life_penalty_test = int(life_penalty_input_area.get())
                life_penalty_error_display['text'] = ''
                if life_penalty_test >= 0 and life_penalty_test <= 100:
                    return life_penalty_test
                elif type(life_penalty_test) is float:
                    life_penalty_error_display['text'] = 'Change value from float to int'
                    return False
                else:
                    life_penalty_error_display['text'] = 'The value is not in required range'
                    return False
            except:
                life_penalty_error_display['text'] = 'Please insert correct value'
                life_penalty_input_area.delete(0, END)
                print('Wrong value of Iteration')
                return False              

        def execute():
            global gamma_value, reward_value, penalty_value, iteration_value, life_penalty_value, destiny, VFR
            gamma_value = gamma_is_float_error()
            reward_value = reward_is_float_error()
            penalty_value = penalty_is_float_error()
            iteration_value = iteration_is_int_error()
            life_penalty_value = life_penalty_is_int_error()
            VFR = var_fast_result.get()
            if gamma_value is not False and reward_value is not False and penalty_value is not False and iteration_value is not False and life_penalty_value is not False:
                destiny = True
                if gamma_value == 1.0:
                    gamma_value = int(gamma_value)
                reward_value = int(reward_value)
                penalty_value = int(penalty_value)
                print(gamma_value, reward_value, penalty_value, iteration_value, life_penalty_value)
                top.destroy()
            else:
                print('Check again inserted values')
                destiny = False

        def information():

            popup_win = Tk()
            popup_win.wm_title('Read me - Polish')

            popup_win.resizable(width=False, height=False)
            HEIGHT_p = 500
            WIDTH_p = 600

            canvas_p = Canvas(popup_win, height=HEIGHT_p, width=WIDTH_p)
            canvas_p.pack()

            label_pop = Label(popup_win, width=75, wraplength=500, text = "Istotą projektu jest stworzenie sztucznej inteligencji, która w opaciu o algorytmy jest w stanie wykonać dane zadanie. Jednakże przy wykorzystaniu wiedzy z zakresu nauczania maszynowego, dany agent jest w stanie wykoać zadanie efektywniej po przez proces iteracyjnego uzupełniania bazy danych. Na potrzeby projektu wykorzystano model nauczania po przez wzmocnienie (eng. Reinforcement Learning), który polega na aktualizowaniu bazy danych na podstawie wykonywania akcji przez agenta: zasada nagradzania oraz karania. Finalnym procesem nauczania agenta jest wtedy, gdy parametry w bazie danych zmieniają się w minimalny sposób. W głównym oknie są ukazanie wstępne parametry charakteryzujące się tym w jaki sposób będzie agent się uczyć w oparciu o równianie Bellmana:\n\nReward - nagroda za wykonanie dobrze zadania\nPenalty - kara za złe wykonanie zadania\nGamma - współczynnik, który opisuje jak szybko uczy się algorytm\nLife Penalty - `Wieczna kara` dowolny ruch agenta kończy się karą\nIteration - określona liczba ruchów wykanych przez agenta", font=('Arial', 10), justify='left')
            label_pop.place(x = 0, y = 10)


        main_title = Label(top,  text = "Machine Learning with Python", font=('Arial', 12))
        main_title.place(x = 70, y = 20)
        describe = Label(top,  text = "Insert correct values and press the button")
        describe.place(x = 60, y = 50) 
        credit = Label(top,  text = "© 2020 Grzegorz Jakimiuk. All Rights Reserved. version 1.0", font=('Arial', 9))
        credit.place(x = 80, y = 385)   
        gamma = Label(top,  text = "Gamma")
        gamma.place(x = 40, y = 80)
        gamma_d = Label(top, text='(from 0 to 1)')
        gamma_d.place(x=300, y=80) 
        gamma_error_display = Label(top, text='', font=('Arial', 8), fg='red')
        gamma_error_display.place(x = 40, y = 100)  
        reward = Label(top,  text = "Reward")
        reward.place(x = 40, y = 120)
        reward_d = Label(top, text='(from 0 to 10000)')
        reward_d.place(x = 300, y=120)
        reward_error_display = Label(top, text='', font=('Arial', 8), fg='red')
        reward_error_display.place(x = 40, y = 140)  
        penalty = Label(top,  text = "Penalty")
        penalty.place(x = 40, y = 160) 
        penalty_d = Label(top, text='(from 0 to 10000)')
        penalty_d.place(x = 300, y = 160)
        penalty_error_display = Label(top, text='', font=('Arial', 8), fg='red')
        penalty_error_display.place(x = 40, y = 180)  

        life_penalty = Label(top,  text = "Life Penalty")
        life_penalty.place(x = 40, y = 200) 
        life_penalty_d = Label(top, text='(from 0 to 100)')
        life_penalty_d.place(x = 300, y = 200)
        life_penalty_error_display = Label(top, text='', font=('Arial', 8), fg='red')
        life_penalty_error_display.place(x = 40, y = 220)  

        iteration = Label(top, text='Iteration')
        iteration.place(x = 40, y = 240)
        iteration_d = Label(top, text='(from 1000 to 50000)')
        iteration_d.place(x = 300, y = 240)
        iteration_error_display = Label(top, text='', font=('Arial', 8), fg='red')
        iteration_error_display.place(x = 40, y = 260) 

        var_fast_result = IntVar()
        checkbutton_fast_result = Checkbutton(top, text='Fast calculation', variable=var_fast_result, state=DISABLED)
        checkbutton_fast_result.place(x = 40, y=350)
            
        submit_button = Button(top,  text = "Execute!", command=execute)
        submit_button.place(x = 170, y = 350) 

        info_button = Button(top, width=15 , text = "Read me - Polish", command=information)
        info_button.place(x = 250, y = 350) 

        top.mainloop()  
