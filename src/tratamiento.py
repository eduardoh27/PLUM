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

    def calcular_threshold(self, porcentaje=0.5):
        """
        Calcula el threshold para el tratamiento.
        """
        if self.control_positivo is None or self.control_negativo is None:
            print("WARNING: No se puede calcular el threshold sin ambos controles.")
            self.threshold = None
        else:
            maximo_control_positivo = max(self.control_positivo.intensidades)
            maximo_control_negativo = max(self.control_negativo.intensidades)
            self.threshold = abs(maximo_control_positivo-maximo_control_negativo)*porcentaje + maximo_control_negativo
        return self.threshold
    
    def establecer_estado_muestras(self):
        """
        Establece el estado de las muestras del tratamiento.
        """
        for muestra in self.muestras:
            muestra.establecer_estado_final()
    
    def concluir_tratamiento(self, porcentaje=0.5):
        """
        Establece el estado de las muestras del tratamiento.
        """
        self.calcular_threshold(porcentaje)
        if self.threshold is not None:
            self.establecer_estado_muestras()
        return self.threshold

    def obtener_controles(self):
        """
        Devuelve una lista con los controles del tratamiento.
        """
        return [c for c in [self.control_positivo, self.control_negativo] if c is not None]

    def __str__(self):
        return f"Tratamiento: nombre = {self.nombre}, # muestras = {len(self.muestras)},\
            control_positivo = {self.control_positivo}, control_negativo = {self.control_negativo}"