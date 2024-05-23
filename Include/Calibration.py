from matplotlib.pylab import*

def Calib(E, Ch, dCh):
   
    sx=0.0 #Declaração de variáveis para simplificar os somatórios 
    sy=0.0 #que são precisos para calcular os paremetros da reta
    sxy=0.0
    sxx=0.0
    syy=0.0
    sinv=0.0

    for i in range(0,len(Ch)): #De acordo com as listas criadas, calcula os somatórios
                                    #que usamos de seguida
        sx+=E[i]/((dCh[i])**2)
        sy+=Ch[i]/((dCh[i])**2)
        sxy+=(E[i]*Ch[i])/((dCh[i])**2)
        sxx+=((E[i])**2)/((dCh[i])**2)
        syy+=((Ch[i])**2)/((dCh[i])**2)
        sinv+= 1/((dCh[i])**2)     
    delta = sinv*sxx - (sx*sx)

    m=(sinv*sxy-sx*sy)/(delta) #Calcula o declive
    b= (sxx*sy-sx*sxy)/(delta) #Calcula a ordenada na origem
    sigma_m = (sinv/delta)**(0.5)#Calcula incerteza associada ao declive
    sigma_b = (sxx/delta)**(0.5) #Calcula incerteza associada à ordenada na origem   

    #print('E (MeV) = (', "{:.6f}".format(1/m), '+-',"{:.6f}".format(
    #    sigma_m/m**2),') x Channel + (',"{:.6f}".format(b/m), '+-', "{:.6f}".format(
    #        ((sigma_b/m)**2+(b*sigma_m/m**2)**2)**0.5), ')')
 
    return 1/m, b/m, sigma_m/m**2, ((sigma_b/m)**2+(b*sigma_m/m**2)**2)**0.5