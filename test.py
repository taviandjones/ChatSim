import pandas as pd
import numpy as np
import simpy
import matplotlib.pyplot as plt
import time

plt.ion()

x = [0]
y = [0]
a = [0, 1, 2, 3]
b = [4, 7, 6, 3]
fig, ax = plt.subplots(ncols=2)
ax[0].plot(x, y)
ax[1].plot(a, b)

plt.show()

class Person:
    def __init__(self, id):
        self.id = id

class Hotel:
    def __init__(self):
        self.env = simpy.Environment()
        self.room = simpy.Resource(self.env, capacity=1)
        self.id = 0

    def generate_person(self):
        while True:
            person = Person(self.id)
            self.env.process(self.enter_hotel(person))
            self.id += 1
            yield self.env.timeout(20)
            plt.cla()
            x.append(float(self.env.now))
            y.append(len(self.room.queue))
            ax[0].plot(x, y)
            b[3] += 1
            ax[1].plot(a, b)
            plt.pause(0.5)

    def enter_hotel(self, customer):
        print('Person {} came'.format(customer.id))
        with self.room.request() as req:
            yield req
            print('Person {} entered room at {}'.format(customer.id, self.env.now))
            print(len(self.room.queue))
            yield self.env.timeout(50)
            print('Person {} left'.format(customer.id))

    def run(self):
        self.env.process(self.generate_person())

        self.env.run(until=200)

hotel = Hotel()
hotel.run()
plt.ioff()
plt.show()