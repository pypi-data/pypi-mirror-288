import os
import subprocess
import pprint
import time
import itertools

import numpy as np
import pyarrow.parquet as pq
import pyarrow.dataset as ds
import yaml

from rail.utils import catalog_utils
from rail.core.stage import RailPipeline
from rail.utils.project import RailProject
from rail.cli.pipe_options import RunMode


def handle_command(run_mode, command_line):
    print("subprocess:", *command_line)
    _start_time = time.time()
    print(">>>>>>>>")
    if run_mode == RunMode.dry_run:
        # print(command_line)
        command_line.insert(0, "echo")
        finished = subprocess.run(command_line)
    elif run_mode == RunMode.bash:
        # return os.system(command_line)
        finished = subprocess.run(command_line)
    elif run_mode == RunMode.slurm:
        raise RuntimeError("handle_command should not be called with run_mode == RunMode.slurm")

    returncode = finished.returncode
    _end_time = time.time()
    _elapsed_time = _end_time - _start_time
    print("<<<<<<<<")
    print(f"subprocess completed with status {returncode} in {_elapsed_time} seconds\n")
    return returncode


def handle_commands(run_mode, command_lines, script_path=None):

    if run_mode in [RunMode.dry_run, RunMode.bash]:
        for command_ in command_lines:
            retcode = handle_command(run_mode, command_)
            if retcode:
                return retcode
        return 0
    # At this point we are using slurm and need a script to send to batch
    if script_path is None:
        raise ValueError(
            "handle_commands with run_mode == RunMode.slurm requires a path to a script to write",
        )

    try:
        os.makedirs(os.path.dirname(script_path))
    except:
        pass
    with open(script_path, 'w') as fout:
        fout.write("#!/usr/bin/bash\n\n")
        for command_ in command_lines:
            com_line = ' '.join(command_)
            fout.write(f"{com_line}\n")

    script_log = script_path.replace('.sh', '.log')
    try:
        with subprocess.Popen(
                ["sbatch", "-o", script_log, "--mem", "16448", "-p", "milano", "--parsable", script_path],
                stdout=subprocess.PIPE,
        ) as sbatch:
            assert sbatch.stdout
            line = sbatch.stdout.read().decode().strip()
            return line.split("|")[0]
    except TypeError as msg:
        raise TypeError(f"Bad slurm submit: {msg}") from msg


def inspect(config_file):
    project = RailProject.load_config(config_file)
    printable_config = pprint.pformat(project.config, compact=True)
    print(f"RAIL Project: {project}")
    print(">>>>>>>>")
    print(printable_config)
    print("<<<<<<<<")
    return 0


def truth_to_observed_pipeline(
    project,
    selection,
    flavor,
    run_mode=RunMode.bash,
):
    pipeline_name = "truth_to_observed"
    pipeline_info = project.get_pipeline(pipeline_name)
    pipeline_path = project.get_path('pipeline_path', pipeline=pipeline_name, flavor=flavor)

    input_catalog_name = pipeline_info['InputCatalogTag']
    input_catalog = project.get_catalogs().get(input_catalog_name)

    # Loop through all possible combinations of the iteration variables that are
    # relevant to this pipeline
    if (iteration_vars := input_catalog.get("IterationVars")) is not None:
        iterations = itertools.product(
            *[
                project.config.get("IterationVars").get(iteration_var)
                for iteration_var in iteration_vars
            ]
        )
        for iteration_args in iterations:
            iteration_kwargs = {
                iteration_vars[i]: iteration_args[i]
                for i in range(len(iteration_vars))
            }

            source_catalog = project.get_catalog('reduced', selection=selection, **iteration_kwargs)
            sink_catalog = project.get_catalog(
                'degraded',
                selection=selection,
                flavor=flavor,
                **iteration_kwargs,
            )
            sink_dir = os.path.dirname(sink_catalog)
            script_path = os.path.join(sink_dir, f"submit_{pipeline_name}_{selection}_{flavor}.sh")

            ceci_command = project.generate_ceci_command(
                pipeline_path=pipeline_path,
                config=pipeline_path.replace('.yaml', '_config.yml'),
                inputs=dict(input=source_catalog),
                output_dir=sink_dir,
                log_dir=sink_dir,
            )

            if not os.path.isfile(source_catalog):
                raise ValueError(f"Input file {source_catalog} not found")
            try:
                handle_commands(
                    run_mode,
                    [
                        ["mkdir", "-p", f"{sink_dir}"],
                        ceci_command,
                        [
                            "tables-io",
                            "convert",
                            "--input",
                            f"{sink_dir}/output_dereddener_errors.pq",
                            "--output",
                            f"{sink_dir}/output.hdf5",
                        ]
                    ],
                    script_path,
                )
            except Exception as msg:
                print(msg)
                return 1
        return 0

    # FIXME need to get catalogs even if iteration not specified; this return fallback isn't ideal
    return 1


def spectroscopic_selection_pipeline(
    project,
    selection,
    flavor,
    run_mode=RunMode.bash,
):
    pipeline_name = "spec_selection"
    pipeline_info = project.get_pipeline(pipeline_name)
    pipeline_path = project.get_path('pipeline_path', pipeline=pipeline_name, flavor=flavor)

    input_catalog_name = pipeline_info['InputCatalogTag']
    input_catalog = project.get_catalogs().get(input_catalog_name)

    spec_selections = project.get_spec_selections()
    
    # Loop through all possible combinations of the iteration variables that are
    # relevant to this pipeline
    if (iteration_vars := input_catalog.get("IterationVars")) is not None:
        iterations = itertools.product(
            *[
                project.config.get("IterationVars").get(iteration_var)
                for iteration_var in iteration_vars
            ]
        )
        for iteration_args in iterations:
            iteration_kwargs = {
                iteration_vars[i]: iteration_args[i]
                for i in range(len(iteration_vars))
            }

            source_catalog = project.get_catalog(
                input_catalog_name,
                selection=selection,
                flavor=flavor,
                basename="output_dereddener_errors.pq",
                **iteration_kwargs,
            )
            sink_catalog = project.get_catalog(
                'degraded',
                selection=selection,
                flavor=flavor,
                **iteration_kwargs,
            )
            sink_dir = os.path.dirname(sink_catalog)
            script_path = os.path.join(sink_dir, f"submit_{pipeline_name}_{selection}_{flavor}.sh")

            ceci_command = project.generate_ceci_command(
                pipeline_path=pipeline_path,
                config=pipeline_path.replace('.yaml', '_config.yml'),
                inputs=dict(input=source_catalog),
                output_dir=sink_dir,
                log_dir=sink_dir,
            )

            convert_commands = []
            for spec_selection_ in spec_selections.keys():
                convert_command = [
                    "tables-io",
                    "convert",
                    "--input",
                    f"{sink_dir}/output_select_{spec_selection_}.pq",
                    "--output",
                    f"{sink_dir}/output_select_{spec_selection_}.hdf5",
                ]
                convert_commands.append(convert_command)
                
            if not os.path.isfile(source_catalog):
                raise ValueError(f"Input file {source_catalog} not found")
            try:
                handle_commands(
                    run_mode,
                    [
                        ["mkdir", "-p", f"{sink_dir}"],
                        ceci_command,
                        *convert_commands,
                    ],
                    script_path,
                )
            except Exception as msg:
                print(msg)
                return 1
        return 0

    # FIXME need to get catalogs even if iteration not specified; this return fallback isn't ideal
    return 1


def inform_pipeline(
    project,
    selection="gold",
    flavor="baseline",
    run_mode=RunMode.bash,
):

    pipeline_name = "inform"
    pipeline_info = project.get_pipeline(pipeline_name)
    pipeline_path = project.get_path('pipeline_path', pipeline=pipeline_name, flavor=flavor)
    pipeline_config = pipeline_path.replace('.yaml', '_config.yml')
    sink_dir = project.get_path('ceci_output_dir', selection=selection, flavor=flavor)
    script_path = os.path.join(sink_dir, f"submit_{pipeline_name}.sh")

    input_files = {}
    input_file_tags = pipeline_info['InputFileTags']
    for key, val in input_file_tags.items():
        input_file_flavor = val.get('flavor', 'baseline')
        input_files[key] = project.get_file_for_flavor(input_file_flavor, val['tag'], selection=selection)

    command_line = project.generate_ceci_command(
        pipeline_path=pipeline_path,
        config=pipeline_config,
        inputs=input_files,
        output_dir=sink_dir,
        log_dir=f"{sink_dir}/logs",
    )

    try:
        handle_commands(run_mode, [command_line], script_path)
    except Exception as msg:
        print(msg)
        return 1
    return 0


def estimate_single(
    project,
    selection="gold",
    flavor="baseline",
    run_mode=RunMode.bash,
):

    pipeline_name = "estimate"
    pipeline_info = project.get_pipeline(pipeline_name)
    pipeline_path = project.get_path('pipeline_path', pipeline=pipeline_name, flavor=flavor)
    pipeline_config = pipeline_path.replace('.yaml', '_config.yml')
    sink_dir = project.get_path('ceci_output_dir', selection=selection, flavor=flavor)
    script_path = os.path.join(sink_dir, f"submit_{pipeline_name}.sh")

    input_files = {}
    input_file_tags = pipeline_info['InputFileTags']
    for key, val in input_file_tags.items():
        input_file_flavor = val.get('flavor', 'baseline')
        input_files[key] = project.get_file_for_flavor(input_file_flavor, val['tag'], selection=selection)

    pz_algorithms = project.get_pzalgorithms()
    for pz_algo_ in pz_algorithms.keys():
        input_files[f"model_{pz_algo_}"] = os.path.join(sink_dir, f'inform_model_{pz_algo_}.pkl')

    command_line = project.generate_ceci_command(
        pipeline_path=pipeline_path,
        config=pipeline_config,
        inputs=input_files,
        output_dir=sink_dir,
        log_dir=f"{sink_dir}/logs",
    )

    try:
        handle_commands(run_mode, [command_line], script_path)
    except Exception as msg:
        print(msg)
        return 1
    return 0


def evaluate_single(
    project,
    selection="gold",
    flavor="baseline",
    run_mode=RunMode.bash,
):
    pipeline_name = "evaluate"
    pipeline_info = project.get_pipeline(pipeline_name)
    pipeline_path = project.get_path('pipeline_path', pipeline=pipeline_name, flavor=flavor)
    pipeline_config = pipeline_path.replace('.yaml', '_config.yml')
    sink_dir = project.get_path('ceci_output_dir', selection=selection, flavor=flavor)
    script_path = os.path.join(sink_dir, f"submit_{pipeline_name}.sh")

    input_files = {}
    input_file_tags = pipeline_info['InputFileTags']
    for key, val in input_file_tags.items():
        input_file_flavor = val.get('flavor', 'baseline')
        input_files[key] = project.get_file_for_flavor(input_file_flavor, val['tag'], selection=selection)

    pdfs_dir = sink_dir
    pz_algorithms = project.get_pzalgorithms()
    for pz_algo_ in pz_algorithms.keys():
        input_files[f"input_evaluate_{pz_algo_}"] = os.path.join(pdfs_dir, f'estimate_output_{pz_algo_}.hdf5')


    command_line = project.generate_ceci_command(
        pipeline_path=pipeline_path,
        config=pipeline_config,
        inputs=input_files,
        output_dir=sink_dir,
        log_dir=f"{sink_dir}/logs",
    )
    try:
        handle_commands(run_mode, [command_line], script_path)
    except Exception as msg:
        print(msg)
        return 1
    return 0


def pz_single(
    project,
    selection="gold",
    flavor="baseline",
    run_mode=RunMode.bash,
):
    pipeline_name = "pz"
    pipeline_info = project.get_pipeline(pipeline_name)
    pipeline_path = project.get_path('pipeline_path', pipeline=pipeline_name, flavor=flavor)
    pipeline_config = pipeline_path.replace('.yaml', '_config.yml')
    sink_dir = project.get_path('ceci_output_dir', selection=selection, flavor=flavor)
    script_path = os.path.join(sink_dir, f"submit_{pipeline_name}.sh")

    input_files = {}
    input_file_tags = pipeline_info['InputFileTags']
    for key, val in input_file_tags.items():
        input_file_flavor = val.get('flavor', flavor)
        input_files[key] = project.get_file_for_flavor(input_file_flavor, val['tag'], selection=selection)

    command_line = project.generate_ceci_command(
        pipeline_path=pipeline_path,
        config=pipeline_config,
        inputs=input_files,
        output_dir=sink_dir,
        log_dir=f"{sink_dir}/logs",
    )
    try:
        handle_commands(run_mode, [command_line], script_path)
    except Exception as msg:
        print(msg)
        return 1
    return 0


def tomography_single(
    project,
    selection="gold",
    flavor="baseline",
    run_mode=RunMode.bash,
):
    pipeline_name = "tomography"
    pipeline_info = project.get_pipeline(pipeline_name)
    pipeline_path = project.get_path('pipeline_path', pipeline=pipeline_name, flavor=flavor)
    pipeline_config = pipeline_path.replace('.yaml', '_config.yml')
    sink_dir = project.get_path('ceci_output_dir', selection=selection, flavor=flavor)
    script_path = os.path.join(sink_dir, f"submit_{pipeline_name}.sh")

    input_files = {}
    input_file_tags = pipeline_info['InputFileTags']
    for key, val in input_file_tags.items():
        input_file_flavor = val.get('flavor', flavor)
        input_files[key] = project.get_file_for_flavor(input_file_flavor, val['tag'], selection=selection)

    pdfs_dir = sink_dir
    pz_algorithms = project.get_pzalgorithms()
    for pz_algo_ in pz_algorithms.keys():
        input_files[f"input_{pz_algo_}"] = os.path.join(pdfs_dir, f'output_estimate_{pz_algo_}.hdf5')

    command_line = project.generate_ceci_command(
        pipeline_path=pipeline_path,
        config=pipeline_config,
        inputs=input_files,
        output_dir=sink_dir,
        log_dir=f"{sink_dir}/logs",
    )
    try:
        handle_commands(run_mode, [command_line], script_path)
    except Exception as msg:
        print(msg)
        return 1
    return 0


def sompz_single(
    project,
    selection="gold",
    flavor="baseline",
    run_mode=RunMode.bash,
):
    pipeline_name = "som_pz"
    pipeline_info = project.get_pipeline(pipeline_name)
    pipeline_path = project.get_path('pipeline_path', pipeline=pipeline_name, flavor=flavor)
    pipeline_config = pipeline_path.replace('.yaml', '_config.yml')
    sink_dir = project.get_path('ceci_output_dir', selection=selection, flavor=flavor)
    script_path = os.path.join(sink_dir, f"submit_{pipeline_name}.sh")

    input_file_dict = {}
    input_file_tags = pipeline_info['InputFileTags']
    for key, val in input_file_tags.items():
        input_file_flavor = val.get('flavor', flavor)
        input_file_dict[key] = project.get_file_for_flavor(input_file_flavor, val['tag'], selection=selection)

    input_files = dict(
        train_deep_data = input_file_dict['input_train'],
        train_wide_data = input_file_dict['input_train'],
        test_spec_data = input_file_dict['input_test'],
        test_balrog_data = input_file_dict['input_test'],
        test_wide_data = input_file_dict['input_test'],
        truth = input_file_dict['input_test'],
    )
        
    pdfs_dir = sink_dir

    command_line = project.generate_ceci_command(
        pipeline_path=pipeline_path,
        config=pipeline_config,
        inputs=input_files,
        output_dir=sink_dir,
        log_dir=f"{sink_dir}/logs",
    )
    try:
        handle_commands(run_mode, [command_line], script_path)
    except Exception as msg:
        print(msg)
        return 1
    return 0



def subsample_data(
    project,
    source_tag="degraded",
    selection="gold",
    flavor="baseline",
    label="train_file",
    run_mode=RunMode.bash,
):

    hdf5_output = project.get_file_for_flavor(flavor, label, selection=selection)
    output = hdf5_output.replace('.hdf5', '.parquet')
    output_metadata = project.get_file_metadata_for_flavor(flavor, label)
    basename = output_metadata['SourceFileBasename']
    output_dir = os.path.dirname(output)
    size = output_metadata.get("NumObjects")
    seed = output_metadata.get("Seed")
    catalog_metadata = project.get_catalogs()['degraded']
    iteration_vars = catalog_metadata['IterationVars']

    iterations = itertools.product(
        *[
            project.config.get("IterationVars").get(iteration_var)
            for iteration_var in iteration_vars
        ]
    )
    sources = []
    for iteration_args in iterations:
        iteration_kwargs = {
            iteration_vars[i]: iteration_args[i]
            for i in range(len(iteration_vars))
        }

        source_catalog = project.get_catalog(
            source_tag,
            selection=selection,
            flavor=flavor,
            basename=basename,
            **iteration_kwargs,
        )
        sources.append(source_catalog)

    if run_mode == RunMode.slurm:
        raise NotImplementedError("subsample_data not set up to run under slurm")

    dataset = ds.dataset(sources)
    num_rows = dataset.count_rows()
    print("num rows", num_rows)
    rng = np.random.default_rng(seed)
    print("sampling", size)

    size = min(size, num_rows)    
    indices = rng.choice(num_rows, size=size, replace=False)
    subset = dataset.take(indices)
    print("writing", output)

    if run_mode == RunMode.bash:
        os.makedirs(output_dir, exist_ok=True)
        pq.write_table(
            subset,
            output,
        )
    print("done")
    handle_command(run_mode, ["tables-io", "convert", "--input", f"{output}", "--output", f"{hdf5_output}"])
    return 0



def build_pipelines(project, flavor='baseline'):

    output_dir = project.get_common_path('project_scratch_dir')
    flavor_dict = project.get_flavor(flavor)
    pipelines_to_build = flavor_dict['Pipelines']
    pipeline_overrides = flavor_dict.get('PipelineOverrides', {})
    do_all = 'all' in pipelines_to_build

    for pipeline_name, pipeline_info in project.get_pipelines().items():
        if not (do_all or pipeline_name in pipelines_to_build):
            print(f"Skipping pipeline {pipeline_name} from flavor {flavor}")
            continue
        output_yaml = project.get_path('pipeline_path', pipeline=pipeline_name, flavor=flavor)
        if os.path.exists(output_yaml):
            print(f"Skipping existing pipeline {output_yaml}")
            continue

        pipe_out_dir = os.path.dirname(output_yaml)

        try:
            os.makedirs(pipe_out_dir)
        except:
            pass

        overrides = pipeline_overrides.get('default', {})
        overrides.update(**pipeline_overrides.get(pipeline_name, {}))

        pipeline_kwargs = pipeline_info.get('kwargs', {})
        for key, val in pipeline_kwargs.items():
            if val == 'SpecSelections':
                pipeline_kwargs[key] = project.get_spec_selections()
            elif val == 'PZAlgorithms':
                pipeline_kwargs[key] = project.get_pzalgorithms()
            elif val == 'NZAlgorithms':
                pipeline_kwargs[key] = project.get_nzalgorithms()
            elif val == 'Classifiers':
                pipeline_kwargs[key] = project.get_classifiers()
            elif val == 'Summarizers':
                pipeline_kwargs[key] = project.get_summarizers()
                
        if overrides:
            pipe_ctor_kwargs = overrides.pop('kwargs', {})
            pz_algorithms = pipe_ctor_kwargs.pop('PZAlgorithms', None)
            if pz_algorithms:
                orig_pz_algorithms = project.get_pzalgorithms().copy()
                pipe_ctor_kwargs['algorithms'] = {
                    pz_algo_: orig_pz_algorithms[pz_algo_] for pz_algo_ in pz_algorithms
                }            
            pipeline_kwargs.update(**pipe_ctor_kwargs)
            stages_config = os.path.join(pipe_out_dir, f"{pipeline_name}_{flavor}_overrides.yml")
            with open(stages_config, 'w') as fout:
                yaml.dump(overrides, fout)
        else:
            stages_config = None

        pipeline_class = pipeline_info['PipelineClass']
        catalog_tag = pipeline_info['CatalogTag']

        if catalog_tag:
            catalog_utils.apply_defaults(catalog_tag)

        tokens = pipeline_class.split('.')
        module = '.'.join(tokens[:-1])
        class_name = tokens[-1]
        log_dir = f"{output_dir}/logs/{pipeline_name}"

        __import__(module)
        RailPipeline.build_and_write(
            class_name,
            output_yaml,
            None,
            stages_config,
            output_dir,
            log_dir,
            **pipeline_kwargs,
        )

    return 0
