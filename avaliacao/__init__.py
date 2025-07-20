#!/usr/bin/env python3
# coding: utf-8

from copy import copy

import itertools
import numpy           as np
import pandas          as pd
import scipy.stats     as st
import statsmodels.api as sm

# Procedimento Stepwise
def stepwise(modelo, X, Y):
    X_sw      = copy(X)
    modelo_sw = copy(modelo)
    
    # Set significance level
    alpha = 0.05
    
    while True:
        # Get p-values for all predictors
        p_values = modelo_sw.pvalues[1:]  # Exclude the constant term
        
        # Find the predictor with the highest p-value
        max_p_value = np.max(p_values)
        
        # If the highest p-value is greater than the significance level, remove the predictor
        if max_p_value > alpha:
            removed_feature_index = np.argmax(p_values) + 1
            
            X_sw = X_sw.drop(X_sw.columns[removed_feature_index], axis=1)
            
            # Refit the model
            modelo_sw = sm.OLS(Y, X_sw).fit()
        else:
            break
    return modelo_sw

# Função para Cálculo das Transformadas
def transformada(n, valor):
    if n == 0:
        resultado = valor
    elif n == 1:
        resultado = np.reciprocal(valor)
    elif n == 2:
        resultado = np.log(valor)
    elif n == 3:
        resultado = valor.pow(2)
    elif n == 4:
        resultado = np.sqrt(valor)
    elif n == 5:
        resultado = 1/valor.pow(2)
    elif n == 6:
        resultado = np.sqrt(np.reciprocal(valor))
    return(resultado)

def transformada_print(n):
    if n == 0:
        resultado = "x"
    elif n == 1:
        resultado = "1/x"
    elif n == 2:
        resultado = "ln(x)"
    elif n == 3:
        resultado = "x²"
    elif n == 4:
        resultado = "√x"
    elif n == 5:
        resultado = "1/x²"
    elif n == 6:
        resultado = "√(1/x)"
    return(resultado)

def comb_print(comb):
    resultado = ""
    for transf in comb:
        resultado += " - " + transformada_print(transf)
    return resultado

# Função para Montar as Combinações¶
# Esta função monta as possíveis combinações de 0 até combN para cada coluna de
# amostra. Em um computador de 16GB de memória RAM, o limite de combinações foi
# de 2x25.
def comb_amostra(amostra, combN = 7):
    
    combs = list(itertools.product(range(combN), repeat=len(amostra.columns)))
    
    return combs

# Função para transformar a amostra de acordo com as combinaçãoes combs.
def amostra_transformada(amostra, combs):
    amostra_transf = []
    combi = 0
    for comb in combs:
        combi += 1
        print('\r comb = {0}'.format(combi), end='', flush=True)
        for i in range(len(amostra.columns)):
            if i == 0:
                coluna_transf = pd.DataFrame(transformada(comb[i], amostra.iloc[:, i]))
            else:
                coluna_transf = coluna_transf.join(transformada(comb[i], amostra.iloc[:, i]))
        coluna_transf = pd.DataFrame(coluna_transf)
        coluna_transf.columns = amostra.columns
        # coluna_transf = coluna_transf.replace([np.inf, -np.inf], np.nan).dropna()
        coluna_transf = coluna_transf.replace([np.inf, -np.inf], np.nan).fillna(0)
        amostra_transf.append(coluna_transf)
        
    return amostra_transf

# Função para Remover os Dados Discrepantes
# Esta função remove os dados com resíduos padronizados maiores do que residMax
# de uma amostra em um modelo até atingir um Coeficiente de Determinação R²
# igual a R2_alvo ou até atingir os limites de quantidade de remoção de outliers
# out_lim ou de conv_lim.
def exclui_outlier(amostra, modelo, amostra_orig, ycolN = 'Unitario', R2_alvo = 0.75, out_lim = 0.5, conv_lim = 0.5, residMax = 2):
    out_n  = int(out_lim  * len(amostra.index))
    conv_n = int(conv_lim * out_n)
    
    conv_i   = 0
    modelo   = sm.OLS(amostra[ycolN], sm.add_constant(amostra.drop([ycolN], axis=1))).fit()
    R2_velho = modelo.rsquared
    for i in range(out_n):
        influence = modelo.get_influence()
        resid_pad = influence.resid_studentized_internal
        resid_max = max(abs(resid_pad))
        if resid_max < residMax:
            print('Resíduo Padrão Máximo atingido!')
            print(i)
            break
        index   =  list(abs(resid_pad)).index(resid_max)
        # resid_max = max(abs(modelo.resid))
        # index   =  list(abs(modelo.resid)).index(resid_max)
        amostra = amostra.drop(index)
        amostra_orig = amostra_orig.drop(index)
        amostra = amostra.reset_index(drop=True)
        amostra_orig = amostra_orig.reset_index(drop=True)
        modelo  = sm.OLS(amostra[ycolN], sm.add_constant(amostra.drop([ycolN], axis=1))).fit()
        R2_novo = modelo.rsquared
        if (R2_novo < R2_velho):
            if (conv_i == conv_n):
                print('Quantidade de outliers excluídos:')
                print(i+1)
                print('Exclusão dos outliers não convergiu!')
                break
            else:
                conv_i = conv_i + 1
        else:
            R2_velho = R2_novo
    
        if R2_novo >= R2_alvo:
            print('Quantidade de outliers excluídos:')
            print(i+1)
            break
    
    return amostra, modelo, amostra_orig, i+1

# Função para Contar os Resíduos Discrepantes
# Esta função conta os resíduos maiores do que residMax em um modelo.
def cont_resid(modelo, residMax = 3):
    
    influence = modelo.get_influence()
    resid_pad = influence.resid_studentized_internal
    cont_pad = 0
    for n_pad in resid_pad:
        v_pad = abs(n_pad)
        if v_pad > residMax:
            cont_pad += 1
    
    return cont_pad


def dist_resid(modelo):
    z_scores = st.zscore(modelo.resid)
    z_tot = len(z_scores)
    i196 = i164 = i1 = 0
    for z_score in z_scores:
        if (z_score >= -1) & (z_score <= 1):
            i1 += 1
        if (z_score >= -1.64) & (z_score <= 1.64):
            i164 += 1
        if (z_score >= -1.96) & (z_score <= 1.96):
            i196 += 1
    
    return print("{0:.1%} (68%) - {1:.1%} (90%) - {2:.1%} (95%)".format(i1/z_tot, i164/z_tot, i196/z_tot))

