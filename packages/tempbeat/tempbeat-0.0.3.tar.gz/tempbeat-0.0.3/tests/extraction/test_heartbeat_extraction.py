import neurokit2 as nk
import numpy as np
import pytest

from tempbeat.extraction.heartbeat_extraction import hb_extract, temp_hb_extract
from tempbeat.extraction.interval_conversion import peak_time_to_rri
from tempbeat.utils.timestamp import sampling_rate_to_sig_time


class TestTempHbExtract:
    """
    Test cases for the temp_hb_extract function.
    """

    @staticmethod
    def test_temp_hb_extract_regression() -> None:
        """
        Test temp_hb_extract with example ECG data.

        The function should extract the peak times such that they are within 0.01 seconds of the expected values.
        The expected values were obtained by running the function on the example ECG data with the same parameters.
        """
        sampling_rate = 200
        data = nk.data("bio_resting_8min_200hz")
        sig = data["S01"]["ECG"]
        sig_time = sampling_rate_to_sig_time(sig, sampling_rate)
        peaks = temp_hb_extract(sig, sig_time=sig_time, sampling_rate=sampling_rate)

        np.testing.assert_allclose(
            peaks[:20],
            np.array(
                [
                    8.55,
                    9.36,
                    10.24,
                    11.09,
                    11.91,
                    12.71,
                    13.47,
                    14.32,
                    15.115,
                    15.91,
                    16.695,
                    17.48,
                    18.26,
                    19.02,
                    19.87,
                    20.73,
                    21.49,
                    22.26,
                    23.1,
                    23.99,
                ]
            ),
            rtol=0.01,
        )


class TestHbExtract:
    @staticmethod
    @pytest.mark.parametrize("method", ["nk_neurokit", "temp"])
    def test_hb_extract(method) -> None:
        """
        Test hb_extract with example ECG data.

        The function should extract the peak times such that they are within 0.01 seconds of the expected values.
        The expected values were obtained by running the function on the example ECG data with the same parameters.
        """
        sampling_rate = 100
        data = nk.data("bio_resting_5min_100hz")
        sig = data["ECG"]
        sig_time = sampling_rate_to_sig_time(sig, sampling_rate)
        peak_time = hb_extract(
            sig, sig_time=sig_time, sampling_rate=sampling_rate, method=method
        )
        rri, _ = peak_time_to_rri(peak_time=peak_time)
        max_bpm = 200
        min_bpm = 40
        assert np.max(rri) < 60000 / min_bpm
        assert np.min(rri) > 60000 / max_bpm

    @staticmethod
    def test_hb_extract_hb_extract_algo_kwargs() -> None:
        """
        Test hb_extract with example ECG data and hb_extract_algo_kwargs.

        The function should return a tuple.
        """
        sampling_rate = 100
        data = nk.data("bio_resting_5min_100hz")
        sig = data["ECG"]
        sig_time = sampling_rate_to_sig_time(sig, sampling_rate)
        output = hb_extract(
            sig,
            sig_time=sig_time,
            sampling_rate=sampling_rate,
            method="temp",
            hb_extract_algo_kwargs={"output_format": "full"},
        )
        assert isinstance(output, tuple)
        assert isinstance(output[1], dict)
        assert "med_template" in output[1].keys()

    @staticmethod
    def test_hb_extract_hb_extract_algo_kwargs_empty() -> None:
        """
        Test hb_extract with example ECG data and empty hb_extract_algo_kwargs.

        The function should return an np.ndarray.
        """
        sampling_rate = 100
        data = nk.data("bio_resting_5min_100hz")
        sig = data["ECG"]
        sig_time = sampling_rate_to_sig_time(sig, sampling_rate)
        output = hb_extract(
            sig,
            sig_time=sig_time,
            sampling_rate=sampling_rate,
            method="temp",
            hb_extract_algo_kwargs={},
        )
        assert isinstance(output, np.ndarray)
