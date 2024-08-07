# bionic_tensor.py

import numpy as np
import sympy as sp
from pydantic import BaseModel, Field
from typing import List

class BionicTensor(BaseModel):
    dimensions: List[int] = Field(default_factory=list)
    tensor: sp.MutableDenseNDimArray = None

    def __init__(self, **data):
        super().__init__(**data)
        self.tensor = sp.MutableDenseNDimArray([0] * np.prod(self.dimensions), self.dimensions)

    def set_element(self, indices: tuple, value):
        """
        Establece un valor en el tensor en la posición especificada por indices.

        :param indices: Índices del elemento a establecer.
        :param value: Valor a asignar al elemento.
        """
        self.tensor[indices] = value

    def get_element(self, indices: tuple):
        """
        Obtiene un valor del tensor en la posición especificada por indices.

        :param indices: Índices del elemento a obtener.
        :return: Valor del elemento.
        """
        return self.tensor[indices]

    class Config:
        arbitrary_types_allowed = True
