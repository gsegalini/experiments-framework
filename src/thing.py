import random
import os
import numpy as np
import time
# import torch
from src.utils import PerformanceManager

def run(args):
    # initialize performance manager
    filename = "results.csv"
    save_file = os.path.join(args.save_dir, filename)
    perf_manager = PerformanceManager(save_file)

    # set seed, but experiments should be random
    if args.seed < 0:
        # log starting seed
        seed = random.randint(0, 1 << 31)
        args.seed = seed
    random.seed(args.seed)
    np.random.seed(args.seed)
    # torch.manual_seed(args.seed)

    # for each epoch, do something
    for epoch in range(args.num_epochs):
        # log epoch
        perf_manager.log_metric("seed", args.seed)
        perf_manager.log_metric("epoch", epoch)
        # log params
        perf_manager.log_metric("learning_rate", args.learning_rate)
        perf_manager.log_metric("batch_size", args.batch_size)
        perf_manager.log_metric("num_layers", args.num_layers)
        perf_manager.log_metric("required_thing", args.required_thing)
        perf_manager.log_metric("num_epochs", args.num_epochs)

        start_time = time.time()

        # use logic somehow
        # placeholder for required_thing usage
        result = f"Running with required_thing: {args.required_thing}" * (epoch + 1)
        time.sleep(0.01) 
        elapsed_time = time.time() - start_time

        # log results
        perf_manager.log_metric("result_length", len(result))
        perf_manager.log_metric("runtime", elapsed_time)

        # when done, commit row
        perf_manager.commit_row(verbose=args.verbose)
    
    # at end, save performance
    perf_manager.save(append=True) # it can append to existing csv, or overwrite




