import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
plt.style.use('dark_background')            #背景颜色设置为黑色

xx = []
yy = []
zz = []
N=50
xmar= np.linspace(-5,5,N)   #从min(df.x)到max(df.x)，共N个数
ymar= np.linspace(-5,5,N)
x,y=np.meshgrid(xmar,ymar)    #X为N行都为min(df.x)到max(df.x)的矩阵，Y同理。shape值都为(30,30)
z = np.zeros((N,N))
z[5:10,5:10]=10
z[5:10,40:45]=30
z[40:45,5:10]=50
z[40:45,40:45]=70
class Particle:
    def __init__(self, x, y, z, ang_vel):
        self.x = x                  #粒子的起始X点位置
        self.y = y                  #粒子的起始Y点位置
        self.z = z                  #粒子的起始Y点位置
        self.ang_vel = ang_vel      #速度和旋转方向(+为逆时针，-为顺时针)

class ParticleSimulator:
    def __init__(self, particles):
        self.particles = particles

    def evolve(self, dt):
        timestep = 0.01
        nsteps = int(dt / timestep)

        for i in range(nsteps):
            for p in self.particles:
                
                norm = (p.x **2 + p.y ** 2) ** 0.5
                v_x = -p.y / norm
                v_y = p.x / norm

                d_x = timestep * p.ang_vel * v_x
                d_y = timestep * p.ang_vel * v_y

                p.x += d_x
                p.y += d_y
                p.z = p.z

#绘三维图
def visualize(simulator):
    
    X = [p.x for p in simulator.particles]
    Y = [p.y for p in simulator.particles]
    Z = [p.z for p in simulator.particles]
    
    fig = plt.figure(figsize=(20,8),dpi =90)
    # ax = p3.Axes3D(fig)
    
    ax = fig.add_subplot(121,projection="3d")
    ax1 = fig.add_subplot(122)
    # ax = plt.gca(projection="3d") 
    # 运动的点
    point, = ax.plot(X, Y, Z, 'ro', label='p')     #如果不加逗号，返回值是包含一个元素的list，加上逗号表示直接将list的值取出
    # 曲线
    line, = ax.plot(X, Y, Z,'y-', label='line')
    # 运动的点
    point1, = ax1.plot(X, Y, "ro")     #如果不加逗号，返回值是包含一个元素的list，加上逗号表示直接将list的值取出
    # 曲线
    line1, = ax1.plot(X, Y,'y-', label='line')
    # point = [ax.plot(data[0][0,0:1], data[0][1,0:1], data[0][2,0:1],'ro')[0]]       #起始坐标点,data[0][0,0:1]=[0.] ,而data[0][0,0]=0.0
    plt.xlim(-5, 5)
    plt.ylim(-5, 5)

    def init():
        point.set_data([], [])
        point1.set_data([], [])
        return point,                #加上逗号表示返回包含只元素point的元组
    def animate(i):     
        simulator.evolve(0.01)
        X = [p.x for p in simulator.particles]
        Y = [p.y for p in simulator.particles]
        Z = [p.z for p in simulator.particles]
        xx.append(X[0])
        yy.append(Y[0])
        zz.append(Z[0])
        line.set_data(xx[:i+1],yy[:i+1])
        line.set_3d_properties(zz[:i+1])
        point.set_data(X[0],Y[0])
        point.set_3d_properties(Z[0])

        line1.set_data(xx[:i+1],yy[:i+1])
        point1.set_data(X[0],Y[0])

        # print(xx)
        return point,point1,

    ax.set_xlabel('X轴')
    ax.set_ylabel('Y轴')
    ax.set_zlabel('Z轴')
    ax.set_title('3D Test')

    ax.view_init(azim=-60, elev=20)      #azim为图片初始显示时候的角度，0的话为视角垂直x轴。elev=0的话是垂直Z轴
    ax.grid(True)       #True开启网格,False关闭网格

    ax.xaxis._axinfo['tick']['outward_factor'] = 0.0    #坐标轴内(outward)突出的线长
    ax.xaxis._axinfo['tick']['inward_factor'] = 0.4     #坐标轴外(inward)突出的线长
    ax.yaxis._axinfo['tick']['outward_factor'] = 0
    ax.yaxis._axinfo['tick']['inward_factor'] = 0.4
    ax.zaxis._axinfo['tick']['outward_factor'] = 0
    ax.zaxis._axinfo['tick']['inward_factor'] = 0.4

    ax.xaxis.pane.fill = False      #为True或者屏蔽的话图像内的背景颜色偏灰色点
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    ax.xaxis.pane.set_edgecolor('k')        #三维后半部分边框线条黑色加粗
    ax.yaxis.pane.set_edgecolor('k')
    ax.zaxis.pane.set_edgecolor('k')
 
    p=ax.plot_surface(x,y, z, rstride=1, cstride=1, cmap='Spectral_r',alpha=0.6,edgecolor='k',linewidth=0.05)
    cbar=fig.colorbar(p, shrink=0.5,aspect=10)
    cbar.ax.set_title('Z',fontsize=10)
    #-------------------------等高线图---------------------------------------------------
    # fig1, ax1 = plt.subplots(figsize=(5,4),dpi =90)  
    # CS=ax1.contour(x,y, z, levels=10, linewidths=0.5, colors='k')
    cntr = ax1.contourf(x,y, z, levels=10, cmap="Spectral_r")
    # # ax.plot_surface(x,y, rstride=1, cstride=1, cmap='Spectral_r',alpha=0.6,edgecolor='k',linewidth=0.05)
    # scat=ax.scatter(df.x, df.y,c=df.z,s=40, linewidths=0.5, edgecolors="k",alpha=0.8)
    ax1.set_xlabel("X轴")
    ax1.set_ylabel("Y轴")
    # fig.colorbar(cntr,ax1=ax1,label="高度值")  
    # cbar = fig.colorbar(cntr,shrink=0.5,aspect=10,label="高度值")  
    # ax1=cbar.ax   #调出colorbar的ax属性
    # ax1.set_title('高度值',fontsize=10)
    # CS.levels = [int(val) for val in cntr.levels]

    # #FuncAnimation(fig,func,frames,init_func,interval,blit)
    # #fig 绘制动图的画布名称
    # #func自定义动画函数，即下边程序定义的函数update
    # #frames动画长度，一次循环包含的帧数，在函数运行时，其值会传递给函数update(n)的形参“n”
    # #init_func自定义开始帧，即传入刚定义的函数init,初始化函数
    # #e.interval更新频率，以ms计
    # #f.blit选择更新所有点，还是仅更新产生变化的点。应选择True，但mac用户请选择False，否则无法显
    ani = animation.FuncAnimation(fig, animate,init_func = init, blit=False,interval=10)
    
    plt.show()


def test_visualize():
    particles = [Particle(2, 2, 30, 5)]
    #             #  Particle(0.0, -0.5, -1),
    #             #  Particle(-0.1, -0.4, 3)]
    simulator = ParticleSimulator(particles)
    visualize(simulator)

if __name__ == '__main__':
    test_visualize()
    plt.show()