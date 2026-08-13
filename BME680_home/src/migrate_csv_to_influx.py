"""One-time batch import of existing sensor_data_*.csv files into InfluxDB."""
import glob
from pathlib import Path

import pandas as pd
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB connection settings
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "VRXxOsHsqnucFSelWqcIxSUNO4GLMJHlI5btrPn8Efz5GDNw3k1dNOxiXbd9WCQaBv2b5Vky5DBAhP2EHpL-kg=="
INFLUX_ORG = "CPH"
INFLUX_BUCKET = "SensorsAmadeus34"

DATA_DIR = Path(__file__).resolve().parent / 'data'


def migrate_file(csv_path: Path, write_api) -> int:
    df = pd.read_csv(csv_path, skipinitialspace=True)
    df.columns = df.columns.str.strip()
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.set_index('datetime')

    write_api.write(
        bucket=INFLUX_BUCKET,
        record=df,
        data_frame_measurement_name="SensorsAmadeus34",
        data_frame_tag_columns=["DEVICE_ID"],
    )
    return len(df)


def main():
    csv_paths = sorted(glob.glob(str(DATA_DIR / 'sensor_data_*.csv')))
    if not csv_paths:
        print(f"No CSV files found in {DATA_DIR}")
        return

    with InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        for csv_path in csv_paths:
            row_count = migrate_file(Path(csv_path), write_api)
            print(f"Imported {csv_path} ({row_count} rows)")


if __name__ == '__main__':
    main()
