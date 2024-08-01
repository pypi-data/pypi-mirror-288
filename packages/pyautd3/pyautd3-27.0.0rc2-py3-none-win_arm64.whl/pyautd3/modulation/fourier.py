from collections.abc import Iterable

import numpy as np

from pyautd3.driver.datagram.modulation.base import ModulationBase
from pyautd3.driver.datagram.modulation.cache import IntoModulationCache
from pyautd3.driver.datagram.modulation.radiation_pressure import IntoModulationRadiationPressure
from pyautd3.driver.datagram.modulation.transform import IntoModulationTransform
from pyautd3.native_methods.autd3capi_driver import ModulationPtr

from .sine import Sine


class Fourier(
    IntoModulationCache["Fourier"],
    IntoModulationRadiationPressure["Fourier"],
    IntoModulationTransform["Fourier"],
    ModulationBase["Fourier"],
):
    _components: list[Sine]

    def __init__(self: "Fourier", iterable: Iterable[Sine]) -> None:
        super().__init__()
        self._components = list(iterable)

    def _modulation_ptr(self: "Fourier") -> ModulationPtr:
        components: np.ndarray = np.ndarray(len(self._components), dtype=ModulationPtr)
        for i, m in enumerate(self._components):
            components[i]["_0"] = m._modulation_ptr()._0
        return self._components[0]._mode.fourier_ptr(
            components,
            len(self._components),
            self._loop_behavior,
        )
