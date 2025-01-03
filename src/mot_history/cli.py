import click

from . import console, paths
from .api_client import APIClient
from .zip_to_parquet import convert_zip_to_parquet

client = APIClient()


@click.group()
def cli():
    """This is a CLI to use the MOT History API."""


@cli.command()
@click.argument("vrm")
def vrm(vrm: str):
    """Lookup MOT history for a single vehicle by VRM (vehicle registration mark)."""
    console.print(client.get_vrm(vrm))


@cli.command()
@click.argument("vin")
def vin(vin: str):
    """Lookup MOT history for a single vehicle by VIN."""
    console.print(client.get_vin(vin))


@cli.command()
def bulk_urls():
    """Get time-limited download URLs for bulk MOT history data."""
    console.print(client.get_bulk_urls())


@cli.command()
def bulk_data_download():
    """Downloads bulk MOT history data via the time-limited download URLs."""
    client.download_bulk_data()


@cli.command()
def convert_bulk_data_to_parquet():
    """Converts downloaded bulk MOT history data to Parquet files."""
    # TODO: implement this properly
    latest_bulk_datafile = sorted(paths.data_dir.glob("bulk-light-vehicle_*.zip"), reverse=True)[0]
    convert_zip_to_parquet(
        zip_file_path=latest_bulk_datafile,
        parquet_dir_path=paths.data_dir / "bulk.parquet.d",
    )


if __name__ == "__main__":
    cli()
