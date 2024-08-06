from dataclasses import dataclass
import time

from prometheus_client import start_http_server, Gauge, Enum

import logging
from .rocm_smi_env import get_rsmi

logger = logging.getLogger(__name__)


class AppMetrics:
    """
    Representation of Prometheus metrics and loop to fetch and transform
    application metrics into Prometheus metrics.
    """
    @dataclass
    class Config:
        port: int
        polling_interval_seconds: int
        rsmi = None

    def __init__(self, rsmi, config: Config):
        self.rsmi = rsmi
        self.config = config

        self.dev_list = self.rsmi.listDevices()
        self.available_temp_type = self.rsmi.getTemperatureLabel(self.dev_list)

        # Define Prometheus metrics to collect
        self.gpu_utils = [None] * len(self.dev_list)
        self.gpu_mem_utils = [None] * len(self.dev_list)
        self.gpu_temps = [None] * len(self.dev_list)

        # TODO: The schema of prom metrics should be made consistent with
        # Nvidia DCGM-exporter.
        for idx, dev in enumerate(self.dev_list):
            self.gpu_utils[idx] = Gauge(f"gpu_util_{dev}", "GPU utilization")
            self.gpu_mem_utils[idx] = Gauge(f"gpu_mem_util_{dev}", "GPU memory utilization")
            self.gpu_temps[idx] = Gauge(f"gpu_temp_{dev}", "GPU temporary")

    def run_metrics_loop(self):
        """Metrics fetching loop"""
        start_http_server(self.config.port)
        while True:
            logger.info(f"Fetching metrics ...")
            self.fetch()
            time.sleep(self.config.polling_interval_seconds)

    def fetch(self):
        """
        Get metrics from application and refresh Prometheus metrics.
        """
        self.fetch_util()
        self.fetch_mem_util()
        self.fetch_temp()

    def fetch_util(self):
        for idx, device in enumerate(self.dev_list):
            util = self.rsmi.getGpuUse(device)
            self.gpu_utils[idx].set(util)
            print(f"utilization: {util}%")
        
    def fetch_mem_util(self):
        for idx, dev in enumerate(self.dev_list):
            mem_alloc = self.rsmi.getMemInfo(dev, 'vram')
            self.gpu_mem_utils[idx].set(mem_alloc[0]/mem_alloc[1])
            print(f"{mem_alloc[0]/mem_alloc[1]}")

    def fetch_temp(self):
        for idx, device in enumerate(self.dev_list):
            temp = self.rsmi.getTemp(device, self.available_temp_type)
            self.gpu_temps[idx].set(temp)
            print(f"temperature: {temp}")
    

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Parse command line arguments for port and polling interval.')

    parser.add_argument('--port', type=int, default=9001, help='Port number to use.')
    parser.add_argument('--polling-interval-seconds', type=int, default=5, help='Polling interval in seconds.')

    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()

    app_metrics = AppMetrics(
        get_rsmi(),
        AppMetrics.Config(
            port=args.port,
            polling_interval_seconds=args.polling_interval_seconds
        )
    )
    app_metrics.run_metrics_loop()

if __name__ == "__main__":
    main()
