from ovos_plugin_manager.templates.vad import VADEngine

from ovos_vad_plugin_energy.energy import EnergyVad


class EnergyVAD(VADEngine):
    def __init__(self, config=None, sample_rate=None):
        super().__init__(config, sample_rate)
        threshold = self.config.get("threshold")
        samples_per_chunk = self.config.get("samples_per_chunk")
        calibrate_seconds = self.config.get("calibrate_seconds")
        calibrate_zscore_threshold = self.config.get("calibrate_zscore_threshold")
        self.vad = EnergyVad(
            threshold=threshold,
            samples_per_chunk=samples_per_chunk,
            calibrate_seconds=calibrate_seconds,
            calibrate_zscore_threshold=calibrate_zscore_threshold
        )

    def reset(self):
        self.vad.reset_calibration()

    def is_silence(self, chunk):
        return self.vad.process_chunk(chunk)
