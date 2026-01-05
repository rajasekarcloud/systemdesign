#!/bin/bash

IP="http://<PUBLIC_IP_EC2_INSTANCE>:5000/shorten_url"

for url in \
    "https://www.educative.io/cloudlabs/working-with-instances-an-amazon-ec2-walkthrough" \
    "https://www.educative.io/cloudlabs/monitoring-ec2-instances-using-aws-cloudwatch" \
    "https://www.educative.io/cloudlabs/understanding-auto-scaling-group-asg-in-aws" \
    "https://www.educative.io/cloudlabs/build-an-educative-chatbot-with-conversational-ai-using-aws-lex"
do
    echo "Shortening: $url"
    curl -X POST "$IP" \
        -H "Content-Type: application/json" \
        -d "{\"long_url\":\"${url}\"}"
    echo -e "\n"
done
