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

Example:  
selecting  
![](https://user-images.githubusercontent.com/12431317/64166237-00077780-ce47-11e9-9fae-bfe18c592713.png)
![](https://user-images.githubusercontent.com/12431317/64166238-00077780-ce47-11e9-937d-3e9d0f678192.png)
![](https://user-images.githubusercontent.com/12431317/64166239-00077780-ce47-11e9-845d-a330f1b6b586.png)

[![WTFPL](http://www.wtfpl.net/wp-content/uploads/2012/12/wtfpl-badge-2.png)](http://www.wtfpl.net/)
