//
// MIT license
// Copyright (C) 2024 Intel Corporation
// SPDX-License-Identifier: MIT
//

//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//

#include "common.hpp"

int get_current_device_id() {
  return dpct::dev_mgr::instance().current_device_id();
}

void* ggml_sycl_host_malloc(size_t size) try {
  if (getenv("GGML_SYCL_NO_PINNED") != nullptr) {
    return nullptr;
  }

  void* ptr = nullptr;
  // allow to use dpct::get_in_order_queue() for host malloc
  dpct::err0 err = CHECK_TRY_ERROR(
      ptr = (void*)sycl::malloc_host(size, dpct::get_in_order_queue()));

  if (err != 0) {
    // clear the error
    fprintf(
        stderr,
        "WARNING: failed to allocate %.2f MB of pinned memory: %s\n",
        size / 1024.0 / 1024.0,
        "syclGetErrorString is not supported");
    return nullptr;
  }

  return ptr;
} catch (sycl::exception const& exc) {
  std::cerr << exc.what() << "Exception caught at file:" << __FILE__
            << ", line:" << __LINE__ << std::endl;
  std::exit(1);
}

void ggml_sycl_host_free(void* ptr) try {
  // allow to use dpct::get_in_order_queue() for host malloc
  SYCL_CHECK(CHECK_TRY_ERROR(sycl::free(ptr, dpct::get_in_order_queue())));
} catch (sycl::exception const& exc) {
  std::cerr << exc.what() << "Exception caught at file:" << __FILE__
            << ", line:" << __LINE__ << std::endl;
  std::exit(1);
}
