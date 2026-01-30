from ast import parse
from math import exp
from pdb import run
import re
from experiments.params import params
import argparse
import copy
from src.thing import run
import requests

NTFY_TOPIC = "CHANGEME"

def main():

    parser = argparse.ArgumentParser()
    # now define all params here
    parser.add_argument("--learning-rate", type=float, default=0.001, help="learning rate for optimizer")
    parser.add_argument("--batch-size", type=int, default=32, help="batch size for training")
    parser.add_argument("--num-layers", type=int, default=2, help="number of layers in the model")
    parser.add_argument("--required-thing", type=str, help="a required parameter for the experiment")
    
    # you can have more if possible, experiments do not need to include all if not mandatory
    parser.add_argument("--num-epochs", type=int, default=10, help="number of epochs to train")
    parser.add_argument("--num-nodes", type=int, default=128, help="number of nodes in network")

    # where to save things
    parser.add_argument("--out-dir", type=str, default="results/", help="output directory for results")

    # seed
    parser.add_argument("--seed", type=int, default=42, help="random seed for reproducibility")

    parser.add_argument(
        "--experiment",
        type=str,
        default=None,
        help="what experiment to run",
        choices=list(params.keys()) + ["all"], # all runs all
    )

    parser.add_argument("--verbose", action="store_true", help="enable verbose logging")

    parser.add_argument("--save-dir", type=str, default="results/", help="directory to save results")

    args = parser.parse_args()
    # print(args)

    if args.experiment is not None:
        args.seed = -1  # when running experiments, we always randomize seed
        # copy starting values
        starting_args = copy.deepcopy(args)

        if args.experiment == "all":
            experiment_list = list(params.keys())
        else:
            experiment_list = [args.experiment]
        
        for exp_name in experiment_list:
            for param_set in params[exp_name]:
                # reset args
                args = copy.deepcopy(starting_args)
                # set params from param_set
                for key, value in param_set.items():
                    if args.verbose:
                        print(f"{key} = {value}")
                    setattr(args, key, value)

                args.save_dir = f"results/{exp_name}/"
                run(args)
            requests.post(f"https://ntfy.sh/{NTFY_TOPIC}", data=f"Experiment {exp_name} concluded".encode(encoding='utf-8'))
    else:
        # test run with given arguments
        run(args)



if __name__ == "__main__":
    exit(main())
