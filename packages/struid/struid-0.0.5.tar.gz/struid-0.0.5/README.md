Struid - "Stringy UUID"
By Dale Magee
BSD 3-clause License

# What is it?

The Struid is an extension of python's UUID class which is intended to be more "pythonic" than the builtin UUID.

In particular, the struid makes it easy to compare with a string or integer value, e.g:
```python
> a = Struid('deadbeef-d00f-d00f-d00f-c0ffeedecade')
> a == 'deadbeef-d00f-d00f-d00f-c0ffeedecade'
True
> a == 295990755078525382164994183696159263454
True
```

Struid also has convenience helpers to make it backwards-compatible with the regular uuid library:
```python
>from struid import UUID, uuid4
>uuid4().shortstr()
'💤🎝🐆🕏🍛🐃🐉🎧💿🎻🏐💊💡'
>UUID('💤🎝🐆🕏🍛🐃🐉🎧💿🎻🏐💊💡')
UUID('fe2fdb50-9280-461e-aa46-1b3e06718995')
```

# What else can it do?

Struids also have a new shortstr() method, which allows you to compactify your string representations of UUID values down using extended unicode characters (emojis, or any characters you choose)
 
e.g:
```python
> a = Struid('deadbeef-d00f-d00f-d00f-c0ffeedecade')
> a.shortstr()
'🌨🚩💵👤🚡ᚮ🕓💣🐙😝🕴🕤ᛦ'
```

And you can also instantiate a struid from a shortstr, or compare with one:
```python
> Struid('🌨🚩💵👤🚡ᚮ🕓💣🐙😝🕴🕤ᛦ')
Struid('deadbeef-d00f-d00f-d00f-c0ffeedecade')
```

You can change the available characters shortstr() can use by calling struid.set_digits(), e.g:
```python
> import struid
> struid.set_digits("0123456789AbCdEf")
> a=Struid('deadbeef-d00f-d00f-d00f-c0ffeedecade')
> a.shortstr()
'dEAdbEEfd00fd00fd00fC0ffEEdECAdE'
```
(note that changing the available characters affects the shortstr for all guids, 
 so if you e.g save shortstrings to a file and then change character sets, 
 the shortstrings in the file will no longer match)

# What else do I need to know?

Struids are built to be case-insensitive, i.e you must not include both upper and lowercase of the same character in the SHORTSTR_DIGITS, doing so will cause breakage.

