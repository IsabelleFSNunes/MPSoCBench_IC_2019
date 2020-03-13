from tkinter import *

from tkinter import messagebox

import os
import sys
import subprocess

## Globals Variables 
processors = [ 'ARM', 'MIPS',  'PowerPC', 'SPARC' ]
n_cores = ['1', '2', '4', '8', '16', '32', '64']
interconnections = ['NoC approximately timed', 'NoC loosely timed','Router loosely timed']
applications = ['Basicmath', 'Dijkstra', 'SHA', 'Susan-corners', 'Susan-edges', 'Susan-smoothing','Stringsearch', 'FFT', 'LU', 'Water', 'Water-spatial', 'Multi-8', 'Multi-16', 'Multi-parallel',  'Network-Automotive',  'Office-Telecomm', 'Security']

## Valids Combinations to Applications and Cores
def validPlatforms( ):
	
	M = []

	for i, j in enumerate( applications ):
		if j == 'Office-Telecomm' or j == 'Security' or j == 'Network-Automotive':
			M.append( [False] * 7 )
			M[i][2] = True
		else:
			M.append( [True] * 7 )
			if j =='Susan-corners' or j == 'Susan-edges':
				M[i][6] = False
			if j == 'FFT' or j == 'LU' or j == 'Water':
				M[i][5:] = [False] * 2
			if j == 'Multi-parallel':
				M[i][:1] = [False] * 2
			if j == 'Susan-smoothing' or j == 'Water-spatial':
				M[i][4:] = [False] * 3
			if j == 'Multi-8':
				M[i][:2] = [False] * 3
			if j == 'Multi-16':
				M[i][:3] = [False] * 4
	return M  	

## To verify the choices selected 
def selected( frame ):

	positions = []

	for i, j in enumerate(frame):
		if j.get() == True:
			positions.append(i)
	
	return positions
	
	
## Create new list to Tkinter objects
def newObjTkinter( n ):

	variables = []
	
	for i in range( n ):
		tmp = BooleanVar()
		variables.append( tmp )
		
	return variables


## When the button All was clicked 
def clickedAll( var, bt ) :
	n = len( var )
	
	if bt['relief'] == RAISED:
		bt.config( relief = SUNKEN )
		for i in range( n ):
			var[i].set( True )
	else:
		bt.config( relief = RAISED )
		for i in range( n ):
			var[i].set( False )

## This module is used when the botton All was clicked and some checkbox will be modified 
def notclickedAll( bt ):
	if bt['relief'] == SUNKEN:
		bt.config( relief = RAISED )
	
## To verify the Incomplete Settings 
def incompleteSettings(frame):
	
	tmp = []			# Lista temporaria para receber os onvalue dos objetos das checkboxes
	name = ''
	txt = StringVar()
	
	for i in frame:
		for j in frame[i]:
			tmp.append( j.get() ) 
	
		if True not in tmp:
			name +=  i + ' ;\n'
			
		tmp = []
		
	if name != '' :
		txt.set('Select at least one valid option in:\n\n'+ name + '\nComplete this section(s) and try again.')
		messagebox.showerror(title = 'Incomplete Settings', message = txt.get())

	return len(name)

## Power Consumption for MIPS and SPARC
def pwr( frameP ):
	pwrMIPS, pwrSPARC = False, False
	
	if frameP[1].get() == True:			# posição do processador MIPS na lista 
		pwrMIPS = messagebox.askyesno(title = 'Enable power', message = 'Would you like enable the Processor MIPS with power consumption ?')
	if frameP[3].get() == True:			# posição do processador SPARC na lista 
		pwrSPARC = messagebox.askyesno(title = 'Enable power', message = 'Would you like enable the Processor SPARC with power consumption ?')
		
	return pwrMIPS, pwrSPARC

## 
def cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

## rundir Makefile creator
# run_make(path, processors[p], n_cores[c], applications[l], interconnections[i])
def run_make(path, proc, nproc, app, intercon):
    make = "run:\n\t./platform." + intercon + ".x " + app + "." + proc + ".x " + nproc +"\n"
    f = open(path + "/Makefile", "w")
    f.write(make)
    f.close()

## Create and Update the Makefile
def makefile( proc , nCores, app, power, inter, currentPlatform ):
	# Inicialização dos valores de algumas variáveis do SHELL 
	make = '#FILE GENERATED AUTOMAGICALLY - DO NOT EDIT'
	make = make + \
			'\nexport SHELL := /bin/bash'  \
			'\nexport PROCESSOR := ' + proc +  \
			'\nexport NUMCORES := ' + nCores + \
			'\nexport APPLICATION := ' + app + \
			'\nexport PLATFORM := platform.' + inter + '\n'
	
	# Variavel do Compilador
	cross = proc + '-newlib-elf-gcc'
	if proc == 'arm':
		cross = cross.replace('elf', 'eabi')
		
	# Verificação do compilador
	if cmd_exists(cross):
		make = make + 'export CROSS := ' + cross + '\n'
	else:
		sys.exit('\nERROR: Cross-compiler ' + cross + ' is not in the PATH\n')
	
	# Verificação power
	pwrFlag = ''
	make = make + 'export POWER_SIM_FLAG :=' 
	if power:
		make = make + '-DPOWER_SIM=\\\"\\\"'
		pwrFlag = ' -pw'
		
	make = make + '\n'
	make = make + 'export ACSIM_FLAGS := -abi -ndc' + pwrFlag + '\n'
	
	# Verificação da interconecção
	if inter == 'noc.at':
		make = make + 'export WAIT_TRANSPORT_FLAG := -DWAIT_TRANSPORT\nexport TRANSPORT := nonblock\n'
	else:
		make = make + 'export WAIT_TRANSPORT_FLAG := \nexport TRANSPORT := block\n'
		
	make = make + 'export MEM_SIZE_DEFAULT := -DMEM_SIZE=536870912\n'
	make = make + 'export RUNDIRNAME := ' + currentPlatform+ '\n'
	
	# verificar o proc
	make = make + 'export ENDIANESS :=' 
	if proc != 'arm':
		make = make + '-DAC_GUEST_BIG_ENDIAN'
	make = make + '\n'	
	
	# Finalizar o make
	make = make + 'ifeq ($(PROCESSOR),ARM)\nexport CFLAGS_AUX := -DPROCARM\nendif\n'
	make = make + 'ifeq ($(PROCESSOR),MIPS)\nexport CFLAGS_AUX := -DPROCMIPS\nendif\n'
	make = make + 'ifeq ($(PROCESSOR),PowerPC)\nexport CFLAGS_AUX := -DPROCPOWERPC\nendif\n'
	make = make + 'ifeq ($(PROCESSOR),SPARC)\nexport CFLAGS_AUX := -DPROCSPARC\nendif\n'
	make = make + 'include Makefile.rules\n'
	
	return make
		
## Informações sobre o MPSoCBench ( GUI )
def about():
	messagebox.showinfo(title = 'About', message = 'falta completar...')

def helpUse():
	messagebox.showinfo(title = 'Help', message = 'falta completar...')
'''
Funcoes temporarias para testar os botoes
'''

def btExit():
	exit()

def Build(frames, windowMain, listtmp):
	
	count = 0			# variavel para fazer a contagem das seções incompletas
	invalidCombinations = False # variavel para verificar se há combinações invalidas
	
	# Verificar se falta alguma informação
	count = incompleteSettings(frames)
	
	# Se as configurações são validas, prosseguir com a contrução  do simulador
	if count == 0:
				
		pwrMIPS, pwrSPARC = pwr(frames['Processors'])
		
		Matriz = validPlatforms( )
		
		procs = selected( frames['Processors'] )
		inter = selected( frames['Interconnections'] )
		lin = selected( frames['Applications'] )
		col = selected( frames['Cores'] )
		
		for p in procs:
			for i in inter:
				if i == 0:
					i = 'noc.at'
				elif i == 1:
					i = 'noc.lt'
				elif i == 2:
					i = 'router.lt'
				
				for l in lin:		# applications
					for c in col:		# num cores
						if Matriz[l][c] == False:
							invalidCombinations = True
						else:
							currentPlatform = processors[p] + '.' + i + '.'
							
							power = False
							
							if (p == 'MIPS' and pwrMIPS) or (p == 'SPARC' and pwrSPARC) :
								currentPlatform  = currentPlatform  + 'pwr.'
								power = True
								
							currentPlatform  = currentPlatform  + n_cores[c] + '.' + applications[l]
							
							# padronizando a saída
							currentPlatform  = currentPlatform.lower()
							#currentPlatform  = currentPlatform.replace( ' approximately timed', '.at' )
							#currentPlatform  = currentPlatform.replace( ' loosely timed', '.lt' )
							
							print( currentPlatform )
							
							os.system( 'rm Makefile' )
							
							# creates general Makefile 
							
							f = open( 'Makefile', 'w' )		
							f.write( makefile( processors[p].lower(), n_cores[c], applications[l].lower(), power, i, currentPlatform ) )
							
							f.close()
							
							# make the platform
							os.system( 'make clean distclean all' )
							
							os.system('rm Makefile')
							# creates general Makefile
							
							f = open('Makefile', 'w')
							f.write( makefile( processors[p].lower(), n_cores[c], applications[l].lower(), power, i, currentPlatform  ) )
							f.close()
							
							# makes the platform
							
							os.system('make clean distclean all')
							path = 'rundir/' + currentPlatform
							print('Creating rundir for ' + path[7:] + '...')
							# creates rundir for each platform
							os.system('mkdir -p ' + path)
							# copies it to its rundir					
							os.system('make copy')
							os.system('make clean')
							# creates rundir makefile
							run_make(path, processors[p].lower(), n_cores[c], applications[l].lower(), i)
							# creates condor task file in the rundir           
					
		if invalidCombinations:
			messagebox.showinfo(title = 'Warning', message = "Some settings selected won't be completed. You can to verify in Menu > Help the settings that are valids and that they don't.\n")
		
		
		
		
def Execute():
	exit()

# Classe destinada a interface grafica

class Window(Frame):
	def __init__( self, master=None ):
		Frame.__init__( self, master )
		master.title('MPSoCBench')
		
		# Menu inicial
		menubar = Menu( self.master, bg = '#A9A9A9' ) 		
		menubar.add_command( label = 'About', command = about )
		menubar.add_command( label = 'Help', command = helpUse )
		self.master.config( menu = menubar ) 

		
		# Parte 1 : Direcionada para as opções de Configurações
		part1 = LabelFrame( master, text = 'SETTINGS', font = 'bold', padx = 5, pady = 5 )
			
		## Parte 1.1. : Processadores
		part11 = LabelFrame( part1, text = 'Processors', font = 'bold', padx = 5, pady = 5 )
		part11.pack( side = TOP, fill = X, expand = 1 )
		
		# Inicialização de algumas variaveis que serão usadas nesta parte 1.1
		frameProcessors = []
		op1 = []
		
		frameProcessors = newObjTkinter(4)		

		for i, j in enumerate( processors ):
			op1.append( Checkbutton( part11, text = j, variable = frameProcessors[i], command = lambda: notclickedAll( btAll1 )))
			op1[i].pack( side = LEFT, expand = 1 , anchor = W )	
		
		btAll1 = Button( part11, text = 'All', bg = '#C0C0C0', command = lambda: clickedAll( frameProcessors, btAll1 ))
		btAll1.pack( side = LEFT)

		
		## Parte 1.2. : Dispositivos
		part12 = LabelFrame( part1, text = 'Interconnections', font = 'bold', padx = 5, pady = 5 )
		part12.pack( side = TOP, fill = X, expand = 1 )
		
		# Inicialização de algumas variaveis que serão usadas nesta parte 1.2
		frameInter = []
		op2 = []
		
		frameInter = newObjTkinter(3)	
		
		for i, j in enumerate( interconnections ):
			op2.append( Checkbutton( part12, text = j, variable = frameInter[i], command = lambda: notclickedAll( btAll2 ) ) )
			op2[i].pack( side = LEFT, expand = 1 , anchor = W )
		
		btAll2 = Button( part12, text = 'All', bg = '#C0C0C0', command = lambda: clickedAll( frameInter, btAll2 ))
		btAll2.pack( side = LEFT )
		
				
		## Parte 1.3. : numero de cores
		part13 = LabelFrame( part1, text = 'Cores', font = 'bold', padx = 5, pady = 5 )
		part13.pack( side = TOP, fill = X, expand = 1 )
		
		# Inicialização de algumas variaveis que serão usadas nesta parte 1.3
		frameNCores = []
		op3 = []
		
		frameNCores = newObjTkinter(7)
		
		for i, j in enumerate( n_cores ):
			op3.append( Checkbutton( part13, text = j, variable = frameNCores[i], command = lambda: notclickedAll( btAll3 ) ) ) 
			op3[i].pack( side = LEFT, expand = 1 , anchor = W )
		
		btAll3 = Button( part13, text = 'All', bg = '#C0C0C0', command = lambda: clickedAll( frameNCores, btAll3 ))
		btAll3.pack( side = LEFT )
		
		## Parte 1.4. : Aplicações
		part14 = LabelFrame( part1, text = 'Applications', font = 'bold', padx = 5, pady = 5 )
		part14.pack( side = TOP, fill = X, expand = 1 )
		
		part141 = LabelFrame( part14, text = 'ParMibench' )
		part142 = LabelFrame( part14, text = 'SPLASH2' )
		part143 = LabelFrame( part14, text = 'Miscellaneous' )

		## Applications será dividido em 3 partes
		splitThisFrame = 0
		
		# Inicialização de algumas variaveis que serão usadas nesta parte 1.4
		frameApps = []
		
		# 1.4.1
		frameParMibench = []
		op41 = []

		frameParMibench = newObjTkinter(7)
		
		# 1.4.2
		frameSplash2 = []
		op42 = []

		frameSplash2 = newObjTkinter(4)
		
		# 1.4.3
		frameMisc = []
		op43 = []

		frameMisc = newObjTkinter(6)
				
		for i, j in enumerate( applications ):
			if j == 'FFT' or j == 'Multi-8':
				splitThisFrame += 1	
				
			# ParMibench
			if splitThisFrame  == 0:
				op41.append( Checkbutton( part141, text = j, variable = frameParMibench[i], command = lambda: notclickedAll( btAll41 ) ) )
				op41[i].pack( side = TOP, anchor = W  )
				part141.pack( side = LEFT, anchor = N, fill = BOTH, expand = 1 )
		
			# SPLASH2
			if splitThisFrame  == 1:
				op42.append( Checkbutton( part142, text = j, variable = frameSplash2[i-7], command = lambda: notclickedAll( btAll42 ) ) )
				op42[i-7].pack( side = TOP, anchor = W )
				part142.pack( side = LEFT, anchor = N, fill = BOTH, expand = 1 )
			    
			# Miscellaneous   
			if splitThisFrame  == 2:
				op43.append( Checkbutton( part143, text = j, variable = frameMisc[i-11], command = lambda: notclickedAll( btAll43 ) ) )
				op43[i-11].pack( side = TOP, anchor = W )
				part143.pack( side = LEFT, anchor = N, fill = BOTH, expand = 1 )
	
		# Botões All de cada tipo de Aplicações
		btAll41 = Button( part141, text = 'All', bg = '#C0C0C0', command = lambda: clickedAll( frameParMibench, btAll41 ) )
		btAll41.pack( side = TOP, anchor = S, fill = X, expand = 1 )	
		
		btAll42 = Button( part142, text = 'All', bg = '#C0C0C0', command = lambda: clickedAll( frameSplash2, btAll42 ) )
		btAll42.pack( side = TOP, anchor = S, fill = X, expand = 1 )
		
		btAll43 = Button( part143, text = 'All', bg = '#C0C0C0', command = lambda: clickedAll( frameMisc, btAll43 ) )
		btAll43.pack( side = TOP, anchor = S, fill = X, expand = 1 )
		
		frameApps.extend( frameParMibench )
		frameApps.extend( frameSplash2 )
		frameApps.extend( frameMisc )		
		
		part1.pack( side = LEFT, padx = 5, pady = 5, anchor = W )
	    	    
	    # Parte 2 : Direcionada para a lista de Configurações já escolhidas
		part2 = LabelFrame( master, padx = 5, pady = 5 )
		
		# Builded
		part21 = LabelFrame( part2, text = 'Builded', padx = 5, pady = 5 )
		part21.pack( side = TOP, fill = BOTH, expand = 1 ) 
		listtmp = []
			## print('antes', listtmp)
		# Executed
		part22 = LabelFrame( part2, text = 'Executed', padx = 5, pady = 5 )
		part22.pack( side = TOP, fill = BOTH, expand = 1 ) 
		
		part2.config( relief = FLAT )
		part2.pack( side = LEFT, fill = BOTH, expand = 1, anchor = E )
	    
	    # Parte 3 : Direcionada para os botões de Configurações
		part3 = LabelFrame( part1 )
		part3.config( relief = FLAT )
		
		frames = { 'Processors':frameProcessors, 'Interconnections':frameInter, 'Cores':frameNCores, 'Applications':frameApps }
		
		# Criando botões
		bt1 = Button( part3, text = 'Build', bg = '#C0C0C0', command = lambda: Build( frames, self.master, listtmp) )		
		bt2 = Button( part3, text = 'Execute', bg = '#C0C0C0', command = Execute )
		bt3 = Button( part3, text = 'Quit', bg = '#C0C0C0', command = btExit )
		
			## print('depois dos botões serem executados', listtmp)
		
		bt1.pack( side = LEFT, fill = X, expand = 1 )
		bt2.pack( side = LEFT, fill = X, expand = 1 )
		bt3.pack( side = LEFT, fill = X, expand = 1 )
		
		part3.pack( fill = X, expand = 1 )

		
def main():               
	root = Tk()

	root.geometry('1040x480')

	app = Window(root)

	root.mainloop()

if __name__ == "__main__":
	main()
