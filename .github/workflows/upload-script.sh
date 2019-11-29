#!/bin/bash
#
# Upload binary artifacts when a new release is made.
#
# Original source from:
# skx/github-action-publish-binaries


# Ensure that the GITHUB_TOKEN secret is included
if [[ -z "$GITHUB_TOKEN" ]]; then
  echo "Set the GITHUB_TOKEN env variable."
  exit 1
fi

# Ensure that there is a pattern specified.
if [[ -z "$1" ]]; then
    echo "Missing file (pattern) to upload."
    exit 1
fi



# Have we found any artifacts?
found=
for file in $*; do
    if [ -e "$file" ]; then
        found=1
    fi
done

#
# Abort if missing.
#
if [ -z "${found}" ]; then

    echo "*****************************************************************"
    echo " "
    echo " Artifacts are missing."
    echo " "
    echo "*****************************************************************"

    exit 1
fi

# Prepare the headers for our curl-command.
AUTH_HEADER="Authorization: token ${GITHUB_TOKEN}"

# Create the correct Upload URL.
RELEASE_ID=${GITHUB_REF#*/release/}
# $(jq --raw-output '.release.id' "$GITHUB_EVENT_PATH")

if [[ -z "$RELEASE_ID" ]]; then
  echo "Tag couldn't be generated."
  exit 1
fi

LAST_TAG_NAME=$(curl \
   -sSL \  
   -H "Accept: application/vnd.github.v3+json" \
   -H "${AUTH_HEADER}" \
   https://api.github.com/repos/${GITHUB_REPOSITORY}/tags | jq -r '.[0].name')

# For each matching file..
for file in $*; do

    echo "Processing file ${file}"

    if [ ! -e "$file" ]; then
        echo "***************************"
        echo " file not found - skipping."
        echo "***************************"
        continue
    fi

    if [ ! -s "$file" ]; then
        echo "**************************"
        echo " file is empty - skipping."
        echo "**************************"
        continue
    fi


    FILENAME=$(basename "${file}")

    UPLOAD_URL="https://uploads.github.com/repos/${GITHUB_REPOSITORY}/releases/${RELEASE_ID}/assets?name=${FILENAME}"
    echo "Upload URL is ${UPLOAD_URL}"

    # Generate a temporary file.
    tmp=$(mktemp)

    # Upload the artifact - capturing HTTP response-code in our output file.
    response=$(curl \
        -sSL \
        -XPOST \
        -H "${AUTH_HEADER}" \
        --upload-file "${file}" \
        --header "Content-Type:application/octet-stream" \
        --write-out "%{http_code}" \
        --output $tmp \
        "${UPLOAD_URL}")

    # If the curl-command returned a non-zero response we must abort
    if [ "$?" -ne 0 ]; then
        echo "**********************************"
        echo " curl command did not return zero."
        echo " Aborting"
        echo "**********************************"
        cat $tmp
        rm $tmp
        exit 1
    fi

    # If upload is not successful, we must abort
    if [ $response -ge 400 ]; then
        echo "***************************"
        echo " upload was not successful."
        echo " Aborting"
        echo " HTTP status is $response"
        echo "**********************************"
        cat $tmp
        rm $tmp
        exit 1
    fi

    # Show pretty output, since we already have jq
    cat $tmp | jq .
    rm $tmp

done
