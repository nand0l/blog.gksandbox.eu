import boto3
import os
import json

file_path = os.path.join(os.path.dirname(__file__), "response.json")

client = boto3.client("bedrock-runtime", region_name="us-east-1")

response = client.invoke_model(
    modelId="global.amazon.nova-2-lite-v1:0",
    contentType="application/json",
    accept="application/json",
    body=b'{"messages": [{"role": "user", "content": [{"text": "Explain quantum computing in simple terms."}]}], "inferenceConfig": {"max_new_tokens": 512}}'
)

print(f"Response keys: {list(response.keys())}")

with open(file_path, "w") as f:
    response_dict = {
        "ResponseMetadata": response["ResponseMetadata"],
        "contentType": response["contentType"],
        "body": json.loads(response["body"].read().decode("utf-8"))
    }
    json.dump(response_dict, f, indent=2)
    