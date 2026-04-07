import boto3
import json

client = boto3.client("bedrock-runtime", region_name="us-east-1")

# 1. The Request (Sending bytes)
response = client.invoke_model(
    modelId="global.amazon.nova-2-lite-v1:0",
    contentType="application/json",
    accept="application/json",
    body=b'{"messages": [{"role": "user", "content": [{"text": "Explain quantum computing in simple terms."}]}], "inferenceConfig": {"max_new_tokens": 512}}'
)

# 2. The Processing (Reading the stream)
response_body = response["body"].read().decode("utf-8")

# 3. The Parsing (Converting JSON string to Python dictionary)
data = json.loads(response_body)

# 4. The Extraction (Getting the specific answer text)
# Path: output -> message -> content -> first item -> text
answer = data["output"]["message"]["content"][0]["text"]

# 5. The Output
print("-" * 30)
print(answer)
print("-" * 30)