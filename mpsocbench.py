from tkinter import *

from tkinter import messagebox

## Organização dos itens do Simulador
def elements():
	processors = [ 'ARM', 'MIPS',  'PowerPC', 'SPARC', 'All' ]
	n_cores = ['1', '2', '4', '8', '16', '32', '64', 'All' ]
	interconnections = ['NoC approximately timed', 'NoC loosely timed','Router loosely timed', 'All']
	applications = ['Basicmath', 'Dijkstra', 'SHA', 'Susan-corners', 'Susan-edges', 'Susan-smoothing','Stringsearch', 'All', 'FFT', 'LU', 'Water', 'Water-spatial', 'All', 'Multi-parallel', 'Multi-8', 'Multi-16','Office-Telecomm', 'Security', 'Network-Automotive', 'All']
	
	return processors, n_cores, interconnections, applications

## Opções válidas para cada configuração
def validPlatforms( app ):
	while 'All' in app:
  		app.remove('All')

	M = []

	for i, j in enumerate( app ):
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

## Criação de novos objetos do Tkinter
def newObjTkinter( n ):

	variables = []
	
	for i in range( n ):
		tmp = BooleanVar()
		variables.append( tmp )
		
	return variables

## Verificação e Tratamento da opção All
def allSelected( var ):

	n = len( var )

	if var[n-1].get():
		for i in range( n ):
			var[i].set( True )

## Verificação de Configurações incompletas
def incompleteSettings(frame, name):
	
	tmp = []			# Lista temporaria para receber os onvalue dos objetos das checkboxes
	ret = 0				# variavel para armazenar o que deve ser retornado deste modulo 
	
	# Loop para a transferencia dos valores para a lista temporaria
	for i in frame:
		tmp.append( i.get() ) 

	# Quando uma seção não estiver selecionada, enviar uma mensagem de erro para cada caso separadamente.
	if True not in tmp and name == 'Processors':
		messagebox.showerror(title = 'Incomplete Settings', message = 'Select at least one valid option in Processors.\nComplete this section and try again.')
		ret = 1
	
	if True not in tmp and name == 'Inter':
		messagebox.showerror(title = 'Incomplete Settings', message = 'Select at least one valid option in Interconnections.\nComplete this section and try again.')
		ret = 1
	
	if True not in tmp and name == 'NCores':
		messagebox.showerror(title = 'Incomplete Settings', message = 'Select at least one valid option in Cores.\nComplete this section and try again.')
		ret = 1

	if True not in tmp and name == 'Apps':
		messagebox.showerror(title = 'Incomplete Settings', message = 'Select at least one valid option in Applications.\nComplete this section and try again.')
		ret = 1
	
	return ret
'''
Funcoes temporarias para testar os botoes
'''

def btExit():
	exit()

def Build(frames):
	
	sfw = [] 			# variavel para agrupar todas as aplicações
	count = 0			# variavel para fazer a contagem das seções incompletas
	
	# Loop para verificar se a opção all foi selecionada, e agrupar as aplicações
	for f in frames:
		allSelected( frames[f] )
		if f == 'Parmib' or f == 'Splash2' or f == 'Misc':
			sfw.extend( frames[f] )
	
	# verificar as aplicações separadamente
	count += incompleteSettings(sfw, 'Apps')
	
	# verificar as demais seções 
	for f in frames: 
		if f != 'Parmib' or f != 'Splash2' or f != 'Misc':
			count += incompleteSettings(frames[f], f)
	
	# Se as configurações são validas, prosseguir com a contrução  do simulador
	if count == 0:
		print('Pode continuar') 		# mensagem temporaria
		
def Execute():
	exit()

# Classe destinada a interface grafica

class Window(Frame):
	def __init__( self, master=None ):
		Frame.__init__( self, master )
		master.title('MPSoCBench')
		
		processors, n_cores, interconnections, applications = elements()
		
		# Parte 1 : Direcionada para as opções de Configurações
		part1 = LabelFrame( master, text = 'Settings', padx = 5, pady = 5 )
				
		## Parte 1.1. : Processadores
		part11 = LabelFrame( part1, text = 'Processors', padx = 5, pady = 5 )
		part11.pack( side = TOP, fill = X, expand = 1 )
		
		# Inicialização de algumas variaveis que serão usadas nesta parte 1.1
		frameProcessors = []
		op1 = []
		
		frameProcessors = newObjTkinter(5)		

		for i, j in enumerate( processors ):
			op1.append( Checkbutton( part11, text = j, variable = frameProcessors[i]) )
			op1[i].pack( side = LEFT, expand = 1 )	
			
		## Parte 1.2. : Dispositivos
		part12 = LabelFrame( part1, text = 'Interconnections', padx = 5, pady = 5 )
		part12.pack( side = TOP, fill = X, expand = 1 )
		
		# Inicialização de algumas variaveis que serão usadas nesta parte 1.2
		frameInter = []
		op2 = []
		
		frameInter = newObjTkinter(4)	
		
		for i, j in enumerate( interconnections ):
			op2.append( Checkbutton( part12, text = j, variable = frameInter[i] ) )
			op2[i].pack( side = LEFT, expand = 1 )
		
		## Parte 1.3. : numero de cores
		part13 = LabelFrame( part1, text = 'Cores', padx = 5, pady = 5 )
		part13.pack( side = TOP, fill = X, expand = 1 )
		
		# Inicialização de algumas variaveis que serão usadas nesta parte 1.3
		frameNCores = []
		op3 = []
		
		frameNCores = newObjTkinter(8)
		
		for i, j in enumerate( n_cores ):
			op3.append( Checkbutton( part13, text = j, variable = frameNCores[i] ) ) 
			op3[i].pack( side = LEFT, expand = 1 )
		
		## Parte 1.4. : Aplicações
		part14 = LabelFrame( part1, text = 'Applications', padx = 5, pady = 5 )
		part14.pack( side = TOP, fill = X, expand = 1 )
		
		part141 = LabelFrame( part14, text = 'ParMibench' )
		part142 = LabelFrame( part14, text = 'SPLASH2' )
		part143 = LabelFrame( part14, text = 'Miscellaneous' )

		## Applications será dividido em 3 partes
		separador = 0
		
		# Inicialização de algumas variaveis que serão usadas nesta parte 1.4
		# 1.4.1
		frameParMibench = []
		op41 = []

		frameParMibench = newObjTkinter(8)
		
		# 1.4.2
		frameSplash2 = []
		op42 = []

		frameSplash2 = newObjTkinter(5)
		
		# 1.4.3
		frameMisc = []
		op43 = []

		frameMisc = newObjTkinter(7)
		
		for i, j in enumerate( applications ):
	
			# ParMibench
			if separador == 0 and i < 8:
				op41.append( Checkbutton( part141, text = j, variable = frameParMibench[i] ) )
				op41[i].pack( side = TOP, anchor = W  )
				part141.pack( side = LEFT, anchor = N, fill = Y, expand = 1 )

			# SPLASH2
			if separador == 1 and i < 13:
			    op42.append( Checkbutton( part142, text = j, variable = frameSplash2[i-8] ) )
			    op42[i-8].pack( side = TOP, anchor = W )
			    part142.pack( side = LEFT, anchor = N, fill = Y, expand = 1 )

			# Miscellaneous   
			if separador == 2 and i < 20 :
			    op43.append( Checkbutton( part143, text = j, variable = frameMisc[i-13] ) )
			    op43[i-13].pack( side = TOP, anchor = W )
			    part143.pack( side = LEFT, anchor = N, fill = Y, expand = 1 )

			if j == 'All':
				separador+= 1	
				
		part1.pack( side = TOP, padx = 5, pady = 5 )
	    	    
	    # Parte 2 : Direcionada para a lista de Configurações já escolhidas
		#part2 = LabelFrame(master, padx = 5, pady = 5)
	    
	    # Parte 3 : Direcionada para os botões 
		part3 = LabelFrame( master )
		
		frames = { 'Processors':frameProcessors, 'Inter':frameInter, 'Ncores': frameNCores, 'Parmib': frameParMibench, 'Splash2': frameSplash2, 'Misc':frameMisc }

		
		# Criando botões
		## Uso para testes dos checkbox
		bt1 = Button( part3, text = 'Build', command = lambda: Build( frames ) )		
		bt2 = Button( part3, text = 'Execute', command = Execute )
		bt3 = Button( part3, text = 'Quit', command = btExit )
		
		bt1.pack( side = LEFT, fill = X, expand = 1 )
		bt2.pack( side = LEFT, fill = X, expand = 1 )
		bt3.pack( side = LEFT, fill = X, expand = 1 )
		
		part3.pack( fill = X, expand = 1, anchor = N, padx = 7 )

		

                
root = Tk()

root.geometry('540x440')

app = Window(root)

root.mainloop()
