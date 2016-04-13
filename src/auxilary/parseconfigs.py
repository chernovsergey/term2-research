import yaml


def load_yaml(cfg_path):
    with open(cfg_path) as f:
        try:
            return yaml.load(f)
        except yaml.YAMLError as exc:
            raise exc


def load_data_config(parsed_dict):
    ref = parsed_dict['humangenome']

    condition1_replicates = [parsed_dict['condition_first']['replicate_first'],
                             parsed_dict['condition_first']['replicate_second']]

    condition1_inputs = [parsed_dict['condition_first']['input_replicate_first'],
                         parsed_dict['condition_first']['input_replicate_second']]

    condition2_replicates = [parsed_dict['condition_second']['replicate_first'],
                             parsed_dict['condition_second']['replicate_second']]

    condition2_inputs = [parsed_dict['condition_second']['input_replicate_first'],
                         parsed_dict['condition_second']['input_replicate_second']]

    return ref, condition1_replicates, condition1_inputs, condition2_replicates, condition2_inputs
