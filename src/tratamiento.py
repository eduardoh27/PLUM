class Tratamiento:

    def __init__(self, nombre):
        self.nombre = nombre
        self.muestras = []
        self.control_positivo = None
        self.control_negativo = None
        self.threshold = None

    def agregar_muestra(self, muestra):
        self.muestras.append(muestra)

    def agregar_control_positivo(self, control_positivo):
        self.control_positivo = control_positivo
    
    def agregar_control_negativo(self, control_negativo):
        self.control_negativo = control_negativo

    def calcular_threshold(self):
        """
        Calcula el threshold para el tratamiento.
        """
        if self.control_positivo is None or self.control_negativo is None:
            print("No se puede calcular el threshold sin ambos controles.")
            self.threshold = None
        else:
            maximo_control_positivo = max(self.control_positivo.intensidades)
            maximo_control_negativo = max(self.control_negativo.intensidades)
            porcentaje = 0.5
            self.threshold = abs(maximo_control_positivo-maximo_control_negativo)*porcentaje + maximo_control_negativo
        return self.threshold

    def __str__(self):
        return f"Tratamiento: nombre = {self.nombre}, # muestras = {len(self.muestras)},\
            control_positivo = {self.control_positivo}, control_negativo = {self.control_negativo}"