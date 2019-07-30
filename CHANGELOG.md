# Changelog

Most recent releases are shown at the top.

## 2.1.11
- dirty hotfix for the (to be removed) legacy version, which wont include matplotlib because it is imported by the main module

## 2.1.10
- bug fix in gen_from_txt(explicit_none = False)

## 2.1.8
- added support for tabs in explicit table generation

## 2.1.7
- advanced formatting options

## 2.1.6
- saner wildcard imports
- linregression from scipy.stats as wildcard import

## 2.1.5
- adjustet the minimal matplotlib header, to simulate some features, which are only available in the LuaLaTeX backend

## 2.1.3 / 2.1.4
- use fast matplotlib settings as default
- set matplotlib backend before importing pyplot

## 2.1.2
- added the fast backend function

## 2.1.1

- added legacy code again
- Fixed matplotlib header bug
  
## 2.1.0

- Release on PyPi
- Improve README
- Make decimal separators work on all platforms

## 2.0.0

- Complete rehaul of code base, breaking changes
