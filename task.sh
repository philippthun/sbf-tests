#!/bin/bash

find $SERVICE_BINDING_ROOT -type f -exec bash -c "echo {}: \$(cat {})" \;
