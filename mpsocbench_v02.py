from tkinter import *

from tkinter import messagebox

## Organização dos itens do Simulador
def elements():
	processors = [ 'ARM', 'MIPS',  'PowerPC', 'SPARC' ]
	n_cores = ['1', '2', '4', '8', '16', '32', '64']
	interconnections = ['NoC approximately timed', 'NoC loosely timed','Router loosely timed']
	applications = ['Basicmath', 'Dijkstra', 'SHA', 'Susan-corners', 'Susan-edges', 'Susan-smoothing','Stringsearch', 'FFT', 'LU', 'Water', 'Water-spatial', 'Multi-8', 'Multi-16', 'Multi-parallel',  'Network-Automotive',  'Office-Telecomm', 'Security']
	
	return processors, n_cores, interconnections, applications

## Opções válidas para cada configuração
def validPlatforms( app ):
	
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

## Verificação das entradas
def validAppsCores( frameApp , frameCores ):
	lin = []
	col = []
	
	for i, j in enumerate(frameApp):
		if j.get() == True:
			lin.append(i)
			
	for i, j in enumerate(frameCores):
		if j.get() == True:
			col.append(i)
	
	return lin, col
	
	
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

## Modulo direcionado para a configuração power , um extra para os processadores MIPS e SPARC
def pwr( frameP ):
	pwrMIPS, pwrSPARC = False, False
	
	if frameP[1].get() == True:			# posição do processador MIPS na lista 
		pwrMIPS = messagebox.askyesno(title = 'Enable power', message = 'Would you like enable the Processor MIPS with power?')
	if frameP[3].get() == True:			# posição do processador SPARC na lista 
		pwrSPARC = messagebox.askyesno(title = 'Enable power', message = 'Would you like enable the Processor SPARC with power?')
		
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

def Build(frames, applications):
	
	count = 0			# variavel para fazer a contagem das seções incompletas
	
	# Verificar se falta alguma informação
	for f in frames: 
		count += incompleteSettings(frames[f], f)
	
	# Se as configurações são validas, prosseguir com a contrução  do simulador
	if count == 0:
		print('Pode continuar') 		# mensagem temporaria
		
		pwrMIPS, pwrSPARC = pwr(frames['Processors'])
		
		print(pwrMIPS, pwrSPARC )
		
		Matriz = validPlatforms( applications )

		lin, col = validAppsCores(frames['Apps'] , frames['Ncores'] )
		print(lin, col)
		
		for l in lin:
			print(Matriz[l])
			for c in col:
				print(Matriz[l][c])
				if Matriz[l][c] == False:
					messagebox.showinfo(title = 'Warning', message = 'ESSA OPÇÃO NÃO PODE SER CONCLUIDA...')
				# else:
				# build the combination
		
		
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

		# Inicialização das variaveis 
		processors, n_cores, interconnections, applications = elements()
		
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
			op1[i].pack( side = LEFT, expand = 1 )	
		
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
			op2[i].pack( side = LEFT, expand = 1 )
		
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
			op3[i].pack( side = LEFT, expand = 1 )
		
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
		
		part1.pack( side = TOP, padx = 5, pady = 5 )
	    	    
	    # Parte 2 : Direcionada para a lista de Configurações já escolhidas
		#part2 = LabelFrame(master, padx = 5, pady = 5)
	    
	    # Parte 3 : Direcionada para os botões 
		part3 = LabelFrame( master )

		frames = { 'Processors':frameProcessors, 'Inter':frameInter, 'Ncores':frameNCores, 'Apps':frameApps }
		
		# Criando botões
		## Uso para testes dos checkbox
		bt1 = Button( part3, text = 'Build', bg = '#C0C0C0', command = lambda: Build( frames, applications ) )		
		bt2 = Button( part3, text = 'Execute', bg = '#C0C0C0', command = Execute )
		bt3 = Button( part3, text = 'Quit', bg = '#C0C0C0', command = btExit )
		
		bt1.pack( side = LEFT, fill = X, expand = 1 )
		bt2.pack( side = LEFT, fill = X, expand = 1 )
		bt3.pack( side = LEFT, fill = X, expand = 1 )
		
		part3.pack( fill = X, expand = 1, anchor = N, padx = 7 )

		
def main():               
	root = Tk()

	root.geometry('540x480')

	app = Window(root)

	root.mainloop()

if __name__ == "__main__":
	main()
