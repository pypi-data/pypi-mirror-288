#!/usr/bin/env python3

import tomllib
import click
import pandas
import sqlite3
import jinja2
import pathlib
import shutil
import plotly.express as px

PLOTLY_JS = pathlib.Path("./plotly-2.32.0.min.js")
INPUT_TEMPLATE = pathlib.Path("./graph.html.jinja")


@click.command(
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.option(
    "-d",
    "--database",
    help="The database to load the results from",
    metavar="DATABASE",
    required=True,
    type=click.Path(dir_okay=False, exists=True),
)
@click.argument("output_dir", nargs=1)
def main(database, output_dir):
    """Create HTML plots of the results of DATABASE."""
    con = sqlite3.connect(database)
    tmp = pandas.read_sql(
        'SELECT "date","grid5000.site","grid5000.cluster",'
        '"experiment.cores","experiment.libblas_choice","experiment.problem_type",'
        '"experiment.scaling_type","timings.zzz_solve.wall_tot" '
        "FROM results",
        con,
    )
    con.close()
    df = tmp.rename(
        columns=dict(zip(tmp.columns, [x.split(".", 1)[-1] for x in tmp.columns]))
    )
    df["date"] = pandas.to_datetime(df["date"], format="ISO8601")
    for column in ["cores", "zzz_solve.wall_tot"]:
        df[column] = pandas.to_numeric(df[column])
    for problem_type in ["poisson", "elasticity"]:
        for scaling_type in ["weak", "strong"]:
            # The DataFrame for the speedup plot.
            tmp = df[
                (df["problem_type"] == problem_type)
                & (df["scaling_type"] == scaling_type)
            ]
            tmp = tmp.sort_values(by="cores")
            tmp["date"] = tmp["date"].transform(lambda d: d.strftime("%Y-%m-%d"))
            t1 = tmp["zzz_solve.wall_tot"].iloc[0]
            if scaling_type == "weak":
                tmpcol = tmp["zzz_solve.wall_tot"] / tmp["cores"]
                tmp["speedup"] = tmpcol.transform(lambda t: t1 / t)
            elif scaling_type == "strong":
                tmp["speedup"] = tmp["zzz_solve.wall_tot"].transform(lambda t: t1 / t)
            else:
                raise ValueError("Unimplemented scaling_type value.")
            tmp["cluster.site"] = tmp.apply(
                lambda row: f'{row["cluster"]}.{row["site"]}', axis="columns"
            )
            speedup_range = [
                tmp["speedup"].min() * 0.9 - 1,
                tmp["speedup"].max() * 1.1 + 1,
            ]
            runtime_range = [
                tmp["zzz_solve.wall_tot"].min() * 0.9 - 1,
                tmp["zzz_solve.wall_tot"].max() * 1.1 + 1,
            ]
            fig_sc = px.line(
                tmp,
                x="cores",
                y="speedup",
                color="cluster.site",
                animation_frame="date",
                range_y=speedup_range,
                labels={"speedup": "speedup %"},
                title="speedup over cores",
            )
            fig_sc.update_layout(yaxis_tickformat=".2%")
            fig_sd = px.line(
                tmp,
                x="date",
                y="speedup",
                color="cluster.site",
                animation_frame="cores",
                title="speedup over time",
                range_y=speedup_range,
                labels={"speedup": "speedup %"},
            )
            fig_sd.update_layout(yaxis_tickformat=".2%")
            fig_sd.update_xaxes(
                rangeslider_visible=True,
                tickformatstops=[
                    dict(dtickrange=[None, 1000], value="%H:%M:%S.%L ms"),
                    dict(dtickrange=[1000, 60000], value="%H:%M:%S s"),
                    dict(dtickrange=[60000, 3600000], value="%H:%M m"),
                    dict(dtickrange=[3600000, 86400000], value="%H:%M h"),
                    dict(dtickrange=[86400000, 604800000], value="%e. %b d"),
                    dict(dtickrange=[604800000, "M1"], value="%e. %b w"),
                    dict(dtickrange=["M1", "M12"], value="%b '%y M"),
                    dict(dtickrange=["M12", None], value="%Y Y"),
                ],
            )
            fig_rc = px.line(
                tmp,
                x="cores",
                y="zzz_solve.wall_tot",
                color="cluster.site",
                animation_frame="date",
                title="runtime over cores",
                range_y=runtime_range,
                labels={"zzz_solve.wall_tot": "runtime (s)"},
            )
            fig_rd = px.line(
                tmp,
                x="date",
                y="zzz_solve.wall_tot",
                color="cluster.site",
                animation_frame="cores",
                title="runtime over time",
                range_y=runtime_range,
                labels={"zzz_solve.wall_tot": "runtime (s)"},
            )
            fig_rd.update_xaxes(
                rangeslider_visible=True,
                tickformatstops=[
                    dict(dtickrange=[None, 1000], value="%H:%M:%S.%L ms"),
                    dict(dtickrange=[1000, 60000], value="%H:%M:%S s"),
                    dict(dtickrange=[60000, 3600000], value="%H:%M m"),
                    dict(dtickrange=[3600000, 86400000], value="%H:%M h"),
                    dict(dtickrange=[86400000, 604800000], value="%e. %b d"),
                    dict(dtickrange=[604800000, "M1"], value="%e. %b w"),
                    dict(dtickrange=["M1", "M12"], value="%b '%y M"),
                    dict(dtickrange=["M12", None], value="%Y Y"),
                ],
            )
            # The Jinja2 template.
            template = {
                "fig_speedup_cores": fig_sc.to_html(
                    full_html=False, include_plotlyjs=False, auto_play=False
                ),
                "fig_speedup_date": fig_sd.to_html(
                    full_html=False, include_plotlyjs=False, auto_play=False
                ),
                "fig_runtime_cores": fig_rc.to_html(
                    full_html=False, include_plotlyjs=False, auto_play=False
                ),
                "fig_runtime_date": fig_rd.to_html(
                    full_html=False, include_plotlyjs=False, auto_play=False
                ),
                "g5k_attribute": "Experiments presented in this page were "
                "carried out using the Grid'5000 testbed, supported by a "
                "scientific interest group hosted by Inria and including "
                "CNRS, RENATER and several Universities as well as other "
                "organizations (see <a "
                'href="https://www.grid5000.fr">https://www.grid5000.fr</a>).',
                "title": f"Grid'5000 FEniCS experiments, {scaling_type} {problem_type}",
                "plotly_js": PLOTLY_JS,
            }
            # Generate and write out to HTML file.
            shutil.copy(PLOTLY_JS, output_dir)
            with open(
                pathlib.Path(output_dir) / f"{scaling_type}_{problem_type}.html",
                "w",
                encoding="utf-8",
            ) as f:
                with open(INPUT_TEMPLATE) as template_file:
                    jinja_template = jinja2.Template(template_file.read())
                    f.write(jinja_template.render(template))

    # For the runtime plot, see also time series with range selector
    # <https://plotly.com/python/time-series/>


if __name__ == "__main__":
    main()
