import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

data_list = []

fig, ax = plt.subplots()


def animate(i):
    with open("/home/maou/zephyrproject/zephyr/Final_Year_project_bio_potential/FYP_Project_code/Bio_potential recevier code/BLE_EMG_VALUE_lowered.txt",'r') as f:
        for line in f:
            data_list.append(int(line.strip()))
    ax.clear()
    ax.plot(data_list[-500:]) # plot the last 5 data points
    ax.set_ylim([-3000, 4500])
    ax.set_title("BLE EMG Value Reading lowered Plot")
    ax.set_ylabel("BLE EMG Value Reading")
    
# call the animation
ani = FuncAnimation(fig, animate, interval=50000)

# show the plot
plt.show()