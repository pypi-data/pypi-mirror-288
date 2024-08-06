"""
    Proto
    =====

    Proto file definitions and auto-generated code

    Compile with:
    python3 -m grpc_tools.protoc \
        -I . \
        --python_out=. \
        --grpc_python_out=. \
        ./wirepas_positioning/proto/*.proto

    .. Copyright:
        Copyright 2019 Wirepas Ltd. All Rights Reserved.
        See file LICENSE.txt for full license details.
"""

from .nanopb_pb2 import *
from .nanopb_pb2_grpc import *
from .wpe_pb2 import *
from .wpe_pb2_grpc import *
