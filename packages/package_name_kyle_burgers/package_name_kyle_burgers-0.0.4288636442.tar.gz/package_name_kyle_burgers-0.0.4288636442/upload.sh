#!/usr/bin/env sh

rm -rf ./dist
python -m build
tar -czvf dist.tar.gz ./dist
aws s3api put-object --bucket devprod-infra-bite-testing --key dist.tar.gz --body dist.tar.gz