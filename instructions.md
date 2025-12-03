# MMIF instructions

## Global format : 5 decimal digits
* 1: operation type, transfert, computation, alteration,...
* 2: 
* 3: used as index for many operations, will involve index Wi, e.g in address translation
* 4+5: operation dependent, e.g. operation type for computations, alteration kind,...

## Alterations 
* prefix 000
* used to alter the NEXT value arriving in w register BEFORE operation is performed on it
* typically to extract mantissa, exponent, change sign, etc
* 12: +man
* 62:-man
* 22:+sgn
* 72:-sgn
* 32:+mod
* 82: -mod
* 42:+exp (ordre de grandeur)
* 92:-exp (ordre de grandeur)
* 13:noex (number ot exponent)
* 23:exno (exponent to number)

## Computation with register E and F as second operand
* prefix 020 (F) and 021 for (E)
* first operand is w and result in w
* if index digit 3 set to 1, 2, 3 or 4: Wi is added to AAAA
* digit 4 is for operation, digit 5 controls inversion
* 16: + 
* 26: -
* 66: +*
* 76: -* (i.e. not normalised)
* 36: x
* 35: x-
* 86: *  (use b register, set by previous x multiplication)
* 85: *- (use b register, set by previous x multiplication)

## Operation on immediate value as second operand  
* prefix 3
* interpret the 4 digit address as number for an arithmetic operation
* number is interpreted as 0.AAAA
* same semantics as above for E and F

## Operation from specified memory location as second operand
* prefix 40
* address is used to retrieve floating point used in operation
* same semantics as above for E and F

## Writing w to specified  address
* prefix 090
* next digit: 46 for writing and keeping value
* next digit: 96 for writing and resetting value (to check: O+ ?)

## Jumps, End, Alarms
* prefix 4
* 40000 immediate jump to address
* 41000 conditional jump to address depending on ch
* 42000 normal program end
* 47000 end with alarm
