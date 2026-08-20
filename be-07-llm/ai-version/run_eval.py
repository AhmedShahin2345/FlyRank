import json
from src.llm.schema import EnrichInput
from src.app import app
from fastapi.testclient import TestClient

client = TestClient(app)

def load_cases():
    with open("evals/cases.json", "r") as f:
        return json.load(f)

def run_eval():
    cases = load_cases()
    correct = 0
    total = len(cases)
    
    for case in cases:
        input_data = EnrichInput(
            title=case["title"],
            description=case["description"],
            price_gbp=case["price_gbp"]
        )
        
        response = client.post("/enrich", json=input_data.dict())
        result = response.json()
        
        if result["category"] == case["expected_category"]:
            correct += 1
            
    print(f"Score: {correct}/{total} ({correct/total*100:.2f}%)")

if __name__ == "__main__":
    run_eval()
