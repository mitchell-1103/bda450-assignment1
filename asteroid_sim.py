import matplotlib.pyplot as plt
import math
import astropy.coordinates


#helper functions

def spherical_to_components(magnitude, bearing, trajectory):
    return astropy.coordinates.spherical_to_cartesian(
        magnitude,
        math.radians(trajectory),
        math.radians(bearing))


def components_to_spherical(x, y, z):
    magnitude, trajectory, bearing = astropy.coordinates.cartesian_to_spherical(x, y, z)
    return magnitude, math.degrees(bearing.to_value()), math.degrees(trajectory.to_value())


def distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)


# start simulation

class AsteroidSimulation:

    def runsim(self,
               starting_xposition, starting_yposition, starting_zposition,
               starting_xvelocity, starting_yvelocity, starting_zvelocity,
               timeinterval):

        # initial position
        x = starting_xposition
        y = starting_yposition
        z = starting_zposition

        # initial velocity
        vx = starting_xvelocity
        vy = starting_yvelocity
        vz = starting_zvelocity

        time = 0
        initial_distance = distance(x, y, z, 0, 0, 0)

        # lists for plots
        self.time = []
        self.xpos = []
        self.ypos = []
        self.zpos = []
        self.distances = []
        self.speeds = []

        # primary simulation loop
        while time <= 300000:

            d = distance(x, y, z, 0, 0, 0)

            # record current position
            speed, _, _ = components_to_spherical(vx, vy, vz)
            self.time.append(time)
            self.xpos.append(x)
            self.ypos.append(y)
            self.zpos.append(z)
            self.distances.append(d)
            self.speeds.append(speed)

            # stop conditions
            if d < 6400:
                print("Impact with Earth")
                break

            if d > 2 * initial_distance:
                print("Flyaway")
                break

            # gravitational acceleration elements
            ax = -1434921106 / (d ** 3) * x
            ay = -1434921106 / (d ** 3) * y
            az = -1434921106 / (d ** 3) * z

            # new velocity
            vx += ax * timeinterval
            vy += ay * timeinterval
            vz += az * timeinterval

            # new position
            x += vx * timeinterval
            y += vy * timeinterval
            z += vz * timeinterval

            time += timeinterval

        if time >= 300000:
            print("Time out")

        self.make_plots()

    # plotting
    
    def make_plots(self):

        plt.figure()
        plt.plot(self.time, self.xpos)
        plt.title("X Position vs Time")
        plt.xlabel("Time (hours)")
        plt.ylabel("X Position (km)")

        plt.figure()
        plt.plot(self.xpos, self.ypos)
        plt.title("X Position vs Y Position")
        plt.xlabel("X Position (km)")
        plt.ylabel("Y Position (km)")
        plt.axis('square')

        plt.figure()
        plt.plot(self.time, self.distances)
        plt.title("Distance from Earth vs Time")
        plt.xlabel("Time (hours)")
        plt.ylabel("Distance (km)")

        plt.figure()
        plt.plot(self.time, self.speeds)
        plt.title("Speed vs Time")
        plt.xlabel("Time (hours)")
        plt.ylabel("Speed (km/h)")

        fig = plt.figure()
        ax = plt.axes(projection='3d')
        ax.plot(self.xpos, self.ypos, self.zpos)
        ax.plot(0, 0, 0, 'ro')
        ax.set_title("3D Path of Asteroid")
        ax.set_xlabel("X (km)")
        ax.set_ylabel("Y (km)")
        ax.set_zlabel("Z (km)")
        plt.axis('square')
        plt.show()


# test run required by assignment

sim = AsteroidSimulation()
sim.runsim(
    500000, 500000, 0,   # starting position
    0, 10, 10,           # starting velocity
    1                    # time interval (hours)
)