import os
import psutil
import pandas as pd
import csv
import logging
from nvitop import ResourceMetricCollector, Device
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class PerformanceLogger:
    """Performance logger class."""

    def __init__(self, log_dir, log_node):
        os.makedirs(log_dir, exist_ok=True)
        self.log_dir = log_dir
        self.log_node = log_node
        self.df = pd.DataFrame()
        self.tag = None
        self.filepath = None
        self.writer = None
        self.file = None
        self.first_collect = True
        self.collector = ResourceMetricCollector(Device.cuda.all()).daemonize(
            on_collect=self.on_collect,
            interval=1.0,
        )
        self.cpu_count = psutil.cpu_count(logical=False)
        self.start_time = None

    def new_res(self):
        """Creates a new resource file directory and sets the file path."""
        os.makedirs(self.log_dir, exist_ok=True)
        self.filepath = f"{self.log_dir}/node-{self.log_node}.csv"

        # Open the file and set up the CSV writer
        file_exists = os.path.exists(self.filepath)
        self.file = open(self.filepath, 'a', newline='', encoding='utf-8')
        if file_exists:
            self.writer = csv.DictWriter(self.file, fieldnames=self.df.columns)
        else:
            self.writer = None
        logging.info("New resource file created: %s", self.filepath)

    def change_tag(self, tag):
        """Changes the tag and restarts the collector if necessary."""
        if self.filepath is not None:
            self.stop()
        self.tag = tag
        self.new_res()

    def stop(self):
        """Stops the collector and saves the collected data to a CSV file."""
        if self.file:
            self.file.close()
        self.df = pd.DataFrame()

    def get_cpu_usage_per_core(self):
        """Returns the CPU usage per core."""
        cpu_percent = psutil.cpu_percent(interval=0.1, percpu=True)
        return {f"cpu_core_{i+1} (%)": percent for i, percent in enumerate(cpu_percent[:self.cpu_count])}

    def clean_column_name(self, col):
        """Cleans the column name."""
        if col.startswith("metrics-daemon/host/"):
            col = col[len("metrics-daemon/host/"):]
        return col

    def on_collect(self, metrics):
        """Collects and processes metrics."""
        metrics['tag'] = self.tag
        cpu_metrics = self.get_cpu_usage_per_core()
        metrics.update(cpu_metrics)
        df_metrics = pd.DataFrame.from_records([metrics])
        df_metrics.columns = [self.clean_column_name(col) for col in df_metrics.columns]

        if self.df.empty:
            self.df = df_metrics
        else:
            self.df = self.df.reindex(columns=list(self.df.columns) +
                                      [col for col in df_metrics.columns if col not in self.df.columns])
            df_metrics = df_metrics.reindex(columns=self.df.columns, fill_value=None)
            self.df = pd.concat([self.df, df_metrics], ignore_index=True)

        self._write_to_file(df_metrics)

        return True

    def _write_to_file(self, row):
        """Writes a row of data to the file."""
        row_dict = row.to_dict(orient='records')[0]  # Convert DataFrame row to dictionary
        if self.first_collect:
            with open(self.filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=row.columns)
                writer.writeheader()
                writer.writerow(row_dict)
            self.first_collect = False
            logging.info("First collection completed with header: %s", self.filepath)
        else:
            with open(self.filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.df.columns)
                writer.writerow(row_dict)
                f.flush()
            # logging.info(f"Appended row to file: {self.filepath}")

    def start(self):
        """Starts the performance logger."""
        self.start_time = time.time()

    def cleanup(self):
        """Stops the collector and ensures all data is saved."""
        self.stop()

    def __del__(self):
        """Destructor to ensure cleanup is called."""
        self.cleanup()
