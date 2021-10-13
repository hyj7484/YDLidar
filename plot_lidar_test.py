import os
import ydlidar
import time
import sys
from matplotlib.patches import Arc
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

RMAX = 32.0

fig = plt.figure()
fig.canvas.set_window_title('YDLidar LIDAR Monitor')
lidar_polar = plt.subplot(polar=True)
lidar_polar.autoscale_view(True,True,True)
lidar_polar.set_rmax(RMAX)
lidar_polar.grid(True)
ports = ydlidar.lidarPortList();
port = "/dev/ydlidar";
for key, value in ports.items():
    port = value;

laser = ydlidar.CYdLidar();
laser.setlidaropt(ydlidar.LidarPropSerialPort, port);
# 포트 설정 YDLIDAR X4 = 128000
laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 128000)

laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TOF);
laser.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL);
laser.setlidaropt(ydlidar.LidarPropScanFrequency, 10.0);
laser.setlidaropt(ydlidar.LidarPropSampleRate, 20);
laser.setlidaropt(ydlidar.LidarPropSingleChannel, False);

# 각도
# 측정 범위 각도 설정
laser.setlidaropt(ydlidar.LidarPropMaxAngle, 180.0);
laser.setlidaropt(ydlidar.LidarPropMinAngle, -180.0);
# 범위 ?
# 측정 거리
laser.setlidaropt(ydlidar.LidarPropMaxRange, 10.0);
laser.setlidaropt(ydlidar.LidarPropMinRange, 0.01);
# 스캔 ?
scan = ydlidar.LaserScan()

def animate(num):

    r = laser.doProcessSimple(scan);
    if r:
        angle = []
        ran = []
        intensity = []
        for point in scan.points:
            angle.append(point.angle);
            ran.append(point.range);
            intensity.append(point.intensity);
        lidar_polar.clear()
        lidar_polar.scatter(angle, ran, c=intensity, cmap='hsv', alpha=0.95)

ret = laser.initialize();
if ret:
    ret = laser.turnOn();
    if ret:
        ani = animation.FuncAnimation(fig, animate, interval=50)
        plt.show()
        while ret and ydlidar.os_isOk() :
            r = laser.doProcessSimple(scan);
            if r:
                print("Scan received[",scan.stamp,"]:",scan.points.size(),"ranges is [",1.0/scan.config.scan_time,"]Hz");
            else :
                print("Failed to get Lidar Data.")
    laser.turnOff();
laser.disconnecting();
plt.close();
