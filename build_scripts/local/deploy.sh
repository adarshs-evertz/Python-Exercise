#!/bin/bash -x
set -e
OUTPUT_DIR="./build_scripts/local/output_dir"
OPTS=`getopt -o p: --long profile: -n 'parse-options' -- "$@"`

if [ $? != 0 ] ; then echo "Failed parsing options." >&2 ; exit 1 ; fi

echo "$OPTS"
eval set -- "$OPTS"

PROFILE=''

while true; do
  case "$1" in
    -p | --profile ) PROFILE="$2"; shift; shift ;;
    -- ) shift; break ;;
    * ) break ;;
  esac
done

PROFILE_REGION=$(aws configure get region --profile $PROFILE)
REGION=${PROFILE_REGION:=us-east-1}

echo "Start deploying stack"
aws --profile $PROFILE cloudformation deploy --template-file $OUTPUT_DIR/template-export.yaml \
    --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_NAMED_IAM --stack-name python-exercise-$USER \
    --s3-bucket evertz-io-artifacts-bucket-$REGION --s3-prefix python-exercise-$USER/Artifacts/Templates \
    --parameter-overrides Project=python-exercise-$USER Owner=$USER@evertz.com Name=python-exercise-$USER \
      BasePath=python-exercise-$USER
echo "All done"
