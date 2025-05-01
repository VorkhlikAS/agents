import logging
from smolagents import Tool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LastMonthTool(Tool):
    name = "LastMonthTool"
    description = "This is a tool that returns the last month values for the metrics."
    inputs = {}
    output_type = "string"

    def __init__(self, last_month: dict) -> None:
        super().__init__()
        if last_month:
            self.values_str = ', '.join([f"last_{key}: {val}" for key, val in last_month.items()])
        else:
            self.values_str = None

    def forward(self) -> str:
        """
        Get the last month values for the metrics.
        """
        if self.values_str:
            logger.info("Forward function output (LastMonthTool): %s", self.values_str)  # Log the output
            return (
                "Here are the last month values for the metrics, this might help you mark the current metrics correctly:\n" +
                self.values_str
            )
        else:
            default_values = (
                "There were no values in last month."
            )
            logger.info("Forward function default output (LastMonthTool): %s", default_values)  # Log the default output
            return default_values
