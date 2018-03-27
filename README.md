# Elk-Utilities

I've been using Elk for almost a year now, and I think the format is better to understand compared to other DFT programs, but you do have to format them sometimes to get a good graph. I've had the most problems in the optics output files (task 120,121, etc.) and the PDOS format (task 20). Here are some of the utilities I've rewritten to aid in analyzing the data. 

## elk-pdos.py

It's quite diffuclt to do any analysis on the PDOS data using Gnuplot since the data blocks are separated by only 1 blank space. Gnuplot prefers to have double spaces in between data blocks and even supports a header for each data block. I think this is a useful feature so I went ahead and tried to set this up.

**Goal : Plot total PDOS each element, with ability to discern each bands and filenames** 

Usage : 

```
$ python elk-pdos.py PDOS_S01_A0001.OUT ... PDOS_S01_A000X.OUT
$ python elk-pdos.py PDOS_S01_A000*.OUT
$ python elk-pdos.py PDOS_S0*.OUT
```

Detailed instructions on usage is provided inside the routine. Many thanks for Markus Meinert for providing the blocks2columns.py. I used it as a base code to get what I want. The todos for this routine:
* Getting ELMIREP data into headers
* Streamlining with pdos-plotter.sh
* Support for other types of plotters (way in the long run)

## pdos-plotter.sh

This was my first attempt at trying to add up all the PDOS for each element. The main flaw was the fact that this code was designed only for non-spin polarized calculations. The 'pdos.py' file is also an edited version of the 'blocks2columns.py' file. The only difference is that the written files add up all of the components in the separated blocks. This is quite problematic for spin-polarized calculations as the negative spin down is cancelled out by the positive spin up.

This can still be used to gather all the current files, since the first few lines of the script is collecting the necessary filenames to combine. Then again, 'elk-pdos.py' is very flexible since you can combine the whole PDOS.OUT files or just some of them. 

This script has some nice awk, paste, and sed uses that may be useful to your work. They're scavanged from stack exchange and I've modified them to my needs.





# Elk-Utilities
