import matplotlib.pyplot as plt
import xlwt
axis_x = []
axis_y_1 = []
axis_y_2 = []
d_score_neg = 0
d_score_pos = 0
efficiency = []

class Plot:
    def __init__(self, Q_VALUE, SCORE_POSITIVE, SCORE_NEGATIVE, iteration, MAX_ITERATIONS, MOVES_COUNT_TOTAL):
        global axis_x, axis_y_1, axis_y_2, efficiency
        self.iteration_x = iteration
        self.score_positive_y = SCORE_POSITIVE
        self.score_negative_y = SCORE_NEGATIVE

        if len(MOVES_COUNT_TOTAL) == 0:
            efficiency.append(0)
        else:
            avg = sum(MOVES_COUNT_TOTAL)/len(MOVES_COUNT_TOTAL)
            ep = (min(MOVES_COUNT_TOTAL)/avg)*100

            efficiency.append(ep)

        axis_x.append(self.iteration_x)
        axis_y_1.append(SCORE_NEGATIVE)
        axis_y_2.append(SCORE_POSITIVE)
        if self.iteration_x == MAX_ITERATIONS:
            self.draw_plots()
    def draw_plots(self):
        
        self.excelexport()

        fig, axs = plt.subplots(2)
        fig.suptitle('Machine Learning Results')
        axs[0].plot(axis_x, axis_y_1)
        axs[0].plot(axis_x, axis_y_2)
        axs[1].plot(axis_x, efficiency)

        axs[0].set(xlabel = 'Iterations', ylabel='Penalties / Rewards')
        axs[1].set(xlabel = 'Iterations', ylabel='Efficiency (%)')
        plt.show()

    def excelexport(self):

        self.book = xlwt.Workbook(encoding="utf-8")
        sheet_1 = self.book.add_sheet('Sheet 1')

        sheet_1.write(0, 0, 'Iterations')
        sheet_1.write(0, 1, 'Efficiency')
        sheet_1.write(0, 2, 'Penalties')
        sheet_1.write(0, 3, 'Rewards')

        self.i = 1
        for n in axis_x:
            self.i += 1
            sheet_1.write(self.i, 0, n)
        self.i = 1
        for n in efficiency:
            self.i += 1
            sheet_1.write(self.i, 1, n)
        self.i = 1
        for n in axis_y_1:
            self.i += 1
            sheet_1.write(self.i, 2, n)
        self.i = 1
        for n in axis_y_2:
            self.i += 1
            sheet_1.write(self.i, 3, n)

        self.book.save('AI_RESULTS.xls')
        

        


