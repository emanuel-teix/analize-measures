import copy
import math as math
import os
import sys
from scipy.spatial import Delaunay
import numpy as np
#import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
#from matplotlib.patches import Ellipse
from matplotlib import collections as mc
import time

def read_data(min_imag,max_imag):
    counter = 0
    x,y,vx,vy,nx,ny,theta = [],[],[],[],[],[],[]
    a,b,c,d,e,f,g=[],[],[],[],[],[],[]
    with open(name_arq_data_in, 'r') as infile:
        for line in infile:
            if line.startswith("#"):
                if line.split()[0] != "#IND" :
                    counter+=1
                    if min_imag < counter <= max_imag:
                        x.append(a),y.append(b),vx.append(c),vy.append(d),nx.append(e),ny.append(f),theta.append(g)
                        a,b,c,d,e,f,g=[],[],[],[],[],[],[]
            else:
                if min_imag <= counter <= max_imag :
                    lineread=list(map(float,line.split()))
                    a.append(lineread[1])
                    b.append(lineread[2])
                    c.append(lineread[3])
                    d.append(lineread[4])            
                    e.append(lineread[5])
                    f.append(lineread[6])            
                    g.append(lineread[7])
    x.append(a),y.append(b),vx.append(c),vy.append(d),nx.append(e),ny.append(f),theta.append(g)
    return x,y,vx,vy,nx,ny,theta
            


def imag_count(name_arq_data_in) :
    counter = 0
    print("Counting images... wait... it may take 5s to count 1000 images on an I7 \n")
    with open(name_arq_data_in, 'r') as infile:
        for line in infile:
            if line.startswith("#"):
                if line.split()[0] != "#IND" :
                    counter+=1
    print( "Counted", counter, "images.\n")
    print("Type initial and final image number you want to analyse (min=1, max=",counter,") - Use spaces to separate the two numbers")
    line_splitted        = sys.stdin.readline().split()
    min_imag,max_imag = int(line_splitted[0]),int(line_splitted[1])
    if max_imag > counter :
        print("You cannot use  a final image greater than the total number of images. Exiting...")
        exit()

    return min_imag,max_imag

def delaunay(points,max_dist):
    points=np.array(points)
    #print(points)
    tri = Delaunay(points)
    #print(tri.simplices)
    # x,y=[],[]
    # z,zz=[],[]
    # for i,w in enumerate(points):
    #     if i%50 == 0:
    #         x.append(w[0])
    #         y.append(w[1])
    #     else :
    #         z.append(w[0])
    #         zz.append(w[1])
    # fig=plt.scatter(x,y,s=30,c='b')
    # fig=plt.scatter(z,zz,s=30,c='g')
    # plt.show()
    list_neigh = [ [] for i in range(len(points)) ]
    for i in tri.simplices:
        for j in i:
            for l in i:
                if l != j :
                    if np.linalg.norm(points[j]-points[l]) < max_dist : #
                        if l not in list_neigh[j]:
                            list_neigh[j].append(l)
                        if j not in list_neigh[l]:
                            list_neigh[l].append(j)

    #uncomment to see delaunay triangulation image                        
    # x,y=[],[]
    # for i,w in enumerate(list_neigh) :
    #     if i%50==0 :
    #         for j in w :
    #             x.append(points[j][0])
    #             y.append(points[j][1])
    # fig=plt.scatter(x,y,s=30,c='r')
    # fig=plt.triplot(points[:,0], points[:,1], tri.simplices.copy())
    # plt.savefig("toto.png")
    return list_neigh

# function mapping delaunay out index to particle index
# def map_focus_region_to_part(points, list_neighbors, index_particle):
#     for i,w in enumerate(points):
#         #print i, index_particle[i]
#         aux                  = index_particle[i]
#         #print aux
#         part[aux].r          = np.array(w)
#         part[aux].list_neigh = []
#         for j in list_neighbors[i]:
#             part[aux].list_neigh.append(index_particle[j])


# ############Particle class definition##############
# class particle:
#     def __init__(self,ident):
#         self.Delta_counter  = 0
#         self.Delta          = 0.
#         self.r              = np.array([-2000.,-2000.])
#         self.r_orig          = np.array([-2000.,-2000.])
#         self.ident          = ident  #indice geral da particula
#         self.list_neigh     = []
#         self.list_neigh_old = []
#         self.list_neigh_old_delta = []


#     def my_original_position(self):#new
#         self.r_orig=self.r
#         self.list_neigh_old_delta=self.list_neigh
#         #print self.ident, self.r, self.list_neigh
#         #exit()
#         return
        
#     def delta_solid_liquid(self,Delta_x0): #new
#         if self.r_orig[0] >Delta_x0+box_size and self.r_orig[0]<Delta_x0+2*box_size :
#             ll=len(self.list_neigh_old_delta)
#             self.Delta = 0
#             if ll > 4:
#                 for i in self.list_neigh_old_delta:
#                     dr_old_2=np.linalg.norm(part[i].r_orig-self.r_orig)**2
#                     dr_2=np.linalg.norm(part[i].r-self.r)**2
#                     delta_loc = 1-dr_old_2/dr_2
#                     if delta_loc > 0 :
#                         self.Delta+=delta_loc
#                     else:
#                         ll-=1
#                     #print self.ident,i,np.sqrt(dr_old_2),np.sqrt(dr_2),1-dr_old_2/dr_2
#                 if ll > 0 :
#                     self.Delta/=ll
#                 self.Delta_counter=1
#             #print self.ident,self.r_orig[0],self.Delta
#             #exit()
#         return

                    
#     def copy_to_old(self):
#         self.list_neigh_old=copy.deepcopy(self.list_neigh)
#         self.r_old=copy.deepcopy(self.r)
#         self.U_old=copy.deepcopy(self.U)
#         self.M_old=copy.deepcopy(self.M)
#         return self.list_neigh_old
    

            

###############Particle class definition ends here###########

#Opening input parameter file 

file_input_parameter = open("parameter.in")
line_splitted        = file_input_parameter.readline().split()
system_type          = line_splitted[0]
path                 = 'output/' + system_type
max_dist = 13.
#Creating the directory structure for output
os.system('mkdir -p %s' % path)
#open file with input data
#name_arq_data_in = system_type+"/"+line_splitted[1]
name_arq_data_in = line_splitted[1]
#print(name_arq_data_in)
min_imag,max_imag=imag_count(name_arq_data_in)
#print(x)

#reading all variables in the time interval of interest
x,y,vx,vy,nx,ny,theta=read_data(min_imag,max_imag)
#print(x)
#analising...
global_list_neigh=[]
for i in range(len(x)): #i is the image index
    points = []
    for j in range(len(x[i])): #j is the ring center of mass index
        points.append([x[i][j],y[i][j]])
    #print(points)
    #exit()
    aux=delaunay(points,max_dist)
#    print(i)
#    print(aux)
    global_list_neigh.append(aux)
    # print(global_list_neigh[i])
    # print(points)
    #exit()

#print(len(global_list_neigh))

Number_images = len(x)
delta=[]
for j in range(int(Number_images)):
    delta_janela=[]
    for i in range(Number_images-j):
        delta_aux=[]
        for k in range(len(global_list_neigh[i])):
            if len(global_list_neigh[i][k]) > 0 :
                delta_aux.append(len(set(global_list_neigh[i][k]) & set(global_list_neigh[i+j][k]))/len(global_list_neigh[i][k]))
        delta_janela.append(sum(delta_aux)/len(delta_aux))
    delta.append(delta_janela)
mean_delta=[]
window=[]
counter=0
#o=open('delta.dat','w')
for i in delta:
    counter+=1
    #print(i)
    mean_delta.append(sum(i)/len(i))
    window.append(counter)
    #print(mean_delta)
    
    

#for i in range(int(counter)):
mean_delta_array =  np.array(mean_delta)
o=open('delta_n15_N400_PE1_G0_p013.3_p023.3_eadh115.00_eadh225.00_eadh215.00.dat','w')
for i in range(int(counter)):
    print(i,mean_delta_array[i])
    o.write("%d %f\n"%(i,mean_delta_array[i]))
    
    
exit()    
#plt.yscale("log")
#plt.xscale("log")
#o.write(window,mean_delta)
plt.plot(window,mean_delta)
plt.show()

