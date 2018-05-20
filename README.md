Abnum 3
=======

Alphabetic numerals package for Python 3. Module includes various letter value
substituting systems from the ancient times to the modern artificial ones.

Abnum substitution system is better known as _gematria_ in hebrew and
_isopsephy_ in greek, _abjad_ in arabic alphabet and _katapayadi_ in sanskrit.

Currently supported languages are:

- greek (grc)
- hebrew (heb)
- coptic (cop)
- aramaic (arm)
- syriaic (syc)
- arabic (ara)
- phoenician (phn)
- brahmi (brh)
- english (eng)
- finnish (fin)

## Install

`pip install abnum`

## Usage

Get the value of the greek phrase by adding letter values and returning the sum:

```python
    from abnum import Abnum, greek

    g = Abnum(greek)
    print(g.value('ο Λογος')) # 443
```

Use multiplication instead of addition:

```python
    from abnum import Abnum, greek
    from operator import mul
    g = Abnum(greek)
    # use an arithmetic function as the second argument and a start value as the third
    print(g.value('ο Λογος', mul, 1)) # 6174000000
```

Phoenician script:

```python
    from abnum import Abnum, phoenician
    p = Abnum(phoenician)
    a = list(map(g.value, "𐤀𐤍𐤊 𐤕𐤁𐤍𐤕 𐤊𐤄𐤍 𐤏𐤔𐤕𐤓𐤕 𐤌𐤋𐤊 𐤑𐤃𐤍𐤌 𐤁𐤍".split(" ")))
    print(a, sum(a))
```

```text
    [71, 852, 75, 1370, 90, 184, 52], 2694
```

## Jupyter notebooks

Please see Jupyter notebooks for further study and examples:

[Usage of the library](Abnum%203%20introduction.ipynb). Includes the verification of the isopsephical value of the Bergama stele, 100 - 200 AD.

[Isopsephical riddle of the Sibylline verses](Isopsephical%20riddle%20of%20the%20Pseudo%20Sibylline%20hexameter.ipynb), Book 1, lines 137 - 146.

Python 2 version of the Abnum library can still be found from: https://github.com/markomanninen/abnum
