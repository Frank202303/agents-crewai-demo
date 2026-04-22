from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."

#    自定义 工具 
class SentimentAnalysisTool(BaseTool):
    name: str = "sentiment_analysis"   # 情感分析工具,name 必须是英语
    description: str = ("Analyze sentiment of text and ensure positive tone")  #  description 必须是英语
    
    # 伪代码： 做评分，如果不合格重新写
    def _run(self, text:str) -> str:
        return "positive"
