import matplotlib.pyplot as plt
import math

print("Program started")

def distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)

class AsteroidSimulation:

    def runsim(self, x, y, z, vx, vy, vz, dt):

        time = 0
        initial_distance = distance(x, y, z, 0, 0, 0)

        self.time = []
        self.xpos = []
        self.ypos = []
        self.dist = []

        while time <= 300000:
            d = distance(x, y, z, 0, 0, 0)

            self.time.append(time)
            self.xpos.append(x)
            self.ypos.append(y)
            self.dist.append(d)

            if d < 6400:
                print("Impact with Earth")
                break

            if d > 2 * initial_distance:
                print("Flyaway")
                break

            ax = -1434921106 / (d**3) * x
            ay = -1434921106 / (d**3) * y
            az = -1434921106 / (d**3) * z

            vx += ax * dt
            vy += ay * dt
            vz += az * dt

            x += vx * dt
            y += vy * dt
            z += vz * dt

            time += dt

        plt.plot(self.time, self.dist)
        plt.title("Distance from Earth vs Time")
        plt.xlabel("Time (hours)")
        plt.ylabel("Distance (km)")
        plt.show()

sim = AsteroidSimulation()
sim.runsim(500000, 500000, 0, 0, 10, 10, 1)
