from appJar import gui
import os
import copy

saved = 0
first_open = 0
text = 0

#Detetor de texto
def text_detector():
    global first_open, text, saved

    if(app.getTextArea("text") != ""):
        first_open = 1
        text = 1

    if(app.getTextArea("text") == ""):
        text = 0

    print("text:", text,"saved:", saved, "first_open:", first_open) #debugging

#Sobre
def about():
    app.infoBox("Sobre", "Bem vindo ao Armandex Docs, o editor de texto que eu criei!")

#Abrir
def opene():
    global saved, first_open

    #Escolher Ficheiro - guardar em file o local do ficeiro
    file = app.openBox(title=None, dirName=None, fileTypes=[('texts', '.txt')], asFile=False, parent=None, multiple=False, mode='r')

    #Copiar os conteudos do ficheiro para uma string
    with open(file, 'r') as file2:
        data = file2.read()

    #Se já guardou e nao é a primeira vez a abrir
    if (saved == 1 and first_open != 0):
        app.clearAllTextAreas(callFunction=False)#limpar texto anteior
        app.setTextArea("text", data, end=True, callFunction=True)#colocar novo texto
        #atualizar variaveis
        first_open = 1
        saved = 0
    #Senao, se ainda nao guardou e nao e a primeira vez
    elif(saved == 0 and first_open != 0):
        resposta = app.yesNoBox("p1", "Não guardaste o documento que tens atualmente aberto.\nDesejas abrir um novo documento sem guardar?", parent=None)
        if(resposta == True): #Se responder que quer abrir
            app.clearAllTextAreas(callFunction=False)#limpar
            app.setTextArea("text", data, end=True, callFunction=True)#colocar novo texto
            #atualizar variaveis
            first_open = 1
            saved = 0
        else: #Se responder que nao quer abrir
            return 0
    #Se é a primeira vez a abrir
    elif(first_open == 0):
        app.setTextArea("text", data, end=True, callFunction=True)
        first_open = 1
        saved = 0


#Fechar
def close():
    global saved, first_open, text

    #Se nao guardou e o texto existe
    if (saved == 0 and text  == 1):
        #caixa de pergunta
        resposta = app.yesNoBox("p2", "Não guardaste o documento que tens atualmente aberto.\nDesejas apagar sem guardar?", parent=None)
        if (resposta == True): #caso responda sim
            app.clearAllTextAreas(callFunction=False)
            saved = 0
            text = 0
        else: #caso responda nao
            return 0;

    #Se ja guardou e nao e a primeira vez a abrir/fechar
    elif(saved == 1 and first_open != 0):
        app.clearAllTextAreas(callFunction=False) #limpar tudo
        #como limpamos o texto, o novo texto ja nao esta guardado
        saved = 0
        text = 0

    #Se é a primeira vez a abrir/fechar ou se o texto nao exite nao importa o que esta função faz

#Guardar
def save():
    global saved

    #Recolher texto
    conteudo = app.getTextArea("text")

    #Recolher local onde o utilizador quer guardar
    dir = app.saveBox(title=None, fileName=None, dirName="/Users/josearmandoborgesrodrigues/Desktop", fileExt='.txt', fileTypes=None, asFile=None, parent=None)

    #Diretorio para guardar
    save_path = dir.rsplit('/', 1)[0]

    #Pegar na ultima parte da string para ter o nome
    dir = dir.split("/", 50)
    nome = dir[len(dir)-1]

    #Criar um ficheiro no diretorio "save_path" com nome "nome"
    name_of_file = os.path.join(save_path, nome)

    #Escrever no ficeiro aquilo que se recolheu da caixa de texto
    file1 = open(name_of_file, "w")
    file1.write(conteudo)
    file1.close()

    #Indicar que foi guardado
    saved = 1

#Definições
def settings():
    app.infoBox("sobre", "Olá")

#GUI
app = gui("Editor de Texto", "2560X1600")

#Spalshscreen
app.showSplash("Armandex Docs", fill='red', stripe='black', fg='white', font=44)

app.registerEvent(text_detector)

#Setup da janela principal
app.setBg("green")
app.setFont(size = 32, family = "Courier")

#Adicionar caixa de texto
app.addScrolledTextArea("text", text=None)

#Toolbox
tools = ["ABOUT", "OPEN", "CLOSE", "SAVE", "SETTINGS"]
funcs =  [about, opene, close, save, settings]
app.addToolbar(tools, funcs, findIcon=True)
app.setToolbarPinned(pinned=True)



app.go()
