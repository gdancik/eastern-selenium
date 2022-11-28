# eastern-selenium
Automated browsing for common Eastern tasks using Python selenium

### Degree eval lookup

Look up a person's degree evaluation by their last name

```
degree_eval.py lastName [firstName] [--reset]
```

### Show my courses

Look up my courses or CSC courses on Eastern's schedule of classes

```
mycourses.py [--csc]
```

### Highlight final exam times

Highlight a specific final exam time on Eastern's final exam page

```
final_exam_lookup.py pattern
```
For example, calling `final_exam_lookup 'MWF 9-9:50'` will highlight 'MWF 9-9:50' on the page.  

