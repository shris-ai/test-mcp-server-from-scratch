import os
import logging
from . import trends
from mcp.types import Tool, TextContent
import pandas as pd
from enum import Enum

logger = logging.getLogger("mcp-trends")

class TrendTools(str, Enum):
    GET_INTEREST_BY_REGION = "get_interest_by_region"
    CONVERT_TIME = "convert_time"

class ToolHandler():
    def __init__(self, tool_name: str):
        self.name = tool_name

    def get_tool_description(self) -> Tool:
        raise NotImplementedError()
    
    def run_tool(self, args: dict) -> list[TextContent]:
        raise NotImplementedError
    
class CreateToolHandler_GetTrends_InterestByRegion(ToolHandler):
    def __init__(self):
        super().__init__(TrendTools.GET_INTEREST_BY_REGION.value)

    def get_tool_description(self):
        return Tool(
            name=self.name,
            description="Get Interest By Region for Keywords",
            inputSchema={
                "type": "object",
                "properties": {
                    "keywords":{
                        "type": "list",
                        "description": "List of keywords"
                    }
                },
                "required": ["keywords"]
            }
        )
    
    def run_tool(self, args: dict) -> pd.DataFrame:
        logger.info(f"Getting interest by region with args: {args}")

        if "keywords" not in args:
            logger.error("Required arguments are missing!")
            raise RuntimeError("Required - Keywords")
        try:
            api = trends.Trends()
            result = api.get_interest_by_region(args['keywords'])
            result = result.to_csv(index=False)
            
            logger.info("Successfully fetched results")
            logger.debug(f"API response: {result}")

            return result
        except Exception as e:
            logger.error(f"Failed to get interest by region: {str(e)}")
            raise

    