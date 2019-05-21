
# SCALE ARM M0+ Board / lpc812m101

*Description of the SCALE ARM M0+ target*

---

This target is based off the [SCALE](https://github.com/dan-page/scale)
side-channel analysis boards.
Specifically, it targets the `lpc812m101` SoC from NXP, containing a
2 stage ARM Cortex M0+ CPU.

## Getting Started

To build and run an experiment on the target:

```sh
$> source bin/conf.sh
$> export UAS_ARM_TOOLCHAIN_ROOT=<path to 2016q3 ARM embedded toolchain>
$> make -B -f Makefile.experiment UAS_EXPERIMENT=example/addxor UAS_TARGET=scale_lpc812m101 program
```

If you're target device is not connected to `/dev/ttyUSB0`, you also need
to specify `USB_PORT=<port path>`.

---

**Useful links:**
- [NXP lpc81xM SoC Data Sheet](https://www.nxp.com/docs/en/data-sheet/LPC81XM.pdf)
- [ARM Cortex M0+ Technical reference](http://infocenter.arm.com/help/topic/com.arm.doc.ddi0484c/DDI0484C_cortex_m0p_r0p1_trm.pdf)
- [ARM v6-M Architecture Reference Manual](https://static.docs.arm.com/ddi0419/e/DDI0419E_armv6m_arm.pdf)
