# Write output data model with data validation

# NOTE: this is the data model example, please modify it as needed

# import pydantic library
from pydantic import BaseModel, Field
from typing import List, Optional


# Output for BasketAnalysis
class BasketAnalysisOutput(BaseModel):
    frequent_itemsets: List[List[str]] = Field(..., description="List of frequent itemsets")
    association_rules: List[dict] = Field(..., description="List of association rules")


# Output for CollaborativeFiltering
class CollaborativeFilteringOutput(BaseModel):
    recommendations: List[str] = Field(..., description="List of recommendations")


# Output for ContentBased
class ContentBasedOutput(BaseModel):
    recommendations: List[str] = Field(..., description="List of recommendations")
