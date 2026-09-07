from typing import List, Literal
from pydantic import BaseModel, Field, ValidationError

# 1. Define the schema
class CodeAnalysisReport(BaseModel):
    repo_name: str
    lines_of_code: int = Field(gt=0, description="Must be greater than 0")
    vulnerabilities: List[str]
    severity: Literal["LOW", "MEDIUM", "HIGH"]

def validate_payload(raw_data: dict):
    try:
        # Validate raw data against the Pydantic schema
        report = CodeAnalysisReport.model_validate(raw_data)
        print(" Valid Payload:")
        print(f"  Repo: {report.repo_name} | Severity: {report.severity}\n")
    except ValidationError as e:
        print(" Caught Expected Validation Error:")
        print(e)
        print("-" * 50)

if __name__ == "__main__":
    valid_data = {
        "repo_name": "agentic-insight-ai",
        "lines_of_code": 1250,
        "vulnerabilities": ["SQL Injection in legacy module"],
        "severity": "HIGH"
    }

    invalid_data = {
        "repo_name": "broken-repo",
        "lines_of_code": -10,  # Invalid: violating gt=0 constraint
        "vulnerabilities": [],
        "severity": "CRITICAL"  # Invalid: not in Literal["LOW", "MEDIUM", "HIGH"]
    }

    print("--- Testing Valid Payload ---")
    validate_payload(valid_data)

    print("--- Testing Invalid Payload ---")
    validate_payload(invalid_data)