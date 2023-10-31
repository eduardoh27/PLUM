class Celda:

    def __init__(self, tipo, coordenada, tratamiento, circulo=None):
        """
        Inicializa una celda con sus propiedades básicas.

        :param tipo: Tipo de celda (ej. 'muestra_normal', 'control_positivo').
        :param coordenada: Coordenadas de la celda en la grilla (ej. (2,1)).
        :param circulo: Información del círculo detectado, si es que se ha detectado. Default es None.
        """
        self.tipo = tipo  # ej. 'muestra_normal', 'control_positivo'
        self.coordenada = coordenada  # ej. (2,1)
        self.circulo = circulo  # Información del círculo detectado, si es que se ha detectado.
        self.intensidades = []  # Lista para guardar las intensidades a lo largo del tiempo
        self.tratamiento = tratamiento
        self.estado = 'inicial'
        #self.nombre = nombre  # ej. 'SARS-Cov'

    def agregar_intensidad(self, valor):
        """
        Agrega un nuevo valor de intensidad a la lista de intensidades de la celda.

        :param valor: Valor de intensidad a agregar.
        """
        self.intensidades.append(valor)

    def establecer_estado_error(self):
        """
        Establece el estado de la celda como error.
        """
        self.estado = 'error'

    def establecer_estado_positivo(self):
        """
        Establece el estado de la celda como positivo.
        """
        self.estado = 'positivo'
    
    def establecer_estado_negativo(self):
        """
        Establece el estado de la celda como negativo.
        """
        self.estado = 'negativo'
    
    def establecer_estado_final(self):
        """
        Establece el estado de la celda como final.
        """
        if self.estado != 'error':
            mayor_threshold = max(self.intensidades) > self.tratamiento.threshold
            if mayor_threshold:
                self.estado = 'positivo'
            else:
                self.estado = 'negativo'

    def __str__(self):
        """
        Devuelve una representación en cadena de caracteres de la celda.

        :return: Cadena de caracteres que representa la celda.
        """
        return f"Celda: tipo = {self.tipo}, coordenada = {self.coordenada}, tratamiento = {self.tratamiento}, circulo = {self.circulo}, intensidades = {self.intensidades}"