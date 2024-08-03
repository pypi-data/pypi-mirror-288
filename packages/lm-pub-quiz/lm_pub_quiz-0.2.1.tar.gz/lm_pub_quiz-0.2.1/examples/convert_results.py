import json

from lm_pub_quiz import DatasetResults

with open("../BEAR/bear_lite_indices.json") as f:
    indices = json.load(f)

bear_results = DatasetResults.from_path("examples/gpt2_raw_results")


bear_results.filter_subset(indices).reduced("sum", save_path="examples/gpt2_results")
