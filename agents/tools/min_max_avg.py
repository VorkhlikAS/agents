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
                ', '.join([f"{key}: {val}" for key, val in min_values.items()]) + '\n' + 
                ', '.join([f"{key}: {val}" for key, val in avg_values.items()]) + '\n' +  
                ', '.join([f"{key}: {val}" for key, val in max_values.items()])
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
                "Here are the min, max, and average values for the metrics, this might help you mark the current metrics correctly:\n" +
                "SLA: min: 0.5, avg: 0.7, max: 0.9; " +
                "VISIBILITY: min: 0.8, avg: 0.85, max: 0.9; " +
                "AVG_DURATION: min: 23, avg: 25, max: 30; " +
                "DENSITY_BY_COMPANY: min: 10, avg: 12, max: 15; " +
                "DENSITY_BY_OWNERBLOCK: min: 5, avg: 6, max: 8; " +
                "DENSITY_BY_APPLICATION: min: 6, avg: 7, max: 9"
            )
            logger.info("Forward function default output: %s", default_values)  # Log the default output
            return default_values
