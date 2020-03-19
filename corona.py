"""
Functies gebruikt voor vb SIR model

Ingmar Nopens
"""
# Importeren van functionaliteiten
import matplotlib.pyplot as plt
#import seaborn as  sns
import numpy as np
import pandas as pd

from scipy.integrate import odeint



# ----------------------------
# Implementatie  populatie model
# ----------------------------

def model_afgeleiden(variables, t, beta, gamma):

    S = variables[0]
    I = variables[1]
    R = variables[2]
    
    S_new = -beta*I*S 
    I_new = beta*I*S - gamma*I
    R_new = gamma*I
    return [S_new, I_new, R_new]

def populatie_model(tijdstappen, S_0, I_0, R_0, beta, gamma, returnDataFrame=True, plotFig=True):
    """
    Modelimplementatie van het populatiemodel 
    
    Parameters
    -----------
    tijdstappen : np.array
        array van tijdstappen          
    """
    modeloutput = odeint(model_afgeleiden, [S_0, I_0, R_0], tijdstappen, args=(beta, gamma));
    modeloutput = pd.DataFrame(modeloutput, columns=['S','I','R'], index=tijdstappen)
    if plotFig:
        modeloutput.plot()
    if returnDataFrame:
        return modeloutput    

# ----------------------------
# Model optimalisatie functies
# ----------------------------
def SSE(gemeten, model):
    """
    Functie om de Sum of Squared Errors (SSE) te berekenen tussen een set van gemeten en gemodelleerde waarden.

    Parameters
    -----------
    gemeten : np.array
        numpy array van lengte N, met de gemeten waarden
    model : np.array
        numpy array van lengte N, met de gemodelleerde waarden

    Notes
    -----
    We werken hier niet met de DataFrame-structuur, maar gewoon met 2 getallenreeksen. De gebruiker is verantwoordelijk dat
    de gemeten en gemodelleerde waardne overeenstemmen
    """
    residuals = gemeten.flatten() - model.flatten()
    return np.sum(residuals**2)

# ------------------------------
# Model sensitiviteiten functies
# ------------------------------
def abs_sensitiviteit(tijd, model, parameternaam, pert, args):
    """
    Berekent de gevoeligheidsfunctie(s) van de modeloutput(s) naar één bepaalde parameter
    
    Argumenten
    -----------
    tijd : np.array
        array van tijdstappen
    model : function (geen stringnotatie!)
        naam van het model
    parameternaam : string
        naam van de parameter waarvoor de gevoeligheidsfunctie moet opgesteld worden
    args : dictionairy
        alle parameterwaarden die het model nodig heeft
    """

    perturbatie=pert
    
    parameterwaarde = args[parameternaam]
    args[parameternaam]= parameterwaarde + parameterwaarde*perturbatie
    populatie_hoog = model(tijd,args['S_0'],args['I_0'],args['R_0'],args['beta'],args['gamma'], plotFig=False);
    args[parameternaam]= parameterwaarde - parameterwaarde*perturbatie
    populatie_laag = model(tijd,args['S_0'],args['I_0'],args['R_0'],args['beta'],args['gamma'], plotFig=False);
    
    sens = (populatie_hoog - populatie_laag)/(2.*perturbatie*parameterwaarde)
    
    return sens
  
    
    
def rel_sensitiviteit_par(tijd, model, parameternaam, pert, args):
    """
    Berekent de gevoeligheidsfunctie(s) van de modeloutput(s) naar één bepaalde parameter
    
    Argumenten
    -----------
    tijd : np.array
        array van tijdstappen
    model : function (geen stringnotatie!)
        naam van het model
    parameternaam : string
        naam van de parameter waarvoor de gevoeligheidsfunctie moet opgesteld worden
    args : dictionairy
        alle parameterwaarden die het model nodig heeft
    """

    perturbatie=pert
    
    parameterwaarde = args[parameternaam]
    args[parameternaam]= parameterwaarde + parameterwaarde*perturbatie
    populatie_hoog = model(tijd,args['S_0'],args['I_0'],args['R_0'],args['beta'],args['gamma'], plotFig=False);
    args[parameternaam]= parameterwaarde - parameterwaarde*perturbatie
    populatie_laag = model(tijd,args['S_0'],args['I_0'],args['R_0'],args['beta'],args['gamma'], plotFig=False);
    
    sens = (populatie_hoog - populatie_laag)/(2.*perturbatie*parameterwaarde)*(parameterwaarde)
    
    return sens 
    
def rel_sensitiviteit_var(tijd, model, parameternaam, pert, args):
    """
    Berekent de gevoeligheidsfunctie(s) van de modeloutput(s) naar één bepaalde parameter
    
    Argumenten
    -----------
    tijd : np.array
        array van tijdstappen
    model : function (geen stringnotatie!)
        naam van het model
    parameternaam : string
        naam van de parameter waarvoor de gevoeligheidsfunctie moet opgesteld worden
    args : dictionairy
        alle parameterwaarden die het model nodig heeft
    """

    perturbatie=pert
    
    parameterwaarde = args[parameternaam]
    args[parameternaam]= parameterwaarde
    populatie_gewoon = model(tijd,args['S_0'],args['I_0'],args['R_0'],args['beta'],args['gamma'], plotFig=False);
    args[parameternaam]= parameterwaarde + parameterwaarde*perturbatie
    populatie_hoog = model(tijd,args['S_0'],args['I_0'],args['R_0'],args['beta'],args['gamma'], plotFig=False);
    args[parameternaam]= parameterwaarde - parameterwaarde*perturbatie
    populatie_laag = model(tijd,args['S_0'],args['I_0'],args['R_0'],args['beta'],args['gamma'], plotFig=False);
    
    sens = (populatie_hoog - populatie_laag)/(2.*perturbatie*parameterwaarde)/(populatie_gewoon)
    
    return sens  
    
def rel_sensitiviteit_tot(tijd, model, parameternaam, pert, args):
    """
    Berekent de gevoeligheidsfunctie(s) van de modeloutput(s) naar één bepaalde parameter
    
    Argumenten
    -----------
    tijd : np.array
        array van tijdstappen
    model : function (geen stringnotatie!)
        naam van het model
    parameternaam : string
        naam van de parameter waarvoor de gevoeligheidsfunctie moet opgesteld worden
    args : dictionairy
        alle parameterwaarden die het model nodig heeft
    """

    perturbatie=pert
    
    parameterwaarde = args[parameternaam]
    args[parameternaam]= parameterwaarde
    populatie_gewoon = model(tijd,args['S_0'],args['I_0'],args['R_0'],args['beta'],args['gamma'], plotFig=False);
    args[parameternaam]= parameterwaarde + parameterwaarde*perturbatie
    populatie_hoog = model(tijd,args['S_0'],args['I_0'],args['R_0'],args['beta'],args['gamma'], plotFig=False);
    args[parameternaam]= parameterwaarde - parameterwaarde*perturbatie
    populatie_laag = model(tijd,args['S_0'],args['I_0'],args['R_0'],args['beta'],args['gamma'], plotFig=False);
    
    sens = (populatie_hoog - populatie_laag)/(2.*perturbatie*parameterwaarde)*(parameterwaarde/populatie_gewoon)
    
    return sens     

figsize=(9,6)

def model(tijdstappen, init, varnames, f, returnDataFrame=False,
          plotresults=True, **kwargs):
    """
    Modelimplementatie
    Parameters
    -----------
    tijdstappen: np.array
        array van tijdstappen
    init: list
        lijst met initiele condities
    varnames: list
        lijst van strings met namen van de variabelen
    f: function
        functie die de afgeleiden definieert die opgelost moeten worden
    returnDataFrame: bool
        zet op True om de simulatiedata terug te krijgen
    kwargs: dict
        functie specifieke parameters
    """
    fvals = odeint(f, init, tijdstappen, args=(kwargs["beta"],kwargs["gamma"]))
    data = {col:vals for (col, vals) in zip(varnames, fvals.T)}
    idx = pd.Index(data=tijdstappen, name='Tijd')
    modeloutput = pd.DataFrame(data, index=idx)

    if plotresults:
        fig, ax = plt.subplots(figsize=figsize)
        modeloutput.plot(ax=ax);
    if returnDataFrame:
        return modeloutput

def sensitiviteit(tijdstappen, init, varnames, f, parameternaam,
                  log_perturbatie=-4, soort='absoluut', **kwargs):
    """
    Berekent de gevoeligheidsfunctie(s) van de modeloutput(s) naar 1 bepaalde parameter
    Argumenten
    -----------
    tijdstappen: np.array
        array van tijdstappen
    init: list
        lijst met initiele condities
    varnames: list
        lijst van strings met namen van de variabelen
    f: function
        functie die de afgeleiden definieert die opgelost moeten worden
    parameternaam : string
        naam van de parameter waarvoor de gevoeligheidsfunctie moet opgesteld worden
    perturbatie: float
        perturbatie van de parameter
    kwargs: dict
        functie specifieke parameters
    """
    perturbatie = 10**log_perturbatie
    res_basis = model(tijdstappen, init, varnames, f, returnDataFrame=True,
                     plotresults=False, **kwargs)
    parameterwaarde_basis = kwargs.pop(parameternaam)
    kwargs[parameternaam] = (1 + perturbatie) * parameterwaarde_basis
    res_hoog = model(tijdstappen, init, varnames, f, returnDataFrame=True,
                     plotresults=False, **kwargs)
    kwargs[parameternaam] = (1 - perturbatie) * parameterwaarde_basis
    res_laag = model(tijdstappen, init, varnames, f, returnDataFrame=True,
                     plotresults=False, **kwargs)
    if soort == 'absolute sensitiviteit':
        sens = (res_hoog - res_laag)/(2.*perturbatie)

    if soort == 'relatieve sensitiviteit parameter':
            sens = (res_hoog - res_laag)/(2.*perturbatie)*parameterwaarde_basis

    if soort == 'relatieve sensitiviteit variabele':
        sens = (res_hoog - res_laag)/(2.*perturbatie)/res_basis

    if soort == 'relatieve totale sensitiviteit':
        sens = (res_hoog - res_laag)/(2.*perturbatie)*parameterwaarde_basis/res_basis
    fig, ax = plt.subplots(figsize=figsize)
    sens.plot(ax=ax)
#    ax.set_xlabel('Tijd')
#ax.set_ylabel(soort)
   