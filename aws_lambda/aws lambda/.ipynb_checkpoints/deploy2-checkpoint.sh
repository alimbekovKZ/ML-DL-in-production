#!/bin/bash
aws s3 cp pytorch_fn.zip s3://lambda-functions/
aws lambda update-function-code --function-name pytorch_example \   --s3-bucket lambda-functions --s3-key pytorch_fn.zip
