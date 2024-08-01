# Write input data model with data validation

# NOTE: this is the data model example, please modify it as needed

# import pydantic library
from pydantic import BaseModel, Field
from typing import List, Optional


# Input for BasketAnalysis
class BasketAnalysisInput(BaseModel):
    data: List[List[str]] = Field(..., description="List of transactions where each transaction is a list of items")
    min_support: float = Field(0.1, description="Minimum support for frequent itemsets")
    min_confidence: float = Field(0.5, description="Minimum confidence for association rules")
    min_lift: float = Field(1.0, description="Minimum lift for association rules")
    min_length: int = Field(2, description="Minimum length of itemsets")
    max_length: int = Field(2, description="Maximum length of itemsets")
    max_rules: int = Field(10, description="Maximum number of rules to generate")
    itemset_type: Optional[str] = Field(None, description="Type of itemset to generate: frequent or association")


# Input for CollaborativeFiltering
class CollaborativeFilteringInput(BaseModel):
    data: List[List[str]] = Field(..., description="List of transactions where each transaction is a list of items")
    user_id: str = Field(..., description="User ID for whom recommendations are generated")


# Input for ContentBased
class ContentBasedInput(BaseModel):
    data: List[List[str]] = Field(..., description="List of transactions where each transaction is a list of items")
    item_id: str = Field(..., description="Item ID for which recommendations are generated")
    top_n: int = Field(10, description="Number of recommendations to generate")
    similarity_metric: Optional[str] = Field(None, description="Similarity metric to use for content-based filtering")
