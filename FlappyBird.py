import pygame
import random
import random as rd
import  numpy as np
pygame.init()
width,height=500,500
screen=pygame.display.set_mode((width,height))
game_over=False
clock=pygame.time.Clock()
fps=30
p_width=50
gap=100
b_dim=30
p_up_height=350
pipeup=pygame.image.load('pipe2.png')
pipeup_re=pygame.transform.scale(pipeup,(p_width,p_up_height))
pipelow=pygame.image.load('pipe1.png')
pipelow_re=pygame.transform.scale(pipelow,(p_width,p_up_height))
maxpop=100
bgr=pygame.image.load('bgr1.png')
bgr=pygame.transform.scale(bgr,(width,height))
birdimg=pygame.image.load('bird1.png')
birdimg=pygame.transform.scale(birdimg,(b_dim,b_dim))
class FlappyBird:
    def __init__(self,weights1,weights2,weights3):
        self.weights1=weights1
        self.weights2=weights2
        self.weights3=weights3
        self.posx=50
        self.posy=height//2 -100
        self.jumpheight=15
        self.lost=False
        self.img=birdimg
        self.score=0#based on lifetime
        self.gravity=30

    def draw(self,input_data):
        hiden_layer_output = input_data.dot(self.weights1)
        hiden_layer_output2 = hiden_layer_output.dot(self.weights2)
        final_output = hiden_layer_output2.dot(self.weights3)
        big=max(final_output)
        click=0
        for i in range(2):
            if big==final_output[i]:
                click=i
                break
        if click==0:
            self.posy-=self.jumpheight
        else:
            self.posy+=self.gravity
        #drawing
        screen.blit(self.img,(self.posx,self.posy))
#biology
def weight_generator():
    weight1=np.random.randint(-100,100,size=(6,3)).T
    weight2=np.random.randint(-100,100,size=(3,6)).T
    weight3=np.random.rand(3,2)
    return weight1,weight2,weight3
def populate(maxpop):
    generationlist=[]
    for i in range(maxpop):
        weights1,weights2,weights3=weight_generator()
        tempbird=FlappyBird(weights1,weights2,weights3)
        generationlist.append(tempbird)
    return generationlist
birds=populate(maxpop)###############################################################
def reproduction(pre_gen):
    #fitness
    fitnesslist = []
    for i in range(len(pre_gen)):
        fitnesslist.append(pre_gen[i].score)
    # top3 selection
    top3 = []
    for i in range(3):
        top3.append(pre_gen[fitnesslist.index(max(fitnesslist))])
        fitnesslist[fitnesslist.index(max(fitnesslist))] = -1
    generationlist=[]
    for i in range(len(pre_gen)):
        while True:
            rd1 = rd.randint(0, len(top3) - 1)
            rd2 = rd.randint(0, len(top3) - 1)
            if rd1 != rd2:
                break
            else:
                break
        mutationprob = 2
        md = rd.randint(0, 10)
        # learning_rate = 0.01
        mutaion_will_happen = False
        if md < mutationprob:
            mutaion_will_happen = True

        parent1 = top3[rd1]
        parent2 = top3[rd2]
        w1 = []
        for j in parent1.weights1.T:
            w1.append(list(j))
        w2 = []
        for j in parent2.weights1.T:
            w2.append(list(j))
        wlength = len(w1)
        part1 = wlength // 2
        result_weight1list = w1[0:part1] + w2[part1:wlength]
        # mutation 1
        if mutaion_will_happen:
            ft=1
            for m in range(random.randint(4,80)):
                result_weight1list[rd.randint(0, len(result_weight1list) - 1)][
                rd.randint(0, len(result_weight1list[0]) - 1)] += rd.randint(-100,100)*ft
                if m%2==0:
                    ft=-1
                else:
                    ft=1
        result_weight1array = np.array(result_weight1list).T
        hw1 = []
        for j in parent1.weights2.T:
            hw1.append(list(j))
        hw2 = []
        for j in parent2.weights2.T:
            hw2.append(list(j))
        hwlength = len(w1)
        hpart1 = hwlength // 2
        hresult_weight1list = hw1[0:hpart1] + hw2[hpart1:hwlength]
        # mutaion 2
        if mutaion_will_happen:
            hresult_weight1list[rd.randint(0, len(hresult_weight1list) - 1)][
                rd.randint(0, len(hresult_weight1list[0]) - 1)] = rd.randint(-100,100)
            hresult_weight1list[rd.randint(0, len(hresult_weight1list) - 1)][
                rd.randint(0, len(hresult_weight1list[0]) - 1)] = rd.randint(-100,100)
            hresult_weight1list[rd.randint(0, len(hresult_weight1list) - 1)][rd.randint(0,len(hresult_weight1list[0])-1)] = rd.randint(-100,100)
            hresult_weight1list[rd.randint(0, len(hresult_weight1list) - 1)][rd.randint(0,len(hresult_weight1list[0])-1)] = rd.randint(-100,100)
        hresult_weight1array = np.array(hresult_weight1list).T
        hw2_1 = []
        for j in parent1.weights3.T:
            hw2_1.append(list(j))
        hw2_2=[]
        for j in parent2.weights3.T:
            hw2_2.append(list(j))
        hwlength = len(hw2_1)
        hpart1 = hwlength // 2
        hresult_weight2list = hw2_1[0:hpart1] + hw2_2[hpart1:hwlength]
        if mutaion_will_happen:
            ft=1
            for m in range(random.randint(4,15)):
                hresult_weight2list[random.randint(0, len( hresult_weight2list ) - 1)][
                random.randint(0, len( hresult_weight2list [0]) - 1)] += random.random()*ft
                if m%2==0:
                    ft=-1
                else:
                    ft=1
        hresult_weight2array=np.array(hresult_weight2list).T
        # child creation
        babybird = FlappyBird(result_weight1array, hresult_weight1array,hresult_weight2array)
        generationlist.append(babybird)
    # top3[0].score=0
    return generationlist
def show_text(gen_no,score):
    font = pygame.font.Font('freesansbold.ttf', 15)
    text = font.render(f' Generation: {gen_no} , best score: {score} ', True, (255, 0, 0))
    textRect = text.get_rect()
    textRect.center = (235,30)
    screen.blit(text, textRect)
death=0
posx=width
posy_up=random.randint(-280,0)
posy_low=posy_up+p_up_height+gap
p_speed=10
score=0
genno=1

gen_score=[]

grand_score=[]

while not game_over:
    screen.fill((255,255,255))
    screen.blit(bgr,(0,0))
    for events in pygame.event.get():
        if events.type==pygame.QUIT:
            game_over=True
    posx-=p_speed
    if posx+p_width<0:
        posx=width
        posy_up = random.randint(-280, 0)
        posy_low = posy_up + p_up_height + gap
        score+=1
    def drawpipies():
        screen.blit(pipeup_re,(posx,posy_up))
        screen.blit(pipelow_re,(posx,posy_low))
    def draw_birds():
        global death
        for i in birds:
            ##inputs
            if not i.lost:
                h_dist=posx-i.posx
                v_dis_up=i.posy - posy_up+p_up_height
                v_dis_low=posy_low-i.posy-50
                inputs=np.array([h_dist,v_dis_up,v_dis_low])
                #lost checking
                if i.posy > height:
                    i.lost = True
                    gen_score.append(i.score)
                if i.posy < 0:
                    i.lost = True
                    gen_score.append(i.score)
                if (abs(i.posx+b_dim-posx)<10 or posx-i.posx<0) and  i.posy-(posy_up+p_up_height) <0 :
                    i.lost=True
                    gen_score.append(i.score)
                if (abs(i.posx+b_dim-posx)<10 or posx-i.posx<0) and posy_low-i.posy-b_dim<0:
                    i.lost=True
                    gen_score.append(i.score)
                if not i.lost:
                    i.draw(inputs)
                    i.score+=1

    def isalldied():
       count=0
       for i in birds:
           if i.lost:
               count+=1
       return  count
    show_text(genno,score)
    if isalldied()==len(birds):
        grand_score.append(max(gen_score))
        birds=reproduction(birds)
        genno+=1
        score=0
        death=0
        posx = width
        posy_up = random.randint(-280, 0)
        posy_low = posy_up + p_up_height + gap
    draw_birds()
    drawpipies()
    pygame.display.update()
    clock.tick(fps)
pygame.quit()
n=input("Enter y to see graph: ")
if n=='y':
    xaxis=[]
    for i in range(1,len(grand_score)+1):
        xaxis.append(i)
    import matplotlib.pyplot as plt
    plt.plot(xaxis,grand_score)
    plt.show()

