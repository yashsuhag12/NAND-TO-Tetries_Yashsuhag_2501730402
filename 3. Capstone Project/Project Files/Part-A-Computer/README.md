# Part A — Hack Computer

Place these HDL chips in a Nand2Tetris project directory alongside the official built-in chips and your Lab 1/Lab 2 chips.

- `CPU.hdl`: Hack CPU datapath, ALU control, destinations, memory write and jump logic.
- `Memory.hdl`: RAM16K, Screen and Keyboard memory map.
- `Computer.hdl`: ROM32K + CPU + Memory integration.

Run the official `CPU.tst`, `Memory.tst`, `ComputerAdd.tst`, `ComputerMax.tst`, and `ComputerRect.tst` in the Hardware Simulator. The project PDF asks for screenshots of each successful run. These screenshots must be captured from your local simulator; they are not fabricated here.

**Important integration note:** The CPU uses the Lab ALU and standard Nand2Tetris `Register`, `PC`, `Mux16`, `Not`, `And`, `Or` chips. Ensure your HDL simulator supports bus-part output connections such as `out[0..14]=addressM`.
