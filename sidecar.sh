#!/bin/bash

while true; do
  find $SERVICE_BINDING_ROOT -type f -exec bash -c "echo {}: \$(cat {})" \;
  sleep 60
done
