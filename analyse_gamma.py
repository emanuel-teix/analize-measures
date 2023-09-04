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
#from matplotlib import collections as mc
import time

def read_data(min_imag,max_imag,skip_images):
    counter = 0
    x,y,vx,vy,nx,ny,theta,color = [],[],[],[],[],[],[],[]
    a1,a2,a3,a4,a5,a6,a7,a8 =[],[],[],[],[],[],[],[]
    with open(name_arq_data_in, 'r') as infile:
        for line in infile:
            if line.startswith("#"):
                if line.split()[0] != "#IND" :
                    counter+=1
                    if min_imag < counter <= max_imag and (counter-min_imag)%skip_images == 1:
                        #print(counter,counter-min_imag)
                        x.append(a1),y.append(a2),vx.append(a3),vy.append(a4),nx.append(a5),ny.append(a6),theta.append(a7),color.append(a8)
                        a1,a2,a3,a4,a5,a6,a7,a8 =[],[],[],[],[],[],[],[]
            else:
                if min_imag <= counter <= max_imag and (counter-min_imag)%skip_images == 0 :
                    lineread=list(map(float,line.split()))
                    a1.append(lineread[1])
                    a2.append(lineread[2])
                    a3.append(lineread[3])
                    a4.append(lineread[4])            
                    a5.append(lineread[5])
                    a6.append(lineread[6])            
                    a7.append(lineread[7])
                    a8.append(lineread[8])
                    
                    
                    
    x.append(a1),y.append(a2),vx.append(a3),vy.append(a4),nx.append(a5),ny.append(a6),theta.append(a7),color.append(a8)
    return x,y,vx,vy,nx,ny,theta,color
            


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
    print("Image interval to skip  (min=1, max=",counter,")" )
    line_splitted        = sys.stdin.readline().split()
    skip_images = int(line_splitted[0])
    return min_imag,max_imag,skip_images

def delaunay(points,max_dist):
    points=np.array(points)
    ##print(points)
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
line = file_input_parameter.readline()
if not line:  #if you find an empty line after de first proceed to imag_count
    print("Need to know total number of images. Proceeding to counting...")
    min_imag,max_imag,skip_images=imag_count(name_arq_data_in)
    file_input_parameter.close()
    file_input_parameter = open("parameter.in","a")
    file_input_parameter.write("%d %d %d\n"%(min_imag,max_imag,skip_images))
    print("init_imag=%d, end_imag=%d, interval=%d\n"%(min_imag,max_imag,skip_images))
    print("Now you will want to run the programm again.\n")
    exit()
try: #if you find something after de first line which is not an integer programm exits
    zzz = int(line.split()[0])
except IndexError:
    print("\nYou don't have integers on the second line of file parameter.in.\nYou probably have to erase white lines at the end of this file. \nExiting..\n")
    exit()

#reading parameter.in once more, now with image limits and number of images to skip each reading
min_imag,max_imag,skip_images = int(line.split()[0]),int(line.split()[1]),int(line.split()[2])

#reading all variables in the time interval of interest
x,y,vx,vy,nx,ny,theta,color=read_data(min_imag,max_imag,skip_images)
#print("Finished reading input data")
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

#print("Finished finding neighbors")

#for i in range(len(x)): #i is the image index
    #for j in range(len(x[i])): #j is the ring center of mass index
Nred = 0
for i in range(len(x[0])):
    if color[0][i] == 7.0: 
       Nred+=1
#print(Nred)    
ind_viz = []
gamma = x
#gamma_mean = []
#print(len(x))
#print(color[0][global_list_neigh[0][0]])        
#number_viz.append((global_list_neigh[0][0]))
#Calculating segregation order parameter for each ring
ngreen = 0
for i in range(len(global_list_neigh)):
    for j in range(len(x[0])):
        ind_viz = global_list_neigh[i][j]
        #print(len(global_list_neigh[i][j]))
        ngreen = 0;
        for k in range(len(ind_viz)):
            if color[i][ind_viz[k]] == 2.0:
               ngreen+=1
        #print(ngreen)       
        gamma[i][j] = ngreen/len(global_list_neigh[i][j])
        #print(i,j,gamma[i][j])
#Calculating mean segregation order parameter for each red ring                
for i in range(len(global_list_neigh)):
    gamma_mean = 0
    for j in range(len(x[0])):
        if color[i][j] == 7.0:
           gamma_mean += gamma[i][j]
    gamma_mean = gamma_mean/Nred
    print(i,gamma_mean)                    
#ind_viz = global_list_neigh[0][0]

#print(len(global_list_neigh))
#for i in range(len(number_viz)):
    #print(color[0][number_viz[i]])
#Number_images = len(x)
#delta=[]
#for j in range(int(Number_images)):
#    delta_janela=[]
#    for i in range(Number_images-j):
#        delta_aux=[]
#        for k in range(len(global_list_neigh[i])):
#            if len(global_list_neigh[i][k]) > 0 :
#                delta_aux.append(len(set(global_list_neigh[i][k]) & set(global_list_neigh[i+j][k]))/len(global_list_neigh[i][k]))
#        delta_janela.append(sum(delta_aux)/len(delta_aux))
#    delta.append(delta_janela)
#print("Finished calculating delta")
#mean_delta=[]
#window=[]
#counter=0
#o=open('delta.dat','w')
#for i in delta:
  #  counter+=1
    #print(i)
    #mean_delta.append(sum(i)/len(i))
    #window.append(counter*skip_images)
    #print(counter*skip_images,mean_delta)
    
#output_file="delta_"+name_arq_data_in
#o=open(output_file,'w')
#for i,w in enumerate(mean_delta) :
#    o.write("%f %f\n"%(50.0*(i+1)*skip_images,w))
    

    
#plt.yscale("log")
#plt.xscale("log")
#plt.scatter(window,mean_delta)
#plt.show()

