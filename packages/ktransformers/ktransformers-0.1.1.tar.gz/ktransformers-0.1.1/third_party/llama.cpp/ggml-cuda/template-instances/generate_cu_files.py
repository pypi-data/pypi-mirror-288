#!/usr/bin/env python3

from glob import glob
import os

TYPES_KV = ["GGML_TYPE_Q4_0", "GGML_TYPE_Q4_1", "GGML_TYPE_Q5_0", "GGML_TYPE_Q5_1", "GGML_TYPE_Q8_0", "GGML_TYPE_F16"]

SOURCE_FATTN_VEC = """// This file has been autogenerated by generate_cu_files.py, do not edit manually.

#include "../fattn-vec-f{vkq_size}.cuh"

DECL_FATTN_VEC_F{vkq_size}_CASE({head_size}, {type_k}, {type_v});
"""

SOURCE_FATTN_WMMA_START = """// This file has been autogenerated by generate_cu_files.py, do not edit manually.

#include "../fattn-wmma-f16.cuh"

"""

SOURCE_FATTN_WMMA_CASE = "DECL_FATTN_WMMA_F16_CASE({head_size}, {cols_per_block}, {kq_acc_t});\n"

TYPES_MMQ = [
    "GGML_TYPE_Q4_0", "GGML_TYPE_Q4_1", "GGML_TYPE_Q5_0", "GGML_TYPE_Q5_1", "GGML_TYPE_Q8_0",
    "GGML_TYPE_Q2_K", "GGML_TYPE_Q3_K", "GGML_TYPE_Q4_K", "GGML_TYPE_Q5_K", "GGML_TYPE_Q6_K"
]

SOURCE_MMQ = """// This file has been autogenerated by generate_cu_files.py, do not edit manually.

#include "../mmq.cuh"

DECL_MMQ_CASE({type});
"""


def get_short_name(long_quant_name):
    return long_quant_name.replace("GGML_TYPE_", "").lower()


def get_head_sizes(type_k, type_v):
    if type_k == "GGML_TYPE_F16" and type_v == "GGML_TYPE_F16":
        return [64, 128, 256]
    if type_k == "GGML_TYPE_F16":
        return [64, 128]
    return [128]


for filename in glob("*.cu"):
    os.remove(filename)

for vkq_size in [16, 32]:
    for type_k in TYPES_KV:
        for type_v in TYPES_KV:
            for head_size in get_head_sizes(type_k, type_v):
                with open(f"fattn-vec-f{vkq_size}-instance-hs{head_size}-{get_short_name(type_k)}-{get_short_name(type_v)}.cu", "w") as f:
                    f.write(SOURCE_FATTN_VEC.format(vkq_size=vkq_size, head_size=head_size, type_k=type_k, type_v=type_v))

for kq_acc_t in ["half", "float"]:
    for cols_per_block in [8, 16, 32]:
        if kq_acc_t == "float" and cols_per_block == 8:
            continue

        with open(f"fattn-wmma-f16-instance-kq{kq_acc_t}-cpb{cols_per_block}.cu", "w") as f:
            f.write(SOURCE_FATTN_WMMA_START)

            for head_size in [64, 80, 96, 112, 128, 256]:
                if cols_per_block == 8 and head_size % 32 != 0: # wmma fragment is 8x32
                    continue
                if kq_acc_t == "float" and cols_per_block == 32 and head_size == 256: # register spilling, bad performance
                    continue
                f.write(SOURCE_FATTN_WMMA_CASE.format(kq_acc_t=kq_acc_t, cols_per_block=cols_per_block, head_size=head_size))

for type in TYPES_MMQ:
    with open(f"mmq-instance-{get_short_name(type)}.cu", "w") as f:
        f.write(SOURCE_MMQ.format(type=type))
