from bird import Bird
from flappy import Flappy
from utils import generate_random_force
from config import *
import random
import copy

game = Flappy()

def getBest(birds,num):
    """Finner de 'num' beste fuglene i en liste 'birds'"""
    fitnessbirds = [bird.fitness for bird in birds]
    fitnessbirds.sort()
    newbirds = []
    for fitness in fitnessbirds:
        if(len(newbirds)<num):
            bird = [bird for bird in birds if bird.fitness==fitness][0]
            newbirds.append(bird)
    return copy.deepcopy(newbirds)

def getAvgFitness(birds):
    """Finner og returnerer den gjennomsnittlige fitnessen i en liste katter"""
    s = sum([bird.fitness for bird in birds])
    return s/len(birds)

def getBestHalf(birds):
    """Finner og returnerer en scramblet liste av de kattegenene med best(lavest) fitness.
    
    Sletter først den dårligste halvdelen, supplerer så opp til maksgrensa med "gode katter" og returnerer en scramblet liste"""
    avg = getAvgFitness(birds) #Finner gjennomsnittsfitnessen i lista over katter
    birds = [bird for bird in birds if bird.fitness>avg] #Lager en liste over katter med fitness mindre enn gjennomsnittet
    #birds = getSorted(birds)[:int(len(birds)/num)]
    newbirds = [] 
    #import pdb;pdb.set_trace()
    while(len(newbirds)<MAX_POPULATION): #Mens det er plass til flere katter
        newbirds += copy.deepcopy(birds)  #Legger til en kopi av 'birds' lista til 'newbirds'
    newbirds = newbirds[:MAX_POPULATION]  #Omdefinerer seg selv med avgrensing og kutter av de kattene med indeks over MAX_POP
    #copy.deepcopy(birds) + copy.deepcopy(birds)
    random.shuffle(newbirds) #Blander rekkefølger på 'newbirds' listen.
    return newbirds

def mixTwo(birdone,birdtwo):
    """Blander genene til to genvarianter
    
    Tar en slice av genene til to varianter og bytter dem mellom kattene.
    """
    oldgenesone = birdone.genes
    oldgenestwo = birdtwo.genes
    birdone.genes = []
    birdtwo.genes = []
    pos = random.randint(0,len(oldgenesone)) #Lager tilfeldig tall 'pos' mellom 0 og antall gener
    pos2 = random.randint(pos,len(oldgenesone)) #Lager tilfeldig tall mellom 'pos' og antall gener
    #import pdb;pdb.set_trace()
    birdone.genes = oldgenesone[:pos] + oldgenestwo[pos:pos2] + oldgenesone[pos2:] #Lagrer birdone sine gener som sine egne frem til 'pos' birdtwo sine i intervallet 'pos':'pos2' og sine egne fra 'pos2' til slutten av sekvensen igjen
    birdtwo.genes = oldgenestwo[:pos] + oldgenesone[pos:pos2] + oldgenestwo[pos2:] 

    return birdone,birdtwo
    
def doMutate(birds):
    """Muterer ett gen i alle kattenes gener ved å tilordne en tilfeldig generert genverdi i en av posisjonene"""
    for bird in birds:
        gene_num = random.randint(0,len(bird.genes)-1)
        bird.genes[gene_num] = [random.randint(-4,4),random.randint(-4,4)]
        #randlist = []
        #for i in range(0,random.randint(0,100)):
        #    r = random.randint(0,len(bird.genes)-1)
        #    randlist.append(r)
        
        #for i in randlist:
        #    gene_num = random.randint(0,len(bird.genes)-1)
        #    bird.genes[gene_num] = [random.randint(-4,4),random.randint(-4,4)]
    

    return birds
    #import pdb;pdb.set_trace()

def doMixUp(birds):
    """Tar en liste 'birds' og blander en slice av genene til annenhver fugl. Returnerer den modifiserte lista"""
    newbirds = []
    for i in range(0,len(birds),2): #For i = annenhver index i 'birds'(0,2,4, etc)
        try:
            birdone = birds[i]    #Velger en katt ved index i
            birdtwo = birds[i+1]  #og en ved i+1
            birdone,birdtwo = mixTwo(birdone,birdtwo) #Bytter om en slice av genene på de to
            newbirds.append(birdone) #Legger dem til i en ny liste
            newbirds.append(birdtwo)
        except IndexError:
            pass
    return newbirds #Returnerer en liste over kattene med modifiserte gener

@game.register_ai
def super_ai(birds):
    """Super AI Funksjon!
    
    Tar en liste 'bird' objekter som argument og returnerer en liste 'bird' objekter
    Funksjonen tar et utdrag av de 10 beste fuglene fra forrige generasjon og tar disse med videre.
    Av de 90 resterende blir halvparten skrapet, og den andre halvparten klonet og mutert. De 10 beste fra forrige blir så lagt til lista igjen.
    """
    counter=0
    for bird in birds:
        if bird.winner:
            counter+=1
    print(f"Winners from last round: {counter}")

    bestBirds = getBest(birds,10)
    birds = getBestHalf(birds)
    birds = doMixUp(birds)
    birds = doMutate(birds)
    birds = bestBirds + birds
    birds = birds[:MAX_POPULATION]
    return birds

game.start()
