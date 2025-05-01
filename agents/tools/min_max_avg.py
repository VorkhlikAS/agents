import logging
from smolagents import Tool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MinMaxAvgTool(Tool):
    name = "MinMaxAvgTool"
    description = "This is a tool that returns the min, max, and average values for the metrics."
    inputs = {}
    output_type = "string"

    def __init__(self, min_values: dict, avg_values: dict, max_values: dict) -> None:
        super().__init__()
        self.values = {}
        if min_values and avg_values and max_values:
            self.values_str = (
                ', '.join([f"min_{key}: {val}" for key, val in min_values.items()]) + '\n' + 
                ', '.join([f"avg_{key}: {val}" for key, val in avg_values.items()]) + '\n' +  
                ', '.join([f"max_{key}: {val}" for key, val in max_values.items()])
            )
        else:
            self.values_str = None

    def forward(self) -> str:
        """
        Get the min, max, and average values for the metrics.
        """
        if self.values_str:
            logger.info("Forward function output: %s", self.values_str)  # Log the output
            return (
                "Here are the min, max, and average values for the metrics, this might help you mark the current metrics correctly:\n" 
                + self.values_str
            )
        else:
            default_values = (
                "There were no values for the metrics."
            )
            logger.info("Forward function default output: %s", default_values)  # Log the default output
            return default_values
