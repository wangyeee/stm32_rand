# STM32 Random Number Generator

This project turns [STM32F4-Discovery](https://www.st.com/en/evaluation-tools/stm32f4discovery.html) board, or any STM32F4 board with USB port into a hardware random number generator.

## Prerequisite
1. [GNU Arm Embedded Toolchain](https://developer.arm.com/open-source/gnu-toolchain/gnu-rm)
2. [STM32CubeMX](https://www.st.com/en/development-tools/stm32cubemx.html)
3. Firmware programming tool

## Compiling the Code
1. Clone this project, open `stm32_rand.ioc` with STM32CubeMX. The click `Generate Code` under `Project` menu to download and copy STM32F4 drivers and USB libraries to `Drivers/CMSIS`, `Drivers/STM32F4xx_HAL_Driver` and 
`Middlewares/ST/STM32_USB_Device_Library`.
2. Type `make` to build, or `make DEBUG=0 OPT=-O2` to build a release version.

## Programing and Running
1. Programme the binary to board. With the onboard ST-Link, varity of tools can be employed to programme the flash memory. Such as [ST-LINK utility](https://www.st.com/en/development-tools/stsw-link004.html) on Windows, or [stlink](https://github.com/texane/stlink) from texane which works on both Linux and macOS.
2. Connect the micro USB port to PC, a new serial port will be available.
3. Random numbers can be accessed by simply reading data from the new serial port. A python script `dump_rand.py` is provided as an example.
