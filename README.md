### Receipt Processor

This repo is the completed exercise of the following challenge: https://github.com/fetch-rewards/receipt-processor-challenge

In order to run this processor service, please follow the commands below:
```bash
# clone the repo
git clone git@github.com:amztc34283/fetch_rewards_take_home.git
# change directory
cd fetch_rewards_take_home
# build the docker image
docker build -t my-fastapi-app .
# run the image in a container
docker run -d -p 8000:8000 my-fastapi-app

# POST /receipts/process to store receipt
curl -X POST "http://localhost:8000/receipts/process" \
-H "Content-Type: application/json" \
-d '{
    "retailer": "M&M Corner Market",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
        {
            "shortDescription": "Mountain Dew 12PK",
            "price": "6.49"
        }
    ],
    "total": "6.49"
}'
# json with the id of the receipt should be returned

# GET /receipts/{id}/points to calculate points for the receipt with {id}
curl -X GET "http://localhost:8000/receipts/{id_you_get_from_previous_step}/points"
# json with calculated points following the rules below should be returned
```

Points Calculation Rules:
- One point for every alphanumeric character in the retailer name.
- 50 points if the total is a round dollar amount with no cents.
- 25 points if the total is a multiple of 0.25.
- 5 points for every two items on the receipt.
- If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
- 6 points if the day in the purchase date is odd.
- 10 points if the time of purchase is after 2:00pm and before 4:00pm.

Optionally, you could install the environment locally and run the tests if Python is installed:
```bash
pip install -r requirements.txt

cd test && pytest
```
Optionally, you could visit http://localhost:8000/docs to understand the schemas and parameters when calling the REST APIs.
