# %%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st
from scipy.optimize import curve_fit
from scipy.optimize import minimize
from experimentalTreatingIsiPol.machines._68FM100 import _68FM100
from experimentalTreatingIsiPol.machines._68FM100_biaxial import _68FM100_biaxial
from experimentalTreatingIsiPol.machines._older_machine import _Older_Machine
import os
import re
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io  # For working with in-memory files
from matplotlib.backends.backend_pdf import PdfPages


blue_tonalities_options = [
    '#1f0794', 
    '#000080', 
    '#6476d1', 
    '#00008B', 
    '#003366', 
    '#191970', 
    '#0000CD', 
    '#27414a', 
    '#4B0082', 
    '#2f6b6b', 
    '#00688B', 
    '#483D8B', 
    '#4682B4', 
    '#708090', 
    '#4169E1', 
    '#778899', 
    '#7B68EE', 
    '#6495ED'
]


linestyles_options = [
    "-",    # solid
    "--",   # dashed
    "-.",   # dashdot
    ":",    # dotted
    " ",    # no line (blank space)
    "-",    # solid (thicker)
    (0, (1, 10)), # loosely dotted
    (0, (5, 10)), # loosely dashed
    (0, (3, 5, 1, 5)), # dashdotted
    (0, (3, 1, 1, 1)), # densely dashdotted
    (0, (5, 5)),  # dashed with same dash and space lengths
    (5, (10, 3)), # long dashes with offset
    (0, (3, 10, 1, 15)), # complex custom dash pattern
    (0, (1, 1)), # densely dotted
    (0, (1, 5)), # moderately dotted
    (0, (3, 1)), # densely dashed
    (0, (3, 5, 1, 5, 1, 5)), # dashdotdot
    (0, (3, 10, 1, 10, 1, 10)), # dashdashdash
]

marker_options = [
    ".",      # point
    ",",      # pixel
    "o",      # circle
    "v",      # triangle down
    "^",      # triangle up
    "<",      # triangle left
    ">",      # triangle right
    "1",      # tripod down
    "2",      # tripod up
    "3",      # tripod left
    "4",      # tripod right
    "s",      # square
    "p",      # pentagon
    "*",      # star
    "h",      # hexagon1
    "H",      # hexagon2
    "+",      # plus
    "x",      # x
    "D",      # diamond
    "d",      # thin diamond
]

def plot_helper(ax,x,y,label,xlabel,ylabel,color='blue', linestyle='-.', marker='<', markersize=1, linewidth=1,**kwargs):

    ax.plot(x,y, label = label, color = color, marker = marker, 
            markersize = markersize, 
            linestyle = linestyle,
            linewidth = linewidth,**kwargs)
    ax.grid()
    ax.legend()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax

def scatter_helper(ax,x,y,label, xlabel, ylabel,color='blue', marker='+', markersize=10, **kwargs):

    ax.scatter(x,y, label = label, color = color, marker = marker,
             s = markersize,
             **kwargs)
    ax.grid()
    ax.legend()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax

def several_plots_helper(ax,xs,ys,labels,xlabel,ylabel,colors: list | None = None, 
                         linestyles: list | None =None, markers : list | None = None, 
                         markersize=1, linewidth=1, 
                         **kwargs
                         ):
    '''
    Função para plotar diversos gráficos.
    '''
    if len(xs)!=len(ys):
        raise Exception('As dimensões das variáveis xs e ys devem ser iguais.')
    
    if len(labels)!=len(ys):
        raise Exception('A quantidade de labels deve ser igual à quantidade de pares.')
    

    if not (colors and markers and linestyles): 

        for each_x, each_y, each_label in zip(xs,ys,labels): 
            if len(each_x)>100:
                slice = int(len(each_x)/20)
                each_x=each_x[::slice]
                each_y=each_y[::slice]

            color = blue_tonalities_options[np.random.random_integers(0,17)]
            marker = marker_options[np.random.random_integers(0,17)]
            linestyle = linestyles_options[np.random.random_integers(0,17)]

            ax.plot(each_x,each_y, label = each_label, color = color, marker = marker, 
                    markersize = markersize, 
                    linestyle = linestyle,
                    linewidth = linewidth,**kwargs)

    else:
        for each_x, each_y, each_label,each_color, each_marker, each_linestyle in zip(xs,ys,labels,colors,markers,linestyles): 
            if len(each_x)>100:
                slice = int(len(each_x)/20)
                each_x=each_x[::slice]
                each_y=each_y[::slice]

            ax.plot(each_x,each_y, label = each_label, color = each_color, marker = each_marker, 
                    markersize = markersize, 
                    linestyle = each_linestyle,
                    linewidth = linewidth,**kwargs)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid()
    fig_obj = ax.get_figure()
    fig_height = fig_obj.get_figheight()
    ax.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -fig_height/20),
        ncol=3,
        framealpha=1,
        )
    
    return ax

def several_scatter_helper(ax,xs,ys,labels,xlabel,ylabel,colors: list | None = None, linestyles: list | None =None, markers : list | None = None, markersize=1, linewidth=1, **kwargs):
    '''
    Função para plotar diversos gráficos.

    PAREI AQUI
    '''
    if len(xs)!=len(ys):
        raise Exception('As dimensões das variáveis xs e ys devem ser iguais.')
    
    if len(labels)!=len(ys):
        raise Exception('A quantidade de labels deve ser igual à quantidade de pares.')
    
    ax.grid()

    if not (colors and markers and linestyles): 

        for each_x, each_y, each_label in zip(xs,ys,labels): 

            if len(each_x)>100:
                slice = int(len(each_x)/20)
                each_x=each_x[::slice]
                each_y=each_y[::slice]

            color = blue_tonalities_options[np.random.random_integers(0,17)]
            marker = marker_options[np.random.random_integers(0,17)]

            ax.scatter(each_x,each_y, label = each_label, color = color, marker = marker, 
                    s = markersize, 
                    **kwargs)

    else:
        for each_x, each_y, each_label,each_color, each_marker in zip(xs,ys,labels,colors,markers): 
           
            if len(each_x)>100:
                slice = int(len(each_x)/20)
                each_x=each_x[::slice]
                each_y=each_y[::slice]

            ax.scatter(each_x,each_y, label = each_label, color = each_color, marker = each_marker, 
                    s = markersize, 
                    **kwargs)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig_obj = ax.get_figure()
    fig_height = fig_obj.get_figheight()
    ax.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -fig_height/15),
        ncol=3,
        framealpha=1,
        )
    
    return ax


class MechanicalTestFittingLinear():
    '''
    Classe para determinar propriedades mecânicas em regimes lineares. Ela servirão para Moduli de Young e Cisalhamento. 
    '''
    def __init__(self, machineName: str, archive_name : str, linearRegionSearchMethod='Deterministic', verbose : bool = True) -> None:
        self.verbose = verbose
        self.rawdata, self.cleaned_raw_data = self.dataExtract(machineName=machineName, archive_name= archive_name, linearRegionSearchMethod=linearRegionSearchMethod)
        self.machineName = machineName
        pass

    def _68FM100_Data_Aquisition(self, archive_name : str, linearRegionSearchMethod):
        '''
        Método para a leitura e aquisição de dados de ensaio efetuados na 68FM100
        '''
        machine  = _68FM100() # Instanciando um novo objeto do tipo Instron 
        raw_data = pd.read_csv(archive_name, sep=machine.column_delimitador, encoding_errors='backslashreplace', on_bad_lines='skip', skiprows=10, decimal=machine.decimal)
        raw_data.columns = machine.colunas
        x = raw_data[machine.colunas[4]]/100 # por conta da percentagem
        y = raw_data[machine.colunas[3]]
        self.__generalDataAquisition(x=x,y=y, x_label=machine.colunas[4], y_label=machine.colunas[3], linearRegionSearchMethod=linearRegionSearchMethod)
        return raw_data
    
    def _68FM100_biaxial_Data_Aquisition(self, archive_name : str, linearRegionSearchMethod):
        '''
        Método para a aquisição de dados dos testes biaxiais
        '''
        machine =  _68FM100_biaxial()
        raw_data = pd.read_csv(archive_name, sep=machine.column_delimitador, encoding_errors='backslashreplace', on_bad_lines='skip', skiprows=3, decimal=machine.decimal)
        raw_data.columns = machine.colunas
        raw_data = raw_data.dropna(axis=0) # remove linhas com na
        
        x = raw_data[machine.colunas[4]]/100 # porque está em %
        y = raw_data[machine.colunas[3]]

        new_x, new_y  = self.__generalDataAquisition(x=x,y=y,
                                      x_label=machine.colunas[4], 
                                      y_label=machine.colunas[3], 
                                      linearRegionSearchMethod=linearRegionSearchMethod)
        
        cleaned_raw_data = raw_data[raw_data[machine.colunas[3]]>new_y[0]]

        return raw_data, cleaned_raw_data


    def _olderMachine_Data_Aquisition(self, archive_name :  str, linearRegionSearchMethod):
        '''
        Method to analyse data of the older machine (the one used before instron arrived)
        '''

        machine  = _Older_Machine() # Instanciando um novo objeto do tipo _Older_Machine 
        raw_data = pd.read_csv(archive_name, sep=machine.column_delimitador, encoding_errors='backslashreplace', on_bad_lines='skip', skiprows=10, decimal=machine.decimal)
        raw_data.columns = machine.colunas
        offset_num = self.__filterInitGraph(y=raw_data[machine.colunas[2]],linearRegionSearchMethod=linearRegionSearchMethod)
        x = raw_data[machine.colunas[3]]
        y = raw_data[machine.colunas[2]]
        x_linear = self.__selectGraphRange(x,offset_num)
        y_linear = self.__selectGraphRange(y,offset_num)

        a,b,root = self.__equationFit(x_linear, y_linear)
        self.plotDataFinalComparison(x,y,x_linear,y_linear,machine.colunas[3],machine.colunas[2])
        self.plotComparisonExcludedData(x,y,x_linear,y_linear,machine.colunas[3],machine.colunas[2])

        new_x, new_y = self.__cut_garbage_data(x,y,x_linear,a,b,root)
        self.plotCleanedData(new_x, new_y, machine.colunas[3],machine.colunas[2])

        self.new_x = new_x # Salvando internamente os dados limpos (x)
        self.new_y = new_y # Salvando internamente os dados limpos (y)
        return raw_data
    
    def __equationFit(self, x_linear, y_linear):
        '''
        Retorna os coeficientes a, b, e a raiz (-b/a) de uma equaçãoo linear f(x)=ax+b
        '''
        def linear(x,a,b):
            return a*x+b

        popt,_ = curve_fit(linear, x_linear, y_linear)
        return tuple([popt[0],popt[1],-popt[1]/popt[0]])
    
    def __cut_garbage_data(self,x,y,x_linear,a,b,root):
        '''
        Método para cortar os dados iniciais do ensaio
        x -> Dados Originais (x)
        y -> Dados Originais (y)
        x_linear -> Conjunto do eixo x, dos dados originais, em que a informação é válida
        a,b -> Coef. das retas ajustadas na região linear
        root -> Raiz da eq. ajustada na parte linear
        '''

        x_cleaned = x[len(x_linear):len(x)] # Exclui os primeiros dados
        y_cleaned = y[len(x_linear):len(x)] # Exclui os primeiros dados
        x_init = np.linspace(root,x[len(x_linear)],20) # Array da raiz do gráfico até o início dos dados originais
        y_init = [a*x+b for x in x_init] # Y ajustado na parte linear
        
        new_x = list(x_init) + list(x_cleaned) 
        new_x = np.subtract(new_x,root) # descontando a raiz
        new_y = list(y_init) + list(y_cleaned)
        return new_x, new_y
    
    def __selectGraphRange(self, var, i):
        '''
        Método para retornar um range de dados, dado seu tamanho, e posição. 
        '''
        offset = int(len(var)/50)
        return var[offset*(i-1):offset+offset*(i-1)]
     
    def __findConvergencePoisson(self, x_strain_linear, y_strain_linear, x_load_linear):
        '''
        Método para encontrar a convergênci da razão de Poisson
        '''
        # Corta os dados no mesmo tamanho
        if len(x_strain_linear)>len(y_strain_linear):
            x_strain_linear = x_strain_linear[0:len(y_strain_linear)]
        else:
            y_strain_linear = y_strain_linear[0:len(x_strain_linear)]

        ratio = np.divide(y_strain_linear,x_strain_linear)
        ratio_inverted = ratio[::-1]

        convergedRatio = self.__selectGraphRange(ratio_inverted,1)

        return np.mean(convergedRatio)
    
    def __filterInitGraph(self, y : pd.Series, linearRegionSearchMethod: str = 'Deterministic')->int:
        '''
        Recebe os dados de ensaios experimentais, e encontra a primeira região linear pela diminuição do desvio padrão da segunda derivada
        '''
        if linearRegionSearchMethod == 'Deterministic':
            i=1
            y_current = self.__selectGraphRange(y,i)
            derivative = np.gradient(y_current)
            second_order_derivative = np.gradient(derivative)
            init_cov = np.std(second_order_derivative)
            cov = init_cov
            convergence_criteria = init_cov/5

            # Se os dados já estão lineares, não há porque filtrar
            if init_cov<0.01:
                return i #

            while(cov > convergence_criteria):
                i+=1
                y_current = self.__selectGraphRange(y,i)
                derivative = np.gradient(y_current)
                second_order_derivative = np.gradient(derivative)
                cov = np.std(second_order_derivative)
                if i>100:
                    raise Exception('loop inf')

            return i    
        
        raise Exception('Método de determinação da região Linear Inválido')

    def __findEndLinearRegion(self, y : pd.Series):
        '''
        TODO -> Progrmar uma forma de se obter a região linear, ou seja, até onde realizar o fitting para o módulo
        '''
        pass     

    def __findYeldStress(self, x: pd.Series, y: pd.Series, E, method = 'percent', max_percentil : float = 0.25):
        '''
        Metodo para determinar a tensao de escoamento basead em medo
        '''

        if method == 'percent':
            x_offset, y_offset, yieldStress = self.__percentYeldStressMethod(x, y, E, max_percentil)

        return x_offset, y_offset,yieldStress
    
    def __percentYeldStressMethod(self, x: pd.Series, y: pd.Series, E : float, max_percentil : float = 0.25):
        '''
        Metodo para encontrar a tensao de escoamento baseado em um offset de 0.2%
        '''
        x_max = np.quantile(x,max_percentil) #Plotando até o décimo quinto percentil do eixo x
        x_linear = np.linspace(0,x_max,100)
        y_linear = [E*x for x in x_linear]
        x_offset = x_linear + 0.002
        y_interpolated = np.interp(x_offset, x,y)
        def FindYield():
            minGlobal = min(abs(y_interpolated- y_linear))
            for each_i in range(len(y_interpolated)):
                if abs(y_interpolated[each_i]-y_linear[each_i])==minGlobal:
                    return y_interpolated[each_i]
                
        yieldPoint = FindYield()
        
        return x_offset, y_linear, yieldPoint
    def __generalDataAquisition(self, x : pd.Series, y : pd.Series, x_label : str, y_label : str, linearRegionSearchMethod : str):
        '''
        Metodo DRY para executar os comandos referentes a aquisicao de dados
        '''
        offset_num = self.__filterInitGraph(y=y,linearRegionSearchMethod=linearRegionSearchMethod)

        x_linear = self.__selectGraphRange(x,offset_num)
        y_linear = self.__selectGraphRange(y,offset_num)

        a,b,root = self.__equationFit(x_linear, y_linear)
        if self.verbose:
            self.plotDataFinalComparison(x,y,x_linear,y_linear,x_label,y_label)
        if offset_num>1 and self.verbose:
            self.plotComparisonExcludedData(x,y,x_linear,y_linear,x_label,y_label)

        new_x, new_y = self.__cut_garbage_data(x,y,x_linear,a,b,root)
        if self.verbose:
            self.plotCleanedData(new_x, new_y, x_label, y_label)

        self.new_x = new_x # Salvando internamente os dados limpos (x)
        self.new_y = new_y # Salvando internamente os dados limpos (y)

        return new_x, new_y

    def __typeCheck(self, var, type_correct):
        '''
        Função de apoio para checar se o tipo passo estão correto
        '''
        if type(var) != type_correct:
            raise Exception(f'O argumento machineName deve ser uma {type_correct}. Recebeu um {type(var)}')

    def dataExtract(self, machineName : str, archive_name : str, linearRegionSearchMethod : str)->pd.DataFrame:
        '''
        Funçãoo para obter, a parte de um tipo de máquina, identificado pelo nome, os dados brutos do ensaio.
        '''
        # Verificação dos argumentos
        self.__typeCheck(machineName, str)
        self.__typeCheck(archive_name, str)

        if machineName == '68FM100':
            return self._68FM100_Data_Aquisition(archive_name, linearRegionSearchMethod)
        
        if machineName == '_older_machine': # Nome temporário, até conseguir o nome correto da máquina
            return self._olderMachine_Data_Aquisition(archive_name, linearRegionSearchMethod)
        
        if machineName == '68FM100_biaxial':
            return self._68FM100_biaxial_Data_Aquisition(archive_name, linearRegionSearchMethod)
        
        raise Exception('Tipo de Máquina não encontrado')
    
    def MeasureYoungModulus(self,length : float = None,thickess : float = None,width : float = None, max_percentil : float = 0.25):
        '''
        Método para medir o módulo de Young
        '''
        if self.machineName == '68FM100':
            linear_region_strain =  self.new_x[0:10] # Está hardcoded, talvez poderiámos pensar em alguma lógica para calcular o ponto final do cálculo
            linear_region_stress = self.new_y[0:10]
            E,b,root=self.__equationFit(x_linear=linear_region_strain, y_linear=linear_region_stress)
            self.E = E
            self.plotStressStrain(self.new_x,self.new_y,E, max_percentil)
            return
        
        if self.machineName == '68FM100_biaxial':
            linear_region_strain =  self.new_x[0:50] # Está hardcoded, talvez poderiámos pensar em alguma lógica para calcular o ponto final do cálculo
            linear_region_stress = self.new_y[0:50]
            E,b,root=self.__equationFit(x_linear=linear_region_strain, y_linear=linear_region_stress)
            self.E = E

            # plotando os dados em 5 em 5
            slice = int(len(self.new_x)/100)
            x=self.new_x[::slice]
            y=self.new_y[::slice]
            self.plotStressStrain(x,y,E, max_percentil)

        if self.machineName == '_older_machine':

            strain = np.divide(self.new_x, length)
            area = thickess*width
            stress =  np.divide(self.new_y, area)
            linear_region_strain =  strain[0:10] # Está hardcoded, talvez poderiámos pensar em alguma lógica para calcular o ponto final do cálculo
            linear_region_stress = stress[0:10]
            E,b,root=self.__equationFit(x_linear=linear_region_strain, y_linear=linear_region_stress)
            self.plotStressStrain(strain,stress,E)

    def MeasurePoissonRatio(self):
        '''
        Método para medir a razão de poisson
        '''
        if self.machineName == '68FM100_biaxial':
            machineConfig = _68FM100_biaxial()

            # Encontrar a região linear da deformação axial pela carga
            axial_strain =  np.abs(self.cleaned_raw_data[machineConfig.colunas[5]])
            range_axial  = self.__filterInitGraph(axial_strain)
            axial_strain_linear = self.__selectGraphRange(axial_strain, range_axial)

            # Encontrar a região linear da deformação transversal pela carga
            transverse_strain =  np.abs(self.cleaned_raw_data[machineConfig.colunas[6]])
            range_transverse  = self.__filterInitGraph(transverse_strain)
            transverse_strain_linear = self.__selectGraphRange(transverse_strain, range_transverse)

            load = self.cleaned_raw_data[machineConfig.colunas[2]]

            load_linear_axial = self.__selectGraphRange(load, range_axial)
            load_linear_tranversal = self.__selectGraphRange(load, range_transverse)

            self.poisson_ratio = self.__findConvergencePoisson(axial_strain_linear,transverse_strain_linear,load_linear_axial)

            def selectData(data):

                slice = int(len(data)/80)
                return data[::slice]
            
            axial_strain = selectData(axial_strain)
            transverse_strain = selectData(transverse_strain)
            axial_strain_linear = selectData(axial_strain_linear)
            load = selectData(load)
            load_linear_axial = selectData(load_linear_axial)
            transverse_strain_linear = selectData(transverse_strain_linear)
            load_linear_tranversal = selectData(load_linear_tranversal)
            
            ax_total, ax_linear = self.plotComparisonPoissonRatioLinear(axial_strain_total=axial_strain,
                                                  transversal_strain_total=transverse_strain
                                                  ,axial_train_linear=axial_strain_linear
                                                  ,load_total=load
                                                  ,load_axial_linear = load_linear_axial
                                                  ,transversal_strain_linear=transverse_strain_linear
                                                  ,load_transversal_linear=load_linear_tranversal
                                                  )
            
             
            plt.show()

    def plotComparisonExcludedData(self, x,y, x_linear,y_linear, x_label, y_label):
        '''
        Método comparar dados excluídos da análise
        '''
        fig, ax = plt.subplots(figsize=(6,3))
        ax = plot_helper(ax=ax, x = x[0:len(x_linear)], y=y[0:len(y_linear)], label='Dados Originais', ylabel=y_label, xlabel=x_label)
        ax = plot_helper(ax=ax, x = x_linear, y=y_linear, label='Curva linear', ylabel=y_label, xlabel=x_label, color='red')
        lim_sup_x = x[len(x_linear)] 
        lim_inf_x = x[0] 
        y_max= y[len(y_linear)]
        y_min= y[0]
        
        ax.arrow(x=lim_sup_x,y=y_min,dx=0,dy=(y_max-y_min)*1.2, color='orange')
        ax.arrow(x=lim_inf_x,y=y_min,dx=0,dy=(y_max-y_min)*1.2, color='orange')
        text_x_position = (lim_inf_x)*1.01
        text_y_position = y_max*1.3
        ax.text(text_x_position, text_y_position, r'Região excluída', fontsize=7, bbox={'facecolor': 'orange', 'alpha': 0.1, 'pad': 2})
        ax.legend(loc ='lower right')
        plt.show()

    def plotCleanedData(self, x,y, x_label, y_label):
        '''
        Método para plotar os dados limpos
        '''
        fig, ax = plt.subplots(figsize=(6,3))
        ax = plot_helper(ax=ax, x = x, y=y, label='Dados Ajustados', ylabel=y_label, xlabel=x_label)    
        plt.show()

    def plotComparisonPoissonRatioLinear(self,axial_strain_total
                                             ,transversal_strain_total
                                             ,load_total
                                             ,axial_train_linear, load_axial_linear
                                             ,transversal_strain_linear, load_transversal_linear
                                         ):
        '''
        Método para plotar a comparação entre as regiões lineares na parte das deformações axial (para gerar um gráfico parecido com a norma)
        '''
        fig_total, ax = plt.subplots(figsize=(8,4), constrained_layout=True)
        # partes totais

        y_label =  r"Deformação absoluta $||\varepsilon||$"
        ax = plot_helper(ax=ax, x = load_total, y=axial_strain_total, label='Dados da deformação axial totais', ylabel=y_label, xlabel='Carregamento [kN]', color=blue_tonalities_options[0], linestyle=linestyles_options[0])
        ax = plot_helper(ax=ax, x = load_total, y=transversal_strain_total, label='Dados da deformação transversal totais', ylabel=y_label, xlabel='Carregamento [kN]', color=blue_tonalities_options[5], linestyle=linestyles_options[5])
        ax = plot_helper(ax=ax, x = load_axial_linear, y=axial_train_linear, label='Parte linear da deformação axial', ylabel=y_label, xlabel='Carregamento [kN]', color='orange', linestyle=linestyles_options[10])
        ax = plot_helper(ax=ax, x = load_transversal_linear, y=transversal_strain_linear, label='Parte linear da deformação transversal', ylabel=y_label, xlabel='Carregamento [kN]', color='red', linestyle=linestyles_options[12])
        
        fig_total.savefig('total_poisson.pdf')
        fig_total.savefig('total_poisson.svg')
        fig_total.savefig('total_poisson.png')

        fig, ax3 = plt.subplots(figsize=(8,4), constrained_layout=True)
        ratio = np.divide(transversal_strain_linear, axial_train_linear)
        ax3 = plot_helper(ax=ax3, x = load_axial_linear, y=ratio, 
                          label=r'Convergência do razão de Poisson, $\nu_{xy}$'+f'={self.poisson_ratio:.3f}', 
                          ylabel=r'$||\frac{\varepsilon_{y}}{\varepsilon_{x}}||$', 
                          xlabel='Carregamento [kN]', 
                          color=blue_tonalities_options[10], linestyle=linestyles_options[10])

        fig.savefig('poisson_calc.pdf')
        fig.savefig('poisson_calc.svg')
        fig.savefig('poisson_calc.png')
        plt.show()
    

        return ax, ax3


    def plotDataFinalComparison(self,x,y, x_linear,y_linear, x_label,y_label):
        '''
        Método para graficar os dados originais e a parte linear
        '''
        fig, ax = plt.subplots(figsize=(6,3))
        ax = plot_helper(ax=ax, x = x, y=y, label='Dados Originais', ylabel=y_label, xlabel=x_label)
        ax = plot_helper(ax=ax, x = x_linear, y=y_linear, label='Curva linear', ylabel=y_label, xlabel=x_label, color='red')
        plt.show()

    def plotStressStrain(self,x,y,E, max_percentil : float = 0.25):
        '''
        Método para graficar a curva de tensão e deformação

        TODO - generalizar para a função receber um eixo, assim ela pode receber diversos corpos de prova
        '''
        x_max = np.quantile(x,max_percentil) #Plotando até o décimo quinto percentil do eixo x
        x_linear = np.linspace(0,x_max)
        y_linear = [E*x for x in x_linear]
        if self.verbose:
            fig, ax = plt.subplots(figsize=(6,3), constrained_layout=True)
            ax = plot_helper(ax=ax, x = x, y=y, label='Curva de tensão', ylabel=r'$\sigma_{x}$', xlabel=r'$\varepsilon \ \frac{mm}{mm}$')
            ax = plot_helper(ax=ax, x = x_linear, y=y_linear, label='Módulo ajustado', ylabel=r'$\sigma_{x} \ [MPa]$', xlabel=r'$\varepsilon \ \frac{mm}{mm}$', color=blue_tonalities_options[5])
            ax.text(x_linear[-1]*0.8,y_linear[-1]*0.3,fr'E={E:.2f} [MPa]',bbox={'facecolor': 'white', 'alpha': 1, 'pad': 3})
        x_offset, y_offset , yieldStress= self.__findYeldStress(x,y,E,max_percentil=max_percentil)
        if self.verbose:
            ax = plot_helper(ax=ax, x = x_offset, y=y_offset, label=fr'Offset ($\sigma_y={yieldStress:.2f} [MPa]$)', ylabel=r'$\sigma_{x} \ [MPa]$', xlabel=r'$\varepsilon \ \frac{mm}{mm}$', color=blue_tonalities_options[8], linewidth=0.1, linestyle='-.')
        self.YeldStress = yieldStress
        self.strain = x
        self.stress = y
        fig.savefig('young_modulus.pdf')
        fig.savefig('young_modulus.svg')
        fig.savefig('young_modulus.png')

class SeveralMechanicalTestingFittingLinear():

    def __init__(self, machineName: str, archive_name: str, archivePattern = 'numeric', linearRegionSearchMethod='Deterministic') -> None:
        
        self.__findOtherArchives(machineName, archive_name, archivePattern, linearRegionSearchMethod)

    
    def __findOtherArchives(self, machineName: str, archive_name :  str, archivePattern : str, linearRegionSearchMethod='Deterministic'):
        '''
        Method to find others files based on the archive name
        '''
        # get parent dir
        parent_dir = os.path.dirname(archive_name)
        # get all files
        files = os.listdir(parent_dir)
        youngModulusArray = []
        YieldStressArray = []
        cpName = []
        stress_array = []
        strain_array = []

        for each_file in os.listdir(parent_dir):
            if re.search(pattern=r"\d*.csv", string=each_file):
                full_path_name = os.path.join(parent_dir, each_file)
                c = MechanicalTestFittingLinear(machineName=machineName, archive_name=full_path_name, 
                                                linearRegionSearchMethod=linearRegionSearchMethod, verbose=False)
                c.MeasureYoungModulus()
                youngModulusArray.append(c.E)
                YieldStressArray.append(c.YeldStress)
                cpName.append(each_file.split(sep='.csv')[0])
                stress_array.append(c.stress)
                strain_array.append(c.strain)

        
        # Dicionario com os dados para o boxPlot
        dictMechanical = {'Corpo de Prova': cpName
                          ,'Módulo de Young': youngModulusArray
                          ,'Tensão de Escoamento': YieldStressArray
                          ,'strain': strain_array
                          ,'stress': stress_array
                          }
        # Figuras para colocar os boxplots
        fig_YoungModuls,ax_youngModulus = plt.subplots(figsize=(4,3))
        fig_YieldStress,ax_YieldStress = plt.subplots(figsize=(4,3))
        sns.boxplot(data=dictMechanical, x="Módulo de Young", ax=ax_youngModulus)
        sns.boxplot(data=dictMechanical, x="Tensão de Escoamento", ax=ax_YieldStress)
        fig_YoungModuls.show()
        fig_YieldStress.show()
        self.dictMechanical =  dictMechanical
        fig_stress_mat, _ = self.__plotStressStrain()
        array_figures = [fig_YoungModuls, fig_YieldStress, fig_stress_mat]

        self.__createrPDFReport(array_figures)


    def __plotStressStrain(self):
        '''
        Metodo para plotar as curvas de tensao/deformacao, para comparacao posterior
        '''
        fig,ax = plt.subplots(figsize=(10,4))
        
        xs = self.dictMechanical['strain']
        ys = self.dictMechanical['stress']
        labels = self.dictMechanical['Corpo de Prova']
        print(labels)
        several_plots_helper(ax=ax, xs=xs, ys=ys,labels=labels,xlabel=r'Deformação $[mm/mm]$', ylabel=r'$\sigma _x $ [MPa]')
        fig.show()

        fig_plotly = go.Figure()
        for each_cp,x,y in zip(labels,xs,ys):
                    fig_plotly.add_trace(
            go.Scatter(
                x=x,  # X-axis (assuming 10 time points or measurements)
                y=y,
                mode="lines",
                name=f"{each_cp}",  # Legend entry
            )
        )
        fig_plotly.update_layout(title='Ensaio de Tração Realizado',
        xaxis_title='Deformação [mm/mm]',
        yaxis_title='Tensão [MPa]')
        fig_plotly.show()

        return fig,fig_plotly

    def __createrPDFReport(self, figs_array : list):
        '''
        Save info into a pdf (PENSAR EM UM FORMA DE COMO CRIAR UM REPORT COM AS INFORMACOES, ASSIM COM E FEITO NA INSTRON)
        '''
        # with PdfPages("output_plots.pdf") as pdf:
        #     for fig in figs_array:
        #         fig.show()
        #         pdf.savefig()  # Save each plot to the PDF file
        #         plt.close()

class MonteCarloErrorPropagation():
    '''
    Classe para calcular a propagação de erros mediante uma simulação de Monte Carlo

    Ex.:

    def density(m,r,t):
        return m/(np.pi*r**2*t)

    measured_r = [10.01,10.02,10.00,10.05]
    measured_t = [1.01,1.02,1.00,1.05]
    measured_m = [10.50,10.35,10.44,10.42]

    MonteCarloErrorPropagation(density, measured_r,measured_t,measured_m)

    '''

    def __init__(self, f : any, *measured_vars):
        self.__computeError(f, *measured_vars)
        self.__plotDistribution()

        pass

    def __computeError(self,f, *params):
        '''
        
        '''
        array_distributions = []

        for each_param in params:
            var = np.array(each_param)
            var_MC = var.mean()+var.std()*np.random.normal(size=10000)
            array_distributions.append(var_MC)

        self.f_MC : np.array = f(*array_distributions)
        self.f_mean = self.f_MC.mean()
        self.f_max = self.f_MC.mean() + 2*self.f_MC.std()
        self.f_min = self.f_MC.mean() - 2*self.f_MC.std()

    def __plotDistribution(self):
        
        graph_limit_min = min(self.f_MC)
        graph_limit_max = max(self.f_MC)
        confidence_inf = self.f_MC.mean()-2*self.f_MC.std()
        confidence_sup = self.f_MC.mean()+2*self.f_MC.std()

        y_confidence_lenght = len(self.f_MC[self.f_MC>confidence_sup])
        fig,ax = plt.subplots(figsize=(4,3))
        ax.hist(self.f_MC, bins=np.linspace(graph_limit_min,graph_limit_max))
        ax.plot([confidence_inf,confidence_inf],[0, y_confidence_lenght], color='orange')
        ax.plot([confidence_sup,confidence_sup],[0,y_confidence_lenght],color='orange')

        self.ax = ax

class SimpleStatistics():
    '''
    Classe para avaliação simples de estatíticas, dado um conjunto de dados
    '''
    def __init__(self, samples : np.array):

        self.samples : np.array = samples
        self.__computeStatistics()
        pass
    
    def __computeStatistics(self):
        '''
        Calcula estatísticas simples
        '''
        self.std = self.samples.std()
        self.mean = self.samples.mean()
        self.median = np.median(self.samples)
        self.first_quartil = np.quantile(self.samples,0.25)
        self.third_quartil = np.quantile(self.samples,3/4)

    def plot_results(self):
        
        self.fig, self.ax = plt.subplots(figsize=(4,3))
        height_bar =  len(self.samples[self.samples>np.quantile(self.samples,0.9)])
        self.ax.hist(self.samples, bins=20)
        self.ax.plot([self.first_quartil, self.first_quartil],[0,height_bar], color='orange')
        self.ax.plot([self.third_quartil, self.third_quartil],[0,height_bar], color='orange')
        self.ax.plot([self.mean, self.mean],[0,height_bar], color='green', label='Média')
        self.ax.plot([self.median, self.median],[0,height_bar], color='red', label='Mediana')
        self.ax.arrow(x=self.first_quartil,y=height_bar,dx=(self.third_quartil-self.first_quartil),dy=0, color='orange', label='Interquartil')
        self.ax.legend()

if __name__ == '__main__':
    # classInitOne =  MechanicalTestFittingLinear('68FM100', archive_name=r'D:\Jonas\ExperimentalData\OS894_22_PP40RE3AM.is_tens_Exports\YBYRÁ_Tensile_PP40RE3AM_SP-01.csv')

    # classInitOne.MeasureYoungModulus()  
    # classInit = SeveralMechanicalTestingFittingLinear('68FM100', archive_name=r'D:\Jonas\ExperimentalData\OS894_22_PP40RE3AM.is_tens_Exports\YBYRÁ_Tensile_PP40RE3AM_SP-01.csv')  
    classInit = MechanicalTestFittingLinear('68FM100_biaxial', archive_name=r'D:\Jonas\PostProcessingData\DataArquives\Specimen_biaxial.csv')
    classInit.MeasureYoungModulus(max_percentil=0.05)
    classInit.MeasurePoissonRatio()

# %%
# %%
