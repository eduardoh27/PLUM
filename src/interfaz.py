import tkinter as tk
from tkinter import messagebox

class App:
    def __init__(self, root, dimensiones):
        self.root = root
        self.root.title("Seleccionar Celdas")

        self.buttons = {}
        self.selected_cells = []
        self.control_pos_cell = None
        self.control_neg_cell = None

        self.mode = "Ensayo"  # Modo predeterminado

        # Botones de selección
        self.cp_btn = tk.Button(self.root, text="C.P.", width=10, height=2, command=lambda: self.set_mode("C.P."))
        self.cp_btn.grid(row=0, column=9)
        
        self.cn_btn = tk.Button(self.root, text="C.N.", width=10, height=2, command=lambda: self.set_mode("C.N."))
        self.cn_btn.grid(row=1, column=9)
        
        self.ensayo_btn = tk.Button(self.root, text="Ensayo", width=10, height=2, command=lambda: self.set_mode("Ensayo"))
        self.ensayo_btn.grid(row=2, column=9)

        dimension_x, dimension_y = dimensiones
        row_labels = [chr(65 + i) for i in range(dimension_y)] # row_labels = ['A', 'B', 'C', 'D', 'E'] in case dimension_y = 5 

        # Crear botones para las celdas
        for i in range(dimension_y):
            for j in range(dimension_x):
                btn = tk.Button(self.root, text=f"{row_labels[i]}{j+1}", width=10, height=3, command=lambda i=i, j=j: self.toggle_cell(i, j))
                btn.grid(row=i, column=j)
                self.buttons[(i, j)] = btn

        # Botones de control
        self.ok_btn = tk.Button(self.root, text="OK", command=self.ok_pressed)
        self.ok_btn.grid(row=dimension_y, column=3, columnspan=2)
        
        self.back_btn = tk.Button(self.root, text="Regresar", command=self.reset_selection)
        self.back_btn.grid(row=dimension_y, column=5, columnspan=2)


    def set_mode(self, mode):
        self.mode = mode

    def toggle_cell(self, i, j):
        if self.mode == "Ensayo":
            if (i, j) in self.selected_cells:
                self.buttons[(i, j)].config(bg='SystemButtonFace')
                self.selected_cells.remove((i, j))
            else:
                self.buttons[(i, j)].config(bg='green')
                self.selected_cells.append((i, j))
        elif self.mode == "C.P.":
            if self.control_pos_cell:
                self.buttons[self.control_pos_cell].config(bg='SystemButtonFace')
            self.control_pos_cell = (i, j)
            self.buttons[(i, j)].config(bg='blue')
        elif self.mode == "C.N.":
            if self.control_neg_cell:
                self.buttons[self.control_neg_cell].config(bg='SystemButtonFace')
            self.control_neg_cell = (i, j)
            self.buttons[(i, j)].config(bg='red')

    def ok_pressed(self):
        answer = messagebox.askquestion("Confirmar", "¿Está seguro de que estas son las celdas que quiere analizar?")
        if answer == 'yes':
            sorted_cells = sorted(self.selected_cells, key=lambda x: (x[0], x[1]))
            #print("Celdas seleccionadas:", [(i+1, j+1) for i, j in sorted_cells])
            if self.control_pos_cell:
                pass
                #print("Control Positivo:", (self.control_pos_cell[0] + 1, self.control_pos_cell[1] + 1))
            if self.control_neg_cell:
                pass
                #print("Control Negativo:", (self.control_neg_cell[0] + 1, self.control_neg_cell[1] + 1))
            self.root.quit()

    def reset_selection(self):
        for i, j in self.selected_cells:
            self.buttons[(i, j)].config(bg='SystemButtonFace')
        if self.control_pos_cell:
            self.buttons[self.control_pos_cell].config(bg='SystemButtonFace')
        if self.control_neg_cell:
            self.buttons[self.control_neg_cell].config(bg='SystemButtonFace')
        self.selected_cells.clear()
        self.control_pos_cell = None
        self.control_neg_cell = None
        self.mode = "Ensayo"  # Reiniciar al modo predeterminado

    def get_selected_cells(self):
        sorted_cells = sorted(self.selected_cells, key=lambda x: (x[0], x[1]))
        results = {
            "Muestras": [(i+1, j+1) for i, j in sorted_cells],
            "Control Positivo": None if not self.control_pos_cell else (self.control_pos_cell[0] + 1, self.control_pos_cell[1] + 1),
            "Control Negativo": None if not self.control_neg_cell else (self.control_neg_cell[0] + 1, self.control_neg_cell[1] + 1)
        }
        return results


class DialogoNumeroTratamientos(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.resultado = None
        tk.Label(self, text="¿Cuántos tratamientos va a analizar?").pack(pady=20)
        tk.Button(self, text="1 Tratamiento", command=lambda: self.set_result(1)).pack(side=tk.LEFT, padx=20)
        tk.Button(self, text="2 Tratamientos", command=lambda: self.set_result(2)).pack(side=tk.RIGHT, padx=20)

    def set_result(self, valor):
        self.resultado = valor
        self.destroy()

def main(dimensiones):

    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal

    # Crear y mostrar el diálogo
    dialogo = DialogoNumeroTratamientos(root)
    root.wait_window(dialogo)

    # Comprobar si se ha establecido un resultado
    if dialogo.resultado is None:
        print("No se seleccionó ningún número de tratamientos. Saliendo.")
        return

    num_tratamientos = dialogo.resultado

    # Mostrar la ventana principal
    root.deiconify()
    
    app = App(root, dimensiones)
    resultados = {}

    for tratamiento in range(1, num_tratamientos + 1):
        # Restablecer selecciones previas
        app.reset_selection()

        # Mostrar mensaje para seleccionar celdas del tratamiento actual
        messagebox.showinfo("Información", f"Seleccione las celdas del tratamiento {tratamiento}")

        root.mainloop()
        
        # Almacenar resultados
        resultados[f"Tratamiento {tratamiento}"] = app.get_selected_cells()

    # Imprimir resultados
    imprimir = False
    if imprimir:
        for tratamiento, celdas in resultados.items():
            print(tratamiento)
            print("Celdas seleccionadas:", celdas["Celdas"])
            if celdas["Control Positivo"]:
                print("Control Positivo:", celdas["Control Positivo"])
            if celdas["Control Negativo"]:
                print("Control Negativo:", celdas["Control Negativo"])
            print()

    return resultados

if __name__ == "__main__":
    dimensiones = (8, 5)
    main(dimensiones)
