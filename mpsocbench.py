from tkinter import *

def elements():
	processors = [ "ARM", "SPARC", "MIPS", "PowerPC", "All" ]
	n_cores = ["1", "2", "4", "8", "16", "32", "64", "All" ]
	interconnections = ["NoC approximately timed", "NoC loosely timed","Router loosely timed", "All"]
	applications = ["Basicmath", "Dijkistra", "SHA", "Susan-corners", "Susan-edges", "Susan-smoothing","Stringsearch", "All", "FFT", "LU", "Water", "Water-spatial", "All", "Multi-parallel", "Multi-8", "Multi-16","Office-Telecomm", "Security", "Network-Automotive", "All"]
	
	return processors, n_cores, interconnections, applications

'''

Funcoes temporarias para testar os botoes

'''

def btExit():
	exit()

def Build():
	exit()
	
def Execute():
	exit()
		
	
# Classe destinada a interface grafica

class Window(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		master.title("MPSoCBench")
		
		processors, n_cores, interconnections, applications = elements()
		
		# Parte 1 : Direcionada para as opções de Configurações
		part1 = LabelFrame(master, text = "Settings", padx = 5, pady = 5)
				
		## Parte 1.1. : Processadores
		part11 = LabelFrame(part1, text = "Processors", padx = 5, pady = 5)
		part11.pack(side = TOP, fill = X, expand = 1)
		
		for i in processors:
			op1 = Checkbutton(part11, text = i)
			op1.pack(side = LEFT, expand = 1)
			
		## Parte 1.2. : Dispositivos
		part12 = LabelFrame(part1, text = "Interconnections", padx = 5, pady = 5)
		part12.pack(side = TOP, fill = X, expand = 1)
		
		for i in interconnections:
			op2 = Checkbutton(part12, text = i)
			
			op2.pack(side = LEFT, expand = 1)
		
		## Parte 1.3. : numero de cores
		part13 = LabelFrame(part1, text = "Cores", padx = 5, pady = 5)
		
		part13.pack(side = TOP, fill = X, expand = 1)
		
		for i in n_cores:
			op3 = Checkbutton(part13, text = i)
			
			op3.pack(side = LEFT, expand = 1)
		
		## Parte 1.4. : Aplicações
		part14 = LabelFrame(part1, text = "Applications", padx = 5, pady = 5)
		part14.pack(side = TOP, fill = X, expand = 1)
		
		part141 = LabelFrame(part14, text = "ParMibench")
		part142 = LabelFrame(part14, text = "SPLASH2")
		part143 = LabelFrame(part14, text = "Miscellaneous")

		## Applications será dividido em 3 partes
		separador = 0
		for i in applications:
		
			# ParMibench
			if separador == 0:
				op41 = Checkbutton(part141, text = i)
				op41.pack(side=TOP, anchor=W)
				part141.pack(side = LEFT, anchor=N, fill = Y, expand = 1)
			
			# SPLASH2
			if separador == 1:
			    op42 = Checkbutton(part142, text = i)
			    op42.pack(side=TOP, anchor=W)
			    part142.pack(side = LEFT, anchor=N, fill = Y, expand = 1)
			
			# Miscellaneous   
			if separador == 2:
			    op43 = Checkbutton(part143, text = i)
			    op43.pack(side=TOP, anchor=W)
			    part143.pack(side = LEFT, anchor=N, fill = Y, expand = 1)
				
			if i == 'All':
				separador+= 1	
				
		part1.pack(side=TOP, padx = 5, pady = 5)
	    	    
	    # Parte 2 : Direcionada para a lista de Configurações já escolhidas
		#part2 = LabelFrame(master, padx = 5, pady = 5)
	    
	    # Parte 3 : Direcionada para os botões 
		part3 = LabelFrame(master)
		
		# Criando um botão
		bt1 = Button(part3, text = "Build", command = Build)
		bt2 = Button(part3, text = "Execute", command = Execute)
		bt3 = Button(part3, text = "Quit", command = btExit)
		
		bt1.pack(side=LEFT, fill = X, expand = 1)
		bt2.pack(side=LEFT, fill = X, expand = 1)
		bt3.pack(side=LEFT, fill = X, expand = 1)
		
		part3.pack(fill = X, expand = 1, anchor = N, padx = 7)



                
root = Tk()

root.geometry("540x440")

app = Window(root)

root.mainloop()
