pso<-function(f, dim, popSize, maxIter, coor, minWsp, maxWsp){
  #f - minimalizowana funkcja
  #dim - wymiar funkcji z R(dim) do R
  #popSize - liczba zmiennych w populacji stada
  #maxIter - liczba iteracji
  #coor - wektor wsp�czynnik�w
  #minWsp, maxWsp - maksymalny rozmiar obszaru poszukiwanego (z tych wsp�rz�dnych losujemy punkty
  #w przedziale od minWsp do maxWsp na ka�dej wsp�rz�dnej)
  
  p_actual <- matrix(NA, nrow=popSize, ncol=dim)
  p_best <- matrix(NA, nrow=popSize, ncol=dim)
  velocity <- matrix(NA, nrow=popSize, ncol=dim)
  g_best <- rep(NA, dim)
  minWsp<-(-20)
  maxWsp<-20
  #losowanie losowych parametr�w dla "pr�dko�ci"
  random_ind<-runif(2)
  #random_ind
  
  ##wype�nienie kolumn macierzy pierwszymi wylosowanymi jednostkami
  for (i in 1:popSize){
    p_actual[i,]<-runif(dim, minWsp, maxWsp)
  }
  p_best<-p_actual
  
  ##wyznaczenie warto�ci minimalnej w populacji pocz�tkowej
  g_best<-p_actual[1,]
  for (i in 2:popSize){
    if(f(p_actual[i,])<f(g_best)){
      g_best<-p_actual[i,]
    }
  }
  
  ##wype�nienie macierzy pr�dko�ci losowymi warto�ciami od 0 do 1
  for (i in 1:popSize){
    velocity[i,]<-runif(dim, 0, 1)
  }

  curIter<-0
  result <- list(x_opt = g_best, f_opt = f(g_best), x_hist = g_best, f_hist = f(g_best), tEval = 0, iter = 0)
  while(curIter<maxIter){
    StartT <- Sys.time()
    #aktualizacja warto�ci macierzy pr�dko�ci
    for (i in 1: popSize){
        velocity[i,]<-coor[1]*velocity[i,]+coor[2]*random_ind[1]*(p_best[i,]-p_actual[i,])
        +coor[3]*random_ind[2]*(g_best-p_actual[i,])
    }
    #aktualizacja warto�ci macierzy po�o�enia i sprawdzenie czy wyst�puje nowa, "lepsza" warto��
    p_actual<-p_actual+velocity
    for (i in 1: popSize){
      if (f(p_actual[i,])<f(p_best[i,])){
        p_best[i,] <- p_actual[i,]
      }
      if (f(p_actual[i,])<f(g_best)){
        g_best <- p_actual[i,]
      }
      
    }
    result$x_opt <- g_best
    result$f_opt <- f(g_best)
    result$x_hist <- rbind(result$x_hist, g_best)
    result$f_hist <- rbind(result$f_hist, f(g_best))
    result$iter   <- curIter
    result$tEval   <- rbind(result$tEval, Sys.time() - StartT)
    curIter=curIter+1
  }
  return(result)
}