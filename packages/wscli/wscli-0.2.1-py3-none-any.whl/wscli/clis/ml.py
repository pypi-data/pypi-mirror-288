import ast
import csv
import json
from dataclasses import asdict, dataclass, field
from typing import ClassVar, Dict, List

import click
import requests

from wscli.api_calls import ApiUrl, CallConfig, Method, Scheme, hit_api
from wscli.config import WsConfig, pass_config
from wscli.utils import pprint


def store_jobs(job_file, jobs: List[Dict]):
    with open(job_file, "a") as fid:
        for job in jobs:
            fid.write(json.dumps(job))


def store_predictions(job_file: str, predictions: Dict):
    prediction_data = ast.literal_eval(
        predictions.get("Item", {}).get("data", {})
    )
    with open(f"{job_file}.csv", "w") as fid:
        headers = prediction_data[0].keys()
        writer = csv.DictWriter(fid, fieldnames=headers)
        writer.writeheader()
        writer.writerows(prediction_data)

    click.echo(f"Data saved to {job_file}.csv")


@dataclass(kw_only=True)
class MlConfig:
    domain: str = "localhost"
    scheme: str = "http"
    port: int = 8000
    base_route: str = "ml"
    Key_: ClassVar[str] = "ml"
    job_ids: List[str] = field(default_factory=list)


pass_ml = click.make_pass_decorator(MlConfig, ensure=True)


@click.group()
@click.pass_context
@pass_config
def cli(config: WsConfig, context: click.Context):
    try:
        context.obj = MlConfig(**config.storer.get_key(MlConfig.Key_))
    except TypeError as err:
        click.echo(
            f"error loading the store key '{MlConfig.Key_}'\n"
            f"Error:\n    {err}\n"
            "please use the wscli config commands to fix the issue"
        )
        raise click.Abort()


@cli.command()
@pass_ml
def config_get(ml: MlConfig):
    click.echo(pprint(asdict(ml)))


@cli.command()
@click.option("--domain")
@click.option("--port", type=int)
@click.option("--base-route")
@pass_ml
@pass_config
def config_set(
    config: WsConfig,
    ml: MlConfig,
    domain: str | None = None,
    port: int | None = None,
    base_route: str | None = None,
):
    if domain:
        ml.domain = domain
    if port:
        ml.port = port
    if base_route:
        ml.base_route = base_route
    config.storer.set_key(key=MlConfig.Key_, data=asdict(ml))
    click.echo(pprint(asdict(ml)))


@cli.command()
@pass_ml
@pass_config
def job_api(config: WsConfig, ml: MlConfig):
    try:
        response = hit_api(
            endpoint="/tasks/api",
            api_url=ApiUrl(
                domain=ml.domain,
                scheme=Scheme(ml.scheme),
                port=ml.port,
                base_route=ml.base_route,
            ),
            call_config=CallConfig(
                token=config.login.access_token,
                method=Method.POST,
                content_type="application/json",
            ),
        )

        ml.job_ids.append(response["job_id"])
        config.storer.set_key(key=ml.Key_, data=asdict(ml))
    except requests.ConnectionError as err:
        click.echo(f"failed to make api call:\n   {err}")


@cli.command()
@click.option("--job-file", default="wscli-job.json")
@pass_ml
@pass_config
@click.option("--file-url", prompt=True)
def job_http(config: WsConfig, ml: MlConfig, file_url: str, job_file: str):
    try:
        response = hit_api(
            endpoint="tasks/http",
            api_url=ApiUrl(
                domain=ml.domain,
                scheme=Scheme(ml.scheme),
                port=ml.port,
                base_route=ml.base_route,
            ),
            call_config=CallConfig(
                token=config.login.id_token,
                method=Method.POST,
                content_type="application/json",
            ),
            payload={"http_file": {"url": file_url}, "ml_config": {}},
        )
        job_id = response.json()["job_id"]
        store_jobs(job_file, [{"id": job_id}])
        click.echo(f"Job {job_id} has been succesfully scheduled")
    except requests.ConnectionError as err:
        click.echo(f"failed to make api call:\n   {err}")


@cli.command
@click.option("--job-id", prompt=True)
@click.option("--output-file", type=click.Path())
@pass_config
@pass_ml
def retrieve_results(
    ml: MlConfig, config: WsConfig, job_id: str, output_file: str
):
    try:
        response = hit_api(
            api_url=ApiUrl(
                domain=ml.domain,
                scheme=Scheme(ml.scheme),
                port=ml.port,
                base_route=ml.base_route,
            ),
            call_config=CallConfig(
                token=config.login.id_token,
                method=Method.GET,
                content_type="application/json",
            ),
            endpoint=f"/results-external/?job_id={job_id}",
        )

        predictions = response.json().get("predictions")
        if output_file:
            store_predictions(
                job_file=output_file,
                predictions=response.json().get("predictions"),
            )
        else:
            click.echo(predictions)

    except requests.ConnectionError as err:
        click.echo(f"failed to make api call:\n   {err}")
