import csv 
import scipy as sc  
import numpy as np #numpy do generowania ciągów floatów
import matplotlib.pyplot as graph 
from scipy.stats.stats import kstest 

NUMBER_OF_REPEAT= 100 #ilosc powtorzen symulacji
MATCHES=25  #przyjmowana liczba meczów w sezonie
FIXED_COSTS=16500
VARIABLE_COSTS=700 #koszty zmienne na każde 100 osób

hist_attendance=[]
with open(r'Lokalizacja pliku','r') as csvfile:
    reader = csv.reader (csvfile,delimiter=";")
    for row in reader:
        hist_attendance.append(int(row[1]))

average_attendance=sc.mean(hist_attendance)
sd_attendance=sc.std(hist_attendance)


graph.hist(hist_attendance,bins=5)
graph.xlabel("Liczba widzów na meczach Zaksy - histogram")
graph.show()       


print("\n\nWykonuję test Kolgomorova, by stwierdzić czy liczba widzów na meczach ma rozkład normalny. Wynik:")

Kolmogorov = kstest(hist_attendance, sc.stats.norm.cdf, args=(average_attendance,sd_attendance))
if Kolmogorov[1] > 0.05:
    print ("Wartosc p-value:", Kolmogorov[1], "- nie ma podstaw do odrzucenia hipotezy zerowej o normalnosci rozkładu widzów na meczach\n")
else:
    print("Wartosc p-value:", Kolmogorov[1], "- nalezy odrzucic hipotezę zerową o normalnosci rozkładu widzów na meczach\n")

def season (surplus, average_attendance, matches, ticket_price, fixed_costs, variable_costs, seed):
    
    sc.random.seed(seed) 
   # tworzę listę wypełnioną widownią na poszczególnych meczach 
    attendance=[0]*matches
    
    #wypełniam ją losowymi liczbami z rozkładu 
    for m in range(matches):
        attendance[m]=round(sc.random.normal(average_attendance, sd_attendance), 0)    

    ## przeprowadzam symulację rachunku przepływów pieniężnych klubu w ramach sezonu  
    for k in range (matches):
        vc_units = 0
        vc_units = attendance[k]//100 #liczę ile razy musimy dodać 450 do łącznych kosztów
        surplus = surplus + attendance[k]*ticket_price #łączny przychód dodaję do nadwyżki
        surplus = surplus - fixed_costs-(vc_units*variable_costs) #łączny koszt odejmuję od nadyżki
    return surplus


#model symulacyjny poniżej
def simulation(surplus, ticket_price, number_of_repeat, matches, average_attendance, fixed_costs, variable_costs):
    result = []*number_of_repeat
    loss_count=0
    profit=[]
    loss=[]
    for seed in range(number_of_repeat):
        result.append(season(surplus, average_attendance, matches, ticket_price, fixed_costs, variable_costs, seed))
        if result[seed] < 0:
            loss_count += 1
            loss.append(result[seed])
        if result[seed] > 0:
            profit.append(result[seed])
    average_profit_result = sc.mean(profit)
    average_loss_result = sc.mean(loss)
    probability = loss_count / number_of_repeat
    return [average_profit_result, loss_count, probability, average_loss_result]


profit_list = []
average_loss_list=[]
ticketprice_list = []
lossprobab_list = []
loss_list=[]
surplus_list=[]

for surplus in range (-2000, 10001, 2000):
    for ticket_price in np.arange (12.0, 15.0, 0.1):
        symulacja=simulation(surplus, ticket_price, NUMBER_OF_REPEAT, MATCHES, average_attendance, FIXED_COSTS, VARIABLE_COSTS)
        ticketprice_list.append(ticket_price)
        profit_list.append(symulacja[0])
        loss_list.append(symulacja[1]) 
        lossprobab_list.append(symulacja[2])
        average_loss_list.append(symulacja[3])
        surplus_list.append(surplus)
        print("\nPrzy symulacji opartej o założenia - nadwyżka: ", surplus, "cena biletu: ",  ticket_price, "prawdopodobieństwo uzyskania ujemnego wyniku na koniec sezonu"," wynosi: ", symulacja[2], ".Średni wynik dodatni to: ", symulacja[0], ".")
graph.plot(ticketprice_list,lossprobab_list)
graph.xlabel('Cena biletu')
graph.ylabel('Prawdopodobieństwo uzyskania ujemnego wyniku')
graph.show()

l1 = profit_list[:30]
l2 = profit_list[30:60]
l3 = profit_list[60:90]
l4 = profit_list[90:120]
l5 = profit_list[120:150]
l6 = profit_list[150:180]
l7 = profit_list[180:210]

prof = []
for i in range(30):
    if i == 29:
        break
    else:
        profit = (l5[i+1]-l5[i])/l5[i]
        prof.append(profit)

        
graph.plot(ticketprice_list[11:30], prof[10:])
graph.xlabel('Cena biltu')
graph.ylabel('% zmiana w zysku względem biletu 10gr tańszego')
graph.show()
#lossprobab_list 
#surplus_list
#profit_list
#average_loss_list


#attendance