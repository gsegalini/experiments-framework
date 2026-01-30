from tqdm.contrib.itertools import product

def param_product(param_dict):
    keys = param_dict.keys()
    values = param_dict.values()
    for instance in product(*values):
        yield dict(zip(keys, instance))

# define experiment parameters here
# each key is an argument to main.py, then list of all values to tests
example_params = param_product({
    "learning_rate": [0.01, 0.001, 0.0001],
    "batch_size": [16, 32, 64],
    "num_layers": [2, 3, 4],
    "required_thing": ["fixed_value"], # this will always be the same
})

example2_params = param_product({
    "required_thing": ["another_value", "this is mandatory!!"],
})

params = {
    "example-name": example_params,
    "example2-name": example2_params
}


if __name__== "__main__":
    import sys
    if len(sys.argv) > 1:
        experiment_name = sys.argv[1]
        param_set = params.get(experiment_name, None)
        if param_set is None:
            print(f"Experiment {experiment_name} not found.")
        else:
            # print all parameter combinations for the given experiment
            for param in param_set:
                print(param)
    else:
        for experiment, param_set in params.items():
            print(f"Experiment: {experiment}, #configs: {len(list(param_set))}")
    
