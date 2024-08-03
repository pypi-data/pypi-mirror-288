import matplotlib.pyplot as plt
import numpy as np
import numba as nb

from minimum_jerk.mytypes import Array, Array2D
import minimum_jerk.utils as fcs

def path_planning(X: Array2D, V: Array2D, 
                  A: Array2D, T: Array, 
                  dt: float) -> tuple:
    
    nr_step = fcs.get_steps(T[-1]-T[0], dt) + 1
    t_stamp = np.linspace(T[0], T[-1], nr_step, endpoint=True)

    position     = [None] * X.shape[0]
    velocity     = [None] * X.shape[0]
    acceleration = [None] * X.shape[0]
    jerk         = [None] * X.shape[0]

    for i in range(len(X)):
        position[i], velocity[i], acceleration[i], jerk[i] = get_minjerk_trajectory(dt, T, X[i], V[i], A[i])

    position = np.array(position)
    velocity = np.array(velocity)
    acceleration = np.array(acceleration)
    jerk = np.array(jerk)
    
    return position, velocity, acceleration, jerk, t_stamp


def get_minjerk_trajectory(dt, tt, xx, uu, aa):
    """Computes a multi-interval minjerk trajectory in 1 dimension

    Args:
        dt ([list]): [double] x nr_intervals
        tt ([list]): [double] x nr_intervals
        xx ([list]): [double] x nr_intervals
        uu ([list]): [double] x nr_intervals
        smooth_acc (bool, optional): Whether the acceleartion between intervals should be smooth.
        i_a_end ([type], optional): If not None shows the number of the interval, whose end-acceleration should be used for the last interval.

    Returns:
        [lists]: x, v, a, j
    """
    # Initialization
    T_whole = tt[-1] - tt[0]
    N_Whole = fcs.get_steps(T_whole, dt) + 1
    x_ret = np.zeros(N_Whole, dtype='double')
    v_ret = np.zeros(N_Whole, dtype='double')
    a_ret = np.zeros(N_Whole, dtype='double')
    j_ret = np.zeros(N_Whole, dtype='double')

    N = len(tt)

    t_last = tt[0]  # last end-time
    n_last = 0  # last end-index

    for i in range(N-1):
        t0 = tt[i]; t1 = tt[i+1]
        x0 = xx[i]; x1 = xx[i+1]
        u0 = uu[i]; u1 = uu[i+1]
        a_ta = aa[i]; a_tb = aa[i+1]
        x, v, a, j = get_min_jerk_trajectory(dt, t0, t1, x0, x1, u0, u1, a_ta=a_ta, a_tb=a_tb)

        len_x = len(x)

        if i == 0:
            x_ret[n_last: n_last+len_x] = x
            v_ret[n_last: n_last+len_x] = v
            a_ret[n_last: n_last+len_x] = a
            j_ret[n_last: n_last+len_x] = j
            n_last += len_x
        else:
            x_ret[n_last: n_last+len_x-1] = x[1:]
            v_ret[n_last: n_last+len_x-1] = v[1:]
            a_ret[n_last: n_last+len_x-1] = a[1:]
            j_ret[n_last: n_last+len_x-1] = j[1:]
            n_last += len_x - 1

    return x_ret, v_ret, a_ret, j_ret

def get_min_jerk_trajectory(dt, ta, tb, x_ta, x_tb, u_ta, u_tb, a_ta=None, a_tb=None):
  # Input:
  #   x_ta, u_ta, (optional: a.ta): conditions at t=ta
  #   x_tb, u_tb, (optional: a.tb): conditions at t=tb
  #   a: is set to [] if start and end acceleration are free
  # Output:
  #   xp_des(t) = [x(t)       u(t)         a(t)            u(t)]
  #             = [position   velocity     acceleration    jerk]

  # Get polynom parameters for different conditions
  T = tb-ta
  if a_ta is not None:
    # 1. set start acceleration
    if a_tb is not None:
      # a. set end acceleration
      c1, c2, c3, c4, c5, c6 = set_start_acceleration(T, x_ta, x_tb, u_ta, u_tb, a_ta, a_tb)
    else:
      # b.free end acceleration
      c1, c2, c3, c4, c5, c6 = set_start_acceleration(T, x_ta, x_tb, u_ta, u_tb, a_ta)
  else:
    # 2. free start acceleration
    if a_tb is not None:
      # a. set end acceleration
      c1, c2, c3, c4, c5, c6 = free_start_acceleration(T, x_ta, x_tb, u_ta, u_tb, a_tb)
    else:
      # b.free end acceleration
      c1, c2, c3, c4, c5, c6 = free_start_acceleration(T, x_ta, x_tb, u_ta, u_tb)

  # Trajectory values ta->tb
  t = np.linspace(0, T, num=round(T/dt+1), endpoint=True) 
  j, a, v, x = get_trajectories(t, c1, c2, c3, c4, c5, c6)
  # x = get_trajectories(t, c1, c2, c3, c4, c5, c6)
  # return x
  return x, v, a, j

# Get  values from polynom parameters
@nb.jit(nopython=True)
def get_trajectories(t, c1, c2, c3, c4, c5, c6):
  # print(c1)
  t_5 = t**5
  t_4 = t**4
  t_3 = t**3
  t_2 = t**2
  j = c1*t_2/2   - c2*t      + c3                               # jerk
  a = c1*t_3/6   - c2*t_2/2  + c3*t     + c4                    # acceleration
  v = c1*t_4/24  - c2*t_3/6  + c3*t_2/2 + c4*t      + c5        # velocity
  x = c1*t_5/120 - c2*t_4/24 + c3*t_3/6 + c4*t_2/2 + c5*t + c6  # position
  return [j, a, v, x]

# 1) Acceleration is set at t=0 (a(0)=a0 => c4=a0)
# @nb.jit(nopython=True)
def set_start_acceleration(T, x0, xT, u0, uT, a0=None, aT=None):
    T_5 = T**5
    T_4 = T**4
    T_3 = T**3
    T_2 = T**2
    if aT is None:
        # free end acceleration u(T)=0
        M = np.array([[320/T_5, -120/T_4, -20/(3*T_2)],
                        [200/T_4, -72/T_3, -8/(3*T)],
                        [40/T_3, -12/T_2, -1.0/3.0]])
        c = np.array([-(a0*T_2)/2 - u0*T - x0 + xT, uT - u0 - T*a0, 0])
    else:
        # set end acceleration a(T)=aT
        M = np.array([[720/T_5, -360/T_4, 60/T_3],
                        [360/T_4, -168/T_3, 24/T_2],
                        [60/T_3, -24/T_2, 3/T]])
        c = np.array([xT - x0 - T*u0 - (a0*T_2)/2, uT - u0 - T*a0, aT - a0])

    c123 = M.dot(c.T)
    c1 = c123[0]
    c2 = c123[1]
    c3 = c123[2]
    c4 = a0
    c5 = u0
    c6 = x0
    return c1, c2, c3, c4, c5, c6

# 2) Acceleration is free at t=0 (u(0)=0 => c3=0)
@nb.jit(nopython=True)
def free_start_acceleration(T, x0, xT, u0, uT, aT=None):
    T_5 = T**5
    T_4 = T**4
    T_3 = T**3
    T_2 = T**2
    if aT is None:
        # free end acceleration u(T)=0
        M = np.array([[120/T_5, -60/T_4, -5/T_2],
                        [60/T_4, -30/T_3, -3/(2*T)],
                        [5/T_2, -3/(2*T), -T/24]])
        c = np.array([xT - x0 - T*u0, uT - u0, 0])
    else:
        # set end acceleration a(T)=aT
        M = np.array([[320/T_5, -200/T_4, 40/T_3],
                        [120/T_4, -72/T_3, 12/T_2],
                        [20/(3*T_2), -8/(3*T), 1.0/3.0]])
        c = np.array([xT - x0 - T*u0, uT - u0, aT])

    c123 = M.dot(c.T)
    c1 = c123[0]
    c2 = c123[1]
    c4 = c123[2]
    c3 = 0
    c5 = u0
    c6 = x0
    return c1, c2, c3, c4, c5, c6

def plotMinJerkTraj(x, v, a, j, dt, title, intervals=None, colors=None, tt=None, xx=None, uu=None):
  """Plots the x,v,a,j trajectories together with possible intervals and colors

  Args:
      x ([List(double)]): position vector
      v ([List(double)]): velocity vector
      a ([List(double)]): acceleration vector
      j ([List(double)]): jerk vector
      dt ([double]): time step
      title ([String]): tittle of the plot
      intervals ([set((a,b))], optional): {(0.1, 0.2), (0.42,0.55), ..}
      colors ([tuple], optional): ('gray', 'blue', ..)
  """
  if colors is None:
    colors = []
  fig, axs = plt.subplots(4, 1)
  timesteps = np.arange(0, x.size) * dt + tt[0]  # (1:length(x))*dt
  for ax in axs:
    ax.set_xlim(xmin=0,xmax=timesteps[-1])
  axs[0].plot(timesteps, x, 'b', label='Plate position')
  axs[0].legend(loc=1)
  axs[1].plot(timesteps, v, 'b', label='Plate velocity')
  axs[1].legend(loc=1)
  axs[2].plot(timesteps, a, 'b', label='Plate acceleration')
  axs[2].legend(loc=1)
  axs[3].plot(timesteps, j, 'b', label='Plate jerk')
  axs[3].legend(loc=1)

  for i in range(4):
    for t in tt:
      axs[i].axvline( t )

  fig.suptitle(title)
  plt.show(block = False)

def plotMJ(dt, tt, xx, uu, smooth_acc):
    print(
    "\n X: " +str(xx) +
    "\n T: " +str(tt) +
    "\n U: " +str(uu)
        )
    title = "Min-Jerk trajectory with " +  ("" if smooth_acc else "non") +"-smoothed acceleration."
    x, v, a, j = get_minjerk_trajectory(dt, tt=tt, xx=xx, uu=uu, smooth_acc=smooth_acc)
    plotMinJerkTraj(x, v, a, j, dt, title, tt=tt[0:4], xx=xx[0:4], uu=uu[0:4])

if __name__ == "__main__":
  dt = 1 / 100
  # time stamp
  tt = [0,   0.2, 0.8, 1]
  # corresponding positions
  xx = [ [0.0, 0.2, 0.6, 0.2],
         [0.0, 0.6, 0.9, 0.1],
         [0.0, 1.0, 2.0, -1.0]]
  # corresponding velocities
  uu = [ [0.0, 3.4, 2.0, 1.0],
         [0.0, 2.2, 1.2, -1.3],
         [0.0, 3.0, 1.3, 5.0] ]
  # None for free, concrete value for fixed
  aa = [ [0.0, 0.0, 0.0, 0.0],
         [0.0, 0.0, 0.0, 0.0],
         [0.0, 0.0, 0.0, 0.0] ]
  
  xx = np.array(xx)
  uu = np.array(uu)
  aa = np.array(aa)
  tt = np.array(tt)

  xxx, vvv, aaa, jjj, t_stamp = path_planning(xx, uu, aa, tt, dt)

  plotMinJerkTraj(xxx[0], vvv[0], aaa[0], jjj[0], dt,  "Free acceleartion", tt=tt)
  plt.show()
