from tkinter import *

from tkinter import messagebox

## Organização dos itens do Simulador
## variaveis globais
processors = [ 'ARM', 'MIPS',  'PowerPC', 'SPARC' ]
n_cores = ['1', '2', '4', '8', '16', '32', '64']
interconnections = ['NoC approximately timed', 'NoC loosely timed','Router loosely timed']
applications = ['Basicmath', 'Dijkstra', 'SHA', 'Susan-corners', 'Susan-edges', 'Susan-smoothing','Stringsearch', 'FFT', 'LU', 'Water', 'Water-spatial', 'Multi-8', 'Multi-16', 'Multi-parallel',  'Network-Automotive',  'Office-Telecomm', 'Security']

## Opções válidas para cada configuração
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

## Verificação das entradas
def selected( frame ):
	positions = []
	for i, j in enumerate(frame):
		if j.get() == True:
			positions.append(i)
	
	return positions
	
	
## Criação de novos objetos do Tkinter
def newObjTkinter( n ):

	variables = []
	
	for i in range( n ):
		tmp = BooleanVar()
		variables.append( tmp )
		
	return variables


## Modulo para o comando dos Botões All de cada seção
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

	
## Verificação de Configurações incompletas
def incompleteSettings(frame, name):
	
	tmp = []			# Lista temporaria para receber os onvalue dos objetos das checkboxes
	ret = 0				# variavel para armazenar o que deve ser retornado deste modulo 
	txt = StringVar()
	
	# Loop para a transferencia dos valores para a lista temporaria
	for i in frame:
		tmp.append( i.get() ) 
	
	if True not in tmp:
		ret = 1 
		txt.set('Select at least one valid option in '+ name + '\nComplete this section and try again.')
		messagebox.showerror(title = 'Incomplete Settings', message = txt.get())

	return ret

## Modulo direcionado para a configuração power , um extra para os processadores MIPS e SPARC
def pwr( frameP ):
	pwrMIPS, pwrSPARC = False, False
	
	if frameP[1].get() == True:			# posição do processador MIPS na lista 
		pwrMIPS = messagebox.askyesno(title = 'Enable power', message = 'Would you like enable the Processor MIPS with power consumption ?')
	if frameP[3].get() == True:			# posição do processador SPARC na lista 
		pwrSPARC = messagebox.askyesno(title = 'Enable power', message = 'Would you like enable the Processor SPARC with power consumption ?')
		
	return pwrMIPS, pwrSPARC
	
	
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
	for f in frames: 
		count += incompleteSettings(frames[f], f)
	
	# Se as configurações são validas, prosseguir com a contrução  do simulador
	if count == 0:
		print('Pode continuar') 		# mensagem temporaria
		
		pwrMIPS, pwrSPARC = pwr(frames['Processors'])
				
		Matriz = validPlatforms( )
		
		procs = selected( frames['Processors'] )
		inter = selected( frames['Inter'] )
		lin = selected( frames['Apps'] )
		col = selected( frames['Ncores'] )
		
		for p in procs:
			for i in inter: 
				for l in lin:		# applications
					for c in col:		# num cores
						if Matriz[l][c] == False:
							invalidCombinations = True
						else:
							txt = processors[p] + '.' + interconnections[i] + '.'
							if pwrMIPS or pwrSPARC:
								txt = txt + 'pwr.'
							txt = txt + n_cores[c] + '.' + applications[l]
							
							print(txt)
					
		if invalidCombinations:
			messagebox.showinfo(title = 'Warning', message = "Some settings selected won't be completed. You can to verify in Menu > Help the settings that are valids and that they don't.")
		
		
		
		
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
			op1.append( Checkbutton( part11, text = j, variable = frameProcessors[i]))
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
			op2.append( Checkbutton( part12, text = j, variable = frameInter[i] ) )
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
			op3.append( Checkbutton( part13, text = j, variable = frameNCores[i] ) ) 
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
		separador = 0
		
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
				separador+= 1	
				
			# ParMibench
			if separador == 0:
				op41.append( Checkbutton( part141, text = j, variable = frameParMibench[i] ) )
				op41[i].pack( side = TOP, anchor = W  )
				part141.pack( side = LEFT, anchor = N, fill = BOTH, expand = 1 )
		
			# SPLASH2
			if separador == 1:
				op42.append( Checkbutton( part142, text = j, variable = frameSplash2[i-7] ) )
				op42[i-7].pack( side = TOP, anchor = W )
				part142.pack( side = LEFT, anchor = N, fill = BOTH, expand = 1 )
			    
			# Miscellaneous   
			if separador == 2:
				op43.append( Checkbutton( part143, text = j, variable = frameMisc[i-11] ) )
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
		print('antes', listtmp)
		# Executed
		part22 = LabelFrame( part2, text = 'Executed', padx = 5, pady = 5 )
		part22.pack( side = TOP, fill = BOTH, expand = 1 ) 
		
		part2.config( relief = FLAT )
		part2.pack( side = LEFT, fill = BOTH, expand = 1, anchor = E )
	    
	    # Parte 3 : Direcionada para os botões de Configurações
		part3 = LabelFrame( part1 )
		part3.config( relief = FLAT )
		
		frames = { 'Processors':frameProcessors, 'Inter':frameInter, 'Ncores':frameNCores, 'Apps':frameApps }
		
		# Criando botões
		bt1 = Button( part3, text = 'Build', bg = '#C0C0C0', command = lambda: Build( frames, self.master, listtmp) )		
		bt2 = Button( part3, text = 'Execute', bg = '#C0C0C0', command = Execute )
		bt3 = Button( part3, text = 'Quit', bg = '#C0C0C0', command = btExit )
		
		print('depois dos botões serem executados', listtmp)
		
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
