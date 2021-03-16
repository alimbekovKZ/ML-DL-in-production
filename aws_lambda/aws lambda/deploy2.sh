#!/bin/bash
mkdir -p packages
cp -r ./venv/lib64/python3.7/site-packages/* packages
cd packages
find . -type d -name "tests" -exec rm -rf {} +
find . -type d -name "__pycache__" -exec rm -rf {} +
rm -rf ./{caffe2,wheel,wheel-*,pkg_resources,boto*,aws*,pip,pip-*,pipenv,setuptools}
rm -rf ./{*.egg-info,*.dist-info}
find . -name \*.pyc -delete
#zip up torch
zip -r9 torch.zip torch
rm -r torch
# zip everything up
zip -r9 ${OLDPWD}/pytorch_fn.zip .
cd $OLDPWD;
cd ./code
zip -rg ${OLDPWD}/pytorch_fn.zip .
cd $OLDPWD
rm -r packages
# copy to s3 and update lambda function
aws s3 cp pytorch_fn.zip s3://lambda-functions/
aws lambda update-function-code --function-name pytorch_example \   --s3-bucket lambda-functions --s3-key pytorch_fn.zip
