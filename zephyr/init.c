// SPDX-License-Identifier: BSD-3-Clause
/*
 * Copyright(c) 2020 Intel Corporation. All rights reserved.
 *
 * Author: Liam Girdwood <liam.r.girdwood@linux.intel.com>
 *         Keyon Jie <yang.jie@linux.intel.com>
 *         Rander Wang <rander.wang@intel.com>
 *         Janusz Jankowski <janusz.jankowski@linux.intel.com>
 */

#include <sof/lib/wait.h>
#include <sof/lib/pm_runtime.h>
#include <sof/lib/notifier.h>

#include <sof/trace/dma-trace.h>

#include <ipc/info.h>
#include <kernel/abi.h>

#include <device.h>
#include <init.h>

/* main firmware context */
static struct sof sof;

struct sof *sof_get(void)
{
	return &sof;
}

static int adsp_init(struct device *dev)
{
#if defined(CONFIG_SOF)
	struct sof *sof = sof_get();
	int err;

#if CONFIG_TRACE
	trace_point(TRACE_BOOT_SYS_TRACES);
	dma_trace_init_early(sof);
#endif

	trace_point(TRACE_BOOT_SYS_NOTIFIER);
	init_system_notify(sof);

	pm_runtime_init(sof);

	init_system_notify(sof);

	/* init the platform */
	err = platform_init(sof);
	if (err < 0)
		panic(SOF_IPC_PANIC_PLATFORM);

	trace_point(TRACE_BOOT_PLATFORM);

#if CONFIG_NO_SLAVE_CORE_ROM
	lp_sram_unpack();
#endif

#endif /* CONFIG_SOF */

	platform_boot_complete(0);

	return 0;
}

SYS_INIT(adsp_init, APPLICATION, CONFIG_KERNEL_INIT_PRIORITY_DEFAULT);