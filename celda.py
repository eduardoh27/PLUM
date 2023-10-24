class Celda:

    def __init__(self, tipo, coordenada, circulo=None):
        self.tipo = tipo  # ej. 'muestra_normal', 'control_positivo'
        self.coordenada = coordenada  # ej. (2,1)
        self.circulo = circulo  # Información del círculo detectado, si es que se ha detectado.
        self.intensidades = []  # Lista para guardar las intensidades a lo largo del tiempo
        #self.nombre = nombre  # ej. 'SARS-Cov'

    def agregar_intensidad(self, valor):
        self.intensidades.append(valor)

    def __str__(self):
        return f"Celda: tipo = {self.tipo}, coordenada = {self.coordenada}, circulo = {self.circulo}, intensidades = {self.intensidades}"
