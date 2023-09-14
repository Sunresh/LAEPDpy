import nidaqmx
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import tkinter as tk

dev = "dev3/" #"SimDev1/"
digital = "dev3/port0/line0" #"SimDev1/port0/line0"

def analogout(v, d):
    with nidaqmx.Task() as task:
        task.ao_channels.add_ao_voltage_chan(d, name_to_assign_to_channel="ao_channel", min_val=0.0, max_val=5.0)
        task.write(v)

def analogoutuu(d):
    with nidaqmx.Task() as task:
        task.ao_channels.add_ao_voltage_chan(d, name_to_assign_to_channel="ao_channel", min_val=0.0, max_val=5.0)
        bb = task.read()
    return bb
        
def decrease(pzt_port):
    with nidaqmx.Task() as task:
        task.ao_channels.add_ao_voltage_chan(pzt_port, name_to_assign_to_channel="ao_channel", min_val=0.0, max_val=5.0)
        start_volt = 0.0
        task.write(0)

def gradually_increase_v(pzt_port, label, pzt_volt, tim, electro_port, electro_volt):
    with nidaqmx.Task() as task:
        task.ao_channels.add_ao_voltage_chan(pzt_port, name_to_assign_to_channel="ao_channel", min_val=0.0, max_val=5.0)
        start_volt = 0.0
        end_volt = pzt_volt
        duration = tim
        time_step = 0.1
        num_steps = int(duration / time_step)
        volt_step = (end_volt - start_volt) / num_steps

        fig, ax = plt.subplots()
        fig.set_size_inches(label.winfo_width() / 100, label.winfo_height() / 100)
        canvas = FigureCanvasTkAgg(fig, master=label)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        line, = ax.plot([], [])
        ax.set_ylim([start_volt, end_volt + 0.1])
        ax.set_xlabel('Time')
        ax.set_ylabel('Voltage')
        ax.set_title('PZT applied Voltage')
        ax.set_xlim(0, duration * 3.5)

        times, voltages = [], []
        start_time = time.time()

        def update_plot():
            line.set_data(times, voltages)
            ax.relim()
            ax.autoscale_view(True, True, False)
            canvas.draw()
            canvas.flush_events()
            time.sleep(time_step)

        for _ in range(2 * num_steps):
            if _ == 0:
                analogout(v=electro_volt, d=electro_port)
                voltage = 0
            elif _ < num_steps:
                voltage = start_volt + _ * volt_step

            elif _ == num_steps:
                voltage = end_volt
                analogout(v=0, d=electro_port)

            elif _ > num_steps:
                voltage = end_volt - (_ - num_steps) * volt_step

            task.write(voltage)
            voltages.append(voltage)
            times.append(time.time() - start_time)
            update_plot()

        task.write(start_volt)
        analogout(v=0, d=electro_port)
        voltages.append(start_volt)
        times.append(time.time() - start_time)
        ax.set_xlabel(f"Time: {round(time.time() - start_time, 3) / 2}s Voltage: {end_volt}V")
        update_plot()
        time.sleep(time_step)


def vinlive(self, dev="Dev2/ai0"):
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan(dev)
        plt.ion()
        fig, ax = plt.subplots()
        line, = ax.plot(np.random.rand(100))
        while True:
            data = task.read(number_of_samples_per_channel=100)
            line.set_ydata(data)
            print(data)
            plt.draw()
            plt.pause(0.01)

def analogin():
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan(dev)
        data = task.read()
        return data

def digitalout(boolean):
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(digital)
        task.write(boolean)

def digitalin():
    with nidaqmx.Task() as task:
        task.di_channels.add_di_chan(digital)
        data = task.read()
        return data

