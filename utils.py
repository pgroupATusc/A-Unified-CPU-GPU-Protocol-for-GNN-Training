import json

import torch
import torch.nn.functional as F


class Dict(dict):

    def __getattr__(self, key):
        return self.get(key)

    def __setattr__(self, key, value):
        self[key] = value

def merge_trace_files(input_files, output_file):
    merged_trace = []

    # Iterate over each input file
    for file in input_files:
        with open(file, 'r') as f:
            # Load JSON data from each file
            trace_data = json.load(f)
            # Extend the merged_trace list with the events from each file
            merged_trace.extend(trace_data["traceEvents"])

    # Create a dictionary for the merged trace data
    merged_data = {
        "traceEvents": merged_trace,
        # Copy other fields such as "metadata", "displayTimeUnit", etc., if present in the input files
    }

    # Write the merged trace to the output file
    with open(output_file, 'w') as f:
        json.dump(merged_data, f)


def loss_fn(y_hat, y):
    if y.dim() > 1:
        y_hat = torch.sigmoid(y_hat)
        loss = F.binary_cross_entropy(y_hat, y.to(torch.float))
    else:
        loss = F.cross_entropy(y_hat, y.to(torch.long))
    return loss


if __name__ == '__main__':
    # List of input trace files to merge
    input_files = [
        "product_three_layer_0.json",
        "product_three_layer_1.json",
        "product_three_layer_2.json",
        "product_three_layer_3.json"
    ]

    # Output file to store the merged trace
    output_file = "trace/combine.json"

    # Call the merge_trace_files function
    merge_trace_files(input_files, output_file)
