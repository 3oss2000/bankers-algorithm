import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton
import numpy as np

def check(i):
    for j in range(no_r):
        if(needed[i][j]>available[j]):
            return False
    return True

def run_bankers_algorithm():
    global no_p, no_r, allocated, maximum, available, needed

    no_p = int(no_p_input.text())
    no_r = int(no_r_input.text())
    allocated_values = [int(x) for x in allocated_input.text().split()]
    maximum_values = [int(x) for x in maximum_input.text().split()]
    available_values = [int(x) for x in available_input.text().split()]

    allocated = np.array(allocated_values).reshape(no_p, no_r)
    maximum = np.array(maximum_values).reshape(no_p, no_r)
    needed = maximum - allocated
    available = np.array(available_values)

    Sequence = np.zeros((no_p,),dtype=int)
    visited = np.zeros((no_p,),dtype=int)
    waiting = np.zeros((no_p,),dtype=int)
    count = 0

    while count < no_p:
        temp = False
        for i in range(no_p):
            if visited[i] == 0:
                if check(i):
                    Sequence[count] = i
                    count += 1
                    visited[i] = 1
                    temp = True
                    for j in range(no_r):
                        available[j] += allocated[i][j]
        if not temp:
            # deadlock detected
            output_label.setText('The system is unsafe\nDeadlock detected. The following processes are waiting for resources:\n' + '\n'.join(['Process ' + str(i) for i in range(no_p) if waiting[i] == 1]))
            break

    if count == no_p:
        output_label.setText('The system is safe\nSafe sequence: ' + str(Sequence) + '\nAvailable resources: ' + str(available))

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle('Banker\'s Algorithm')

no_p_label = QLabel('Number of processes:')
no_p_input = QLineEdit()
no_r_label = QLabel('Number of resources:')
no_r_input = QLineEdit()
allocated_label = QLabel('Allocated resources (space-separated):')
allocated_input = QLineEdit()
maximum_label = QLabel('Maximum resources (space-separated):')
maximum_input = QLineEdit()
available_label = QLabel('Available resources (space-separated):')
available_input = QLineEdit()

run_button = QPushButton('Run Banker\'s Algorithm')
run_button.clicked.connect(run_bankers_algorithm)

output_label = QLabel()
output_label.setText('Output will appear here')

inputs_layout = QVBoxLayout()
inputs_layout.addWidget(no_p_label)
inputs_layout.addWidget(no_p_input)
inputs_layout.addWidget(no_r_label)
inputs_layout.addWidget(no_r_input)
inputs_layout.addWidget(allocated_label)
inputs_layout.addWidget(allocated_input)
inputs_layout.addWidget(maximum_label)
inputs_layout.addWidget(maximum_input)
inputs_layout.addWidget(available_label)
inputs_layout.addWidget(available_input)

output_layout = QVBoxLayout()
output_layout.addWidget(output_label)

buttons_layout = QHBoxLayout()
buttons_layout.addWidget(run_button)

layout = QVBoxLayout()
layout.addLayout(inputs_layout)
layout.addLayout(buttons_layout)
layout.addLayout(output_layout)
window.setLayout(layout)

window.show()
sys.exit(app.exec_())