from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

GROUND_TRUTH = {
    "company_homepage": "https://materialize.com",
    "ceo_name": "Nate Stewart",
    "cto_name": None,
    "year_founded": 2019,
    "funding_status": "series_c",
    "office_locations": ["New York City"],
    "employee_headcount": "51-200",
    "total_funding_raised": 98.5,
}

DATASET_NAME = "context-clash-materialize"


def create_dataset() -> None:
    client = Client()

    if client.has_dataset(dataset_name=DATASET_NAME):
        print(f"Dataset already exists: {DATASET_NAME}")
        return

    dataset = client.create_dataset(
        dataset_name=DATASET_NAME,
        description="Single-company context clash evaluation (Materialize)",
    )
    client.create_example(
        inputs={
            "messages": [
                {"role": "user", "content": "Research the company Materialize."}
            ]
        },
        outputs={k: v for k, v in GROUND_TRUTH.items() if k != "company_homepage" and v is not None},
        dataset_id=dataset.id,
    )
    print(f"Created dataset: {DATASET_NAME}")


if __name__ == "__main__":
    create_dataset()
