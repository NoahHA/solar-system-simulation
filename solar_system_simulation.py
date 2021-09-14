import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# TODO: Let user input number of planets e.g. 5 and that's how many are simulated,
# If num_planets > 4 then don't have the planet size be relative

plt.style.use("dark_background")  # makes it look more like space

G = 6.67408 * 10 ** -11  # gravitational constant

# list of tuples, each containing the name, mass (kg), radius (m), distance
# to the Sun (m) (or to Earth in the case of the Moon), and velocity at
# perihelion (km/s) for a number of astronomical bodies

astro_values = [
    ("sun", 1.989 * 10 ** 30, 696_340_000),
    ("mercury", 3.285 * 10 ** 23, 2_439_700, 46.0 * 10 ** 9, 58_980),
    ("venus", 4.867 * 10 ** 24, 6_051_800, 107.48 * 10 ** 9, 35_260),
    ("earth", 5.972 * 10 ** 24, 6_371_000, 147.09 * 10 ** 9, 30_290),
    ("mars", 6.390 * 10 ** 23, 3_389_500, 206.62 * 10 ** 9, 26_500),
]


def single_mass_orbit(vals, M):
    """
    returns an array with dx/dt, dy/dt, dv_x/dt, dv_y/dt
    for orbit with one central mass
    """
    x, y, vx, vy = vals
    r = np.hypot(x, y)  # modulus of r
    a = G * M / r ** 3  # acceleration

    return np.array([vx, vy, -a * x, -a * y])


def RK4step(f, x, h, M):
    """
    calculates k_n for each derivative and returns the next value, x represents all
    derivatives, f is the gravitational potential function used and h is the timestep
    """
    k1 = h * f(x, M)
    k2 = h * f(x + 0.5 * k1, M)
    k3 = h * f(x + 0.5 * k2, M)
    k4 = h * f(x + k3, M)

    x += (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return x


def RK4integrate(f, init_vals, t, M, R=0):
    """
    Integrates each of the RK4 steps and returns an array filled
    with all position and velocity values
    """

    # empty array to be filled with position and velocity values
    vals = np.zeros([len(t), len(init_vals)])
    vals[0] = init_vals  # sets initial conditions

    for i in range(1, len(t)):
        # computes RK4 for every timestep after the initial conditions
        vals[i] = RK4step(f, vals[i - 1], t[i] - t[i - 1], M)

        # ends the program if the rocket crashes
        if np.hypot(vals[i][1], vals[i][2]) <= R:
            break

    return vals.T  # returns the transpose of the array


def main():
    """
    Simulates the orbits of the first four planets in the solar system using
    perihelion as the starting conditions.
    """
    fig = plt.figure()
    ax = plt.axes()
    # makes sure the axes are the same size so the orbit isn't distorted
    ax.set_aspect("equal")

    # sizes of planets are calibrated with respect to mercury
    mercury_size = 3
    size_calibration_value = mercury_size / astro_values[1][2]
    venus_size = astro_values[2][2] * size_calibration_value
    earth_size = astro_values[3][2] * size_calibration_value
    mars_size = astro_values[4][2] * size_calibration_value

    # creates individual markers for each planet
    (line_mercury,) = ax.plot(
        [], [], marker="o", ls="", markersize=mercury_size, color="grey"
    )
    (line_venus,) = ax.plot(
        [], [], marker="o", ls="", markersize=venus_size, color="bisque"
    )
    (line_earth,) = ax.plot(
        [], [], marker="o", ls="", markersize=earth_size, color="blue"
    )
    (line_mars,) = ax.plot(
        [], [], marker="o", ls="", markersize=mars_size, color="brown"
    )

    lines = [line_mercury, line_venus, line_earth, line_mars]

    def init():
        for line in lines:
            line.set_data([], [])
        return lines

    def animate(i):
        """Animates each of the planets"""
        line_mercury.set_data(x[i], y[i])
        line_venus.set_data(x2[i], y2[i])
        line_earth.set_data(x3[i], y3[i])
        line_mars.set_data(x4[i], y4[i])

        return [line_mercury, line_venus, line_earth, line_mars]

    # makes sure simulation length is a float between 0 and 50
    while True:
        try:
            t = float(input("Time Period of Simulation in Years: "))
            if t > 0 and t <= 50:
                break
        except ValueError:
            pass

        print("Error: Please enter a number between 0 and 50\n")

    t *= 3.154 * 10 ** 7  # converts years to seconds
    h = 4 * 10 ** 4  # time interval in seconds
    interval = 0.001  # animation interval in seconds
    M_sun, R_sun = astro_values[0][1], astro_values[0][2]
    t_vals = np.arange(0, t, h)

    # Mercury
    init_vals1 = np.array([0, astro_values[1][3], astro_values[1][4], 0])
    x, y, vx, vy = RK4integrate(single_mass_orbit, init_vals1, t_vals, M_sun)

    # Venus
    init_vals2 = np.array([0, astro_values[2][3], astro_values[2][4], 0])
    x2, y2, vx2, vy2 = RK4integrate(single_mass_orbit, init_vals2, t_vals, M_sun)

    # Earth
    init_vals3 = np.array([0, astro_values[3][3], astro_values[3][4], 0])
    x3, y3, vx3, vy3 = RK4integrate(single_mass_orbit, init_vals3, t_vals, M_sun)

    # Mars
    init_vals4 = np.array([0, astro_values[4][3], astro_values[4][4], 0])
    x4, y4, vx4, vy4 = RK4integrate(single_mass_orbit, init_vals4, t_vals, M_sun)

    anim = animation.FuncAnimation(
        fig,
        animate,
        init_func=init,
        frames=len(x),
        interval=interval,
        blit=True,
        repeat=False,
    )

    # actual sun size is too big so I went with what I thought looks best
    sun_factor = 25
    sun = plt.Circle((0, 0), radius=sun_factor * R_sun, fc="yellow")
    plt.gca().add_patch(sun)

    # size of the simulation is slightly larger than the largest orbit
    mars_orbital_radius = astro_values[4][3]
    plot_size = mars_orbital_radius * 1.4

    plt.xlim(-plot_size, plot_size)
    plt.ylim(-plot_size, plot_size)
    plt.axis("off")

    plt.show()


if __name__ == "__main__":
    main()
