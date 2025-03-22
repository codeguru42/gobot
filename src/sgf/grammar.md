# SGF Grammar

## Syntax

"..." : terminal symbols
[...] : option: occurs at most once
{...} : repetition: any number of times, including zero
(...) : grouping
|   : exclusive or
italics: parameter explained at some other place

## EBNF Grammar

Collection = GameTree { GameTree }
GameTree   = "(" Sequence { GameTree } ")"
Sequence   = Node { Node }
Node       = ";" { Property }
Property   = PropIdent PropValue { PropValue }
PropIdent  = UcLetter { UcLetter }
PropValue  = "[" CValueType "]"
CValueType = (ValueType | Compose)
ValueType  = (None | Number | Real | Double | Color | SimpleText | Text | Point  | Move | Stone)

'list of':    PropValue { PropValue }
'elist of':   ((PropValue { PropValue }) | None)
              In other words elist is list or "[]".

## Tokens

UcLetter   = "A".."Z"
Digit      = "0".."9"
None       = ""

Number     = [("+"|"-")] Digit { Digit }
Real       = Number ["." Digit { Digit }]

Double     = ("1" | "2")
Color      = ("B" | "W")

SimpleText = { any character (handling see below) }
Text       = { any character (handling see below) }

Point      = game-specific
Move       = game-specific
Stone      = game-specific

Compose    = ValueType ":" ValueType
