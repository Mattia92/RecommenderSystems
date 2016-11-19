# coding=utf-8
# Un idea può essere creare il dizionario user-items e ciclare sugli user per vedere qual è il massimo numero
# di interazioni e il numero medio di interazioni
# Se un user ha numero interazioni sotto la media si prende la predizione dell'item based mentre se è sopra si
# può uare quella dello user based


# Un'altra idea è: http://www.sciencedirect.com/science/article/pii/S0957417404000910 capitolo 4


# Si deve usare anche un content base per calcolare user-user similarity e item-item similarity
# basandosi sui dati nei rispettivi profile
# Successivamente si aggiornano le similarity --> sim(i,j) = w * sim1(i,j) + (w-1) * sim2(i,j)
# KNN = 30 oppure KNN = 50