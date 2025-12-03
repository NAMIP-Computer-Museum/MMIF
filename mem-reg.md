# MMIF memory organisation and registers

## Drums

Two drums are available:
* one for program and one for data (hence Harvard style) 
* there are specific instruction to configure
* not totally sure how the function library is considered (need to check call process)

Drums are similar and are organised as follows:
* 100 tracks numbered from 0 to 99
* 20 sectors numbered from 0 to 95 by a step of 5
* addressing is <track><sector> e.g. 1215 means track 12, sector 15. 1211 is illegal
* addressing is thus coded on 4 digit and takes the second part of an instruction (see [instructions.md])
* an address store 1 Word which is composed of 18 digits, representing either 
   * one floating number: see [encoding.md]
   * two instructions, each coded composed of 9 digits: see [instructions.md]
* physical representation: see [encocoding.md]
* mean access time: 7 ms

Registers:
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