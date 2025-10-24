"""
Casos de prueba para validar backoff exponencial con jitter reproducible.
Enfoque: Fijar seed para hacer determinista la aleatoriedad y verificar que
el backoff no excede el cap, y medir reintentos.
"""

import os
import random
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from src.servicios.backoff import bounded_jitter_backoff


class TestBackoffWithSeededJitter:
    """Casos de prueba para backoff determinista con seed fijo"""

    def test_backoff_respects_cap(self):
        """
        Verifica que el backoff no excede jitter máximo
        """
        random.seed(1337)
        base = 0.05
        cap = 0.5

        @bounded_jitter_backoff(tries=4, base=base, cap=cap)
        def fail_twice():
            fail_twice.attempts += 1
            if fail_twice.attempts < 3:
                raise ValueError("Fallo intencional")
            return "success"

        fail_twice.attempts = 0

        with patch("src.servicios.backoff.time.sleep") as mock_sleep:
            result = fail_twice()

            assert result == "success"
            assert fail_twice.attempts == 3
            assert mock_sleep.call_count == 2

            max_sleep = cap + base
            for call in mock_sleep.call_args_list:
                sleep_time = call[0][0]
                assert sleep_time <= max_sleep, (
                    f"Se excede el jitter máximo {max_sleep}"
                )

    def test_backoff_jitter_is_deterministic_with_seed(self):
        """
        Verifica que con seed fijo, el jitter produce los mismos tiempos.
        Ejecuta dos veces la misma función y compara los tiempos de sleep.
        """
        base = 0.05
        cap = 0.5

        def get_sleep_times():
            random.seed(42)

            @bounded_jitter_backoff(tries=3, base=base, cap=cap)
            def fail_once():
                fail_once.attempts += 1
                if fail_once.attempts < 2:
                    raise RuntimeError("Fallo")
                return "ok"

            fail_once.attempts = 0

            sleep_times = []
            with patch("src.servicios.backoff.time.sleep") as mock_sleep:
                fail_once()
                sleep_times = [call[0][0] for call in mock_sleep.call_args_list]

            return sleep_times

        times_1 = get_sleep_times()
        times_2 = get_sleep_times()

        assert times_1 == times_2, "Con el mismo seed, los tiempos deben ser idénticos"

    def test_backoff_exhaustion_raises_exception(self):
        """
        Verifica que cuando se agotan los intentos, se lanza la excepción.
        """
        random.seed(1337)

        @bounded_jitter_backoff(tries=2, base=0.05, cap=0.5)
        def always_fails():
            always_fails.call_count += 1
            raise ValueError("Siempre falla")

        always_fails.call_count = 0

        with patch("src.servicios.backoff.time.sleep"):
            with pytest.raises(ValueError, match="Siempre falla"):
                always_fails()

            # Verifica que intentó exactamente 'tries' veces
            assert always_fails.call_count == 2
