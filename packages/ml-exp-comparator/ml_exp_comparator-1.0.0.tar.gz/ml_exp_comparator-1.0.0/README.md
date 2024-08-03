# ML experiments comparator

ML experiments comparator is an easy tool for comparing different ML experiments.

## Installation

TBU

## How to use

```
# 1. create or select ModelRunner for your experiments
# 2. load trained experimental models into model runners 

model_runner1, model_runner2 = get_model_runners(...)

# 3. create or select DatasetStore containing your dataset
dataset_store = get_dataset_store(...)

# 4. create or select MetricRunner for your dataset
metrics_runners = get_metrics_runners(...)

# 5. create or select ResultsAggregator for collecting metrics
results_aggregator = get_results_aggregator(...)

# 6. init ExperimentRunner
exp_runner = ExperimentsRunner(exp_name='exp_name', 
                               storage_folder='storage_folder', 
                               batch_size=100,
                               exp_models_runners=[model_runner1, model_runner2],
                               dataset_store=dataset_store,
                               metrics_runners=metrics_runners,
                               result_aggregator=results_aggregator)

# 7. run comparison and store the results 
exp_runner.run_and_store()
```
Examples: `examples/.`

## Modules

### Experiments runner 

`from ml_exp_comparator.experiments_runner import ExperimentsRunner`

Runs experimental models on the provided dataset using selected metrics.

### Dataset stores

`from ml_exp_comparator.dataset_stores.dataset_store import DatasetStore`

Dataset wrapper. Yields batches of a specific dataset.

### Metrics runners

`from ml_exp_comparator.metrics_runners.metric_runner import MetricRunner`

Calculates metrics for each output based on true and pred outputs. Aggregates calculated metrics.

### Models runners

`from ml_exp_comparator.models_runners.model_runner import ModelRunner`

Runs trained model on dataset true_input batches.

### Results aggregator

`from ml_exp_comparator.results_aggregators.results_aggregator import ResultsAggregator`

Collects single and aggregated metrics results. Dumps metric results into a local storage.


