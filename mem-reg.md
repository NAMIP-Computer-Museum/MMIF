# MMIF memory organisation and registers

## Registers

Fast access

* floating registers - 18 digits 
   * w (omega) can be considered as the accumulator, it is directly used by the calculating unit as input/output   
   * E,F internal registers with fast access time
   * b (beta) - internal of register of calculating unit, can keep information between a specific operation and be reused
* index register - 4 digits
   * G, H, I, J
   * also name Wi (i=1..4) in short the i bit being  part of the instruction scheme, see [instructions.md]
* other registers
   * ch - of boolean type, used for conditional jumps
   * M - can be considered as the program counter, actually point to the next address (+5 modulo 10000)
   * V, S: 4 digits, used for target address for tape operation (to be checked)
   * A, B: not registers but current tape value on tape A or B

## Drums

Slower access, acting as "RAM"

Two drums are available:
* can be configured either from program (i.e. pair of "orders") or data (i.e. floats)
* there are specific instruction to configure, done at start of program
* configuration possible at half drum level
* not totally sure how the function library is considered (need to check call process)

Drums are similar and are organised as follows:
* 100 tracks numbered from 0 to 99
* 20 sectors numbered from 0 to 95 by a step of 5
* addressing is <track><sector> e.g. 1215 means track 12, sector 15. 1211 is illegal
* addressing is thus coded on 4 digit and takes the second part of an instruction (see [instructions.md])
* an address store 1 Word which is composed of 18 digits, representing either 
   * one floating number: see [encoding.md]
   * two instructions, each coded composed of 9 digits: see [instructions.md]
* total memory per drum is: 2000 Words 
   * this represents 2000 x 9 = 19.000 "equivalent" bytes
   * assuming a bytes captures 2 decimal digits (binary encoding would be more effective)
* physical representation: see [encocoding.md]
* mean access time: 7 ms

## Tapes

Slow memory: about 30ms/word for next word (sequential)

Configuration
* there are 5 possible tapes units that can be mapped to 3 units
  * A and B for input
  * C for output
* a tape is composed of a main track and an auxiliary track

Main track
* sequence of address (4) + word (18), i.e. 22 digits
* for program: address is the target address where it should be store on the drum
* for data, address can be used for typographic info for later printing
* tape is organised in groups, groups are divided in segments
* valid address ends with 0 and 5, so other end digits can be used as markers:
  * +2 = end of tape (as the tape is a loop, it means also back to start)
  * +4 = end of group
  * +1 = end of segment
  * +3 = end of segment and group (last segment of a group)
* within a group (and a segment) all addresses must be unique
* transfer: 
  * from A,B to C, drum or printer
  * start reading NEXT word (not word at current position)
  * stop modality specified before
  * unrolling order is non-blocking, i.e. one can start tape and launch computation, unrolling will occur during compute

Auxiliary track: see later

## Printer

Speed: about 10 cps