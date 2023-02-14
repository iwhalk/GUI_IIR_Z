import scipy.signal
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from  matplotlib import patches
from tkinter import *
import re

#def slide():


def plotImpulseResponse(B, A, muestras):
    # Define the impulse sequence of length 60
    impulse = np.repeat(0., muestras)
    impulse[0] = 1.
    x = np.arange(0, muestras)
 
    # Compute the impulse response
    response = scipy.signal.lfilter(A, B, impulse)
 
    # Plot filter impulse and step response:
    fig = plt.figure(figsize=(10, 6))
    plt.subplot(211)
    plt.stem(x, response, 'm', use_line_collection=True)
    plt.ylabel('Amplitud', fontsize=15)
    plt.xlabel(r'Muestras', fontsize=15)
    plt.title(r'Respuesta al impulso h(n)', fontsize=15)
    plt.show()

def zplane(B,A):    
    B_ = [item * -1 for item in B]
    B_.insert(0, 1)
    Aroots = np.roots(A)
    B_roots = np.roots(B_)
    # Plot Poles and Zeros
    plt.figure(figsize=(6,4))
    ax = plt.subplot(111)
    r = abs(max(B_roots)) + 2; plt.axis('scaled'); plt.axis([-r, r, -r, r])
    #ticks = [-1, 1]; plt.xticks(ticks); plt.yticks(ticks)
    # Unit 
    unitario = patches.Circle((0,0), radius=1, fill=False, color='black', ls='dashed')
    ROC = patches.Circle((0,0), radius=abs(min(B_roots)), fill=False, color='red', ls='dashed')
    ax.add_patch(unitario)
    ax.add_patch(ROC)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xlabel('Re', horizontalalignment='right', x=1.0)
    plt.ylabel('Im',  y=1.0)
    plt.title('Plano Complejo Z', loc='right')
    plt.grid()
    plt.plot(np.real(Aroots),np.imag(Aroots),'rx')
    plt.plot(np.real(B_roots),np.imag(B_roots),'bo')
    plt.show()

def Guardar():

    A.clear()
    B.clear()
    if indiceA_1.get() != '':
        A.append(float(indiceA_1.get()))
    if indiceA_2.get() != '':
        A.append(float(indiceA_2.get()))
    if indiceA_3.get() != '':
        A.append(float(indiceA_3.get()))
    if indiceA_4.get() != '':
        A.append(float(indiceA_4.get()))
    if indiceB_1.get() != '':
        B.append(float(indiceB_1.get()))
    if indiceB_2.get() != '':
        B.append(float(indiceB_2.get()))
    if indiceB_3.get() != '':
        B.append(float(indiceB_3.get()))

def Borrar():
    A.clear()
    B.clear()
    indiceA_1.delete(0, END)
    indiceA_2.delete(0, END)
    indiceA_3.delete(0, END)
    indiceA_4.delete(0, END)
    indiceB_1.delete(0, END)
    indiceB_2.delete(0, END)
    indiceB_3.delete(0, END)

def Ejemplo():

    Borrar()

    indiceA_1.insert(END, '4')
    indiceA_2.insert(END, '5')
    indiceA_3.insert(END, '6')
    indiceA_4.insert(END, '7')
    indiceB_1.insert(END, '2')
    indiceB_2.insert(END, '3')
    indiceB_3.insert(END, '4')

    Guardar()

def validate(P):
    pattern = r'^-?\d+(\.\d+)?([eE][-+]?\d+)?$'
    if re.fullmatch(pattern, P) is None:
        if P == '' or '.':
            return True
        return False
    return True

def graph(B, A):
    B_ = [item * -1 for item in B]
    B_.insert(0, 1)
    pA = np.poly1d(A)
    pB_ = np.poly1d(B_)
    num = poly_to_latex(pA)
    den = poly_to_latex(pB_)
    tmptext = "$"+ "H(Z) = \\frac{"+ num +"}{" + den +"}" +"$"

    ax.clear()
    ax.text(0.1, 0.8, tmptext, fontsize=15)  
    canvas.draw()

def graphZP(B, A):
    B_ = [item * -1 for item in B]
    B_.insert(0, 1)
    Aroots = np.roots(A)
    B_roots = np.roots(B_)
    Zeros = complex_to_latex_set(Aroots, 'Z')
    Poles = complex_to_latex_set(B_roots, 'P')

    ax.clear()
    ax.text(0.1, 0.2, "$"+ Zeros +"$", fontsize=10)
    ax.text(0.1, 0.4, "$"+ Poles +"$", fontsize=10)
    canvas.draw()

def poly_to_latex(poly, variable='Z'):
    poly_coeffs = poly.coef
    poly_degree = len(poly_coeffs)
    latex_str = ''
    for i in range(poly_degree):
        coeff = poly_coeffs[i]
        if coeff == 0:
            continue
        elif coeff > 0 and i > 0:
            latex_str += ' + '
        elif coeff < 0 and i > 0:
            latex_str += ' - '
        if (abs(coeff) != 1 or i == poly_degree) and i != 0:
            latex_str += str(abs(coeff))
        if i == 0:
            latex_str += str(abs(coeff)) + ' '
        if i > 0:
            latex_str += variable + f'^{-i}' + ' '
    return latex_str

def complex_to_latex_set(complex_numbers, variable):
    latex_str = variable + ' = \\{'
    for i, complex_num in enumerate(complex_numbers):
        real, imag = complex_num.real, complex_num.imag
        real_str = "{:.{}f}".format(real, 2)
        imag_str = "{:.{}f}".format(imag, 2)
        if imag >= 0:
            latex_str += real_str + ' + ' + imag_str + 'j'
        else:
            latex_str += real_str + imag_str + 'j'
        if i < len(complex_numbers) - 1:
            latex_str += ', '
    latex_str += '\\}'
    return latex_str

if __name__ == '__main__':
    root = Tk()

    root.title('Conchitas tia Rosa')
    A = []
    B = []
    
    indiceA_1= Entry(root, width=10)
    indiceA_1.grid(row = 0, column = 1)
    indiceA_1.focus()
    indiceA_2= Entry(root, width=10)
    indiceA_2.grid(row = 0, column = 2)
    indiceA_3= Entry(root, width=10)
    indiceA_3.grid(row = 0, column = 3)
    indiceA_4= Entry(root, width=10)
    indiceA_4.grid(row = 0, column = 4)
    indiceB_1= Entry(root, width=10)
    indiceB_1.grid(row = 1, column = 2)
    indiceB_2= Entry(root, width=10)
    indiceB_2.grid(row = 1, column = 3)
    indiceB_3= Entry(root, width=10)
    indiceB_3.grid(row = 1, column = 4)

    vcmd = (indiceA_1.register(validate), '%P')
    indiceA_1.config(validate='all', validatecommand=vcmd)
    vcmd = (indiceA_2.register(validate), '%P')
    indiceA_2.config(validate='all', validatecommand=vcmd)
    vcmd = (indiceA_3.register(validate), '%P')
    indiceA_3.config(validate='all', validatecommand=vcmd)
    vcmd = (indiceA_4.register(validate), '%P')
    indiceA_4.config(validate='all', validatecommand=vcmd)
    vcmd = (indiceA_1.register(validate), '%P')
    indiceB_1.config(validate='all', validatecommand=vcmd)
    vcmd = (indiceB_1.register(validate), '%P')
    indiceB_2.config(validate='all', validatecommand=vcmd)
    vcmd = (indiceB_2.register(validate), '%P')
    indiceB_2.config(validate='all', validatecommand=vcmd)
    vcmd = (indiceB_3.register(validate), '%P')
    indiceB_3.config(validate='all', validatecommand=vcmd)    

    indiceA_Label = Label(root, text = "A")
    indiceA_Label.grid(row = 0, column = 0)
    indiceB_Label = Label(root, text = "B")
    indiceB_Label.grid(row = 1, column = 0)
    IndiceB_Label1 = Label(root, text="1")
    IndiceB_Label1.grid(row=1, column=1)
    muestras_Label = Label(root, text="\n\nMuestras",)
    muestras_Label.grid(row=2, column=0)
    
    horizontal = Scale(root, from_=0, to=100, orient=HORIZONTAL)
    horizontal.set(50)
    horizontal.grid(row=3, column=0)

    BotonImpulso =  Button(root, text="Respuesta al impulso", command=lambda: plotImpulseResponse(B, A, horizontal.get()))    
    BotonROC = Button(root, text="Plano Complejo", command=lambda: zplane(B,A))
    BottonEjemplo = Button (root, text="Ejemplo 1", command=Ejemplo)
    BotonSubir = Button(root, text="Guardar", command = Guardar)
    BotonBorrar = Button(root, text="Borrar", command=Borrar)

    BotonSubir.grid(row = 2, column = 1,columnspan=2, ipadx = 54, ipady=20, pady=5)
    BotonBorrar.grid(row = 2, column = 3,columnspan=2, ipadx = 47, ipady=20)
    BotonImpulso.grid(row = 3, column = 1,columnspan=2, ipadx = 20, ipady=20)
    BotonROC.grid(row = 3, column = 3,columnspan=2, ipadx = 20, ipady=20)
    BottonEjemplo.grid(row = 4, column = 0, ipadx = 20, ipady=20, )
    BotonFuncion = Button(root, text="Función de transferencia",command=lambda: graph(B, A))
    BotonFuncion.grid(row = 6, column = 0, columnspan = 4, padx = 40)
    BotonZP = Button(root, text="Polos y Ceros",command=lambda: graphZP(B, A))
    BotonZP.grid(row = 4, column = 3, columnspan=2, ipadx = 27, ipady=20, pady=5)

    LatexFrame = Frame(root)
    LatexFrame.grid(row = 5, column = 0, columnspan = 4, pady = 10, padx = 10)

    label = Label(LatexFrame)
    label.grid(row = 6, column = 0, columnspan = 4, pady = 10, padx = 10)

    fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)

    canvas = FigureCanvasTkAgg(fig, master=label)
    canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
    canvas._tkcanvas.pack(side="top", fill="both", expand=True)

    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    #entry.insert(0, r"\sum_{i=0}^\infty x_i \frac{y_i}{z_i}")
    #graph() 

    root.bind("<Return>", graph)
    root.bind("<Return>", graphZP)
    root.mainloop()