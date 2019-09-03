# Scopus Query Compiler

Scopus is a database of scientific articles that provides an advanced search function.

When editing search queries, this package allows you to create a query referencing another query. That is, given the following queries:

```ruby
TITLE-ABS-KEY(neur* AND network*)
TITLE-ABS-KEY(recurrent)
```
You can create the query
```ruby
(TITLE-ABS-KEY(neur* AND network*)) AND (TITLE-ABS-KEY(recurrent))
```
by typing `#1 AND #2` and then using the "Scopus Compile: Compile Query" command in the command palette.

The number you type after `#` is simply the number of the line number of the targeted query.

You can theoretically nest as many query references as you want, as long as you have no circular or self-references. Self-references are detected and cause an exception, but circular references are as of yet unhandled.


![](https://raw.githubusercontent.com/Syncrossus/Garbage-File-Storage/master/scopus_compile_1.png?token=AC627VIV64UBBLM3YJFP7L25NYZD4)
![](https://raw.githubusercontent.com/Syncrossus/Garbage-File-Storage/master/scopus_compile_2.png?token=AC627VO3N7VG7KGN5BHLSFS5NYZGW)
![](https://raw.githubusercontent.com/Syncrossus/Garbage-File-Storage/master/scopus_compile_3.png?token=AC627VNQIVHK3YTDDUQZ76K5NYZIS)

