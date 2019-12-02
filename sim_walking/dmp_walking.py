import csv
from dmp_experiments.Python.train_dmp import *
import numpy as np
from dmp_experiments.Python.DMP_runner import DMP_runner
import matplotlib.pyplot as plt
from decimal import *

file = '/home/rhosea/catkin_ws/src/lidar_reading_package/sim_walking/leg_info.csv'
lhip_dmp = 'lhip_dmp'
lkne_dmp = 'lkne_dmp'
lank_dmp = 'lank_dmp'
rhip_dmp = 'rhip_dmp'
rkne_dmp = 'rkne_dmp'
rank_dmp = 'rank_dmp'

# desired foot positions
# joint_trajs = invKin(foot) # array of desired start and end angle positions for each joint
# hardcoded joint hip start and end for now
lhip_pos = [-15,-9]
lkne_pos = [-15,-3]
lank_pos = [-10,-9]
rhip_pos = [-15,-9]
rkne_pos = [-15,-9]
rank_pos = [-15,-9]

trial_len = 0
T = []
q = []
qd = []
qdd = []
with open(file) as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        q = []
        qd = []
        qdd = []
        for val in row:
            q.append(float(val))
            qd.append(0.0)
            qdd.append(0.0)
        T.append(q)
        T.append(qd)
        T.append(qdd)
    T_lhip = T[0:3]
    T_lkne = T[3:6]
    T_lank = T[6:9]
    T_rhip = T[9:12]
    T_rkne = T[12:15]
    T_rank = T[15:18]
    print(T_lkne)
    trial_len = len(q)

dt = Decimal(1) / Decimal(trial_len)
dt = float(dt)

num_basis_fcns = 1000
trained_lhip = train_dmp(lhip_dmp,num_basis_fcns,T_lhip,dt)
trained_lkne = train_dmp(lkne_dmp,num_basis_fcns,T_lkne,dt)
trained_lank = train_dmp(lank_dmp,num_basis_fcns,T_lank,dt)
trained_rhip = train_dmp(rhip_dmp,num_basis_fcns,T_rhip,dt)
trained_rkne = train_dmp(rkne_dmp,num_basis_fcns,T_rkne,dt)
trained_rank = train_dmp(rank_dmp,num_basis_fcns,T_rank,dt)

lhip_runner = DMP_runner(lhip_dmp,lhip_pos[0],lhip_pos[1])
lkne_runner = DMP_runner(lkne_dmp,lkne_pos[0],lkne_pos[1])
lank_runner = DMP_runner(lank_dmp,lank_pos[0],lank_pos[1])
rhip_runner = DMP_runner(rhip_dmp,rhip_pos[0],rhip_pos[1])
rkne_runner = DMP_runner(rkne_dmp,rkne_pos[0],rkne_pos[1])
rank_runner = DMP_runner(rank_dmp,rank_pos[0],rank_pos[1])

Y = []
tau = 1
for i in np.arange(0,int(tau/dt)+1):
    lkne_runner.step(tau,dt)
    Y.append(lkne_runner.y)

time = np.arange(0,tau+dt,dt)

plt.title("2-D DMP demonstration")
plt.xlabel("Time(t)")
plt.ylabel("Angle Position(deg)")
print(Y)
plt.plot(time[1:4993],T_lhip[0])
plt.plot(time,Y)
plt._show()