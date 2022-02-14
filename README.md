# HelpPC Reference Library HTML Version

This project contains Quick Reference Material used to program IBM PC and compatible computers back in the late 80's and early 90's. The information found here is distilled knowledge of many thousands of pages of Programmer reference material. 

It also contains a utility program written in C to convert the information found in the TXT files to an HTML site. 

The original program that used this data is available online on various retro software repositories. The TXT files availabe here can be updated and fed back into the program.

The format of the TXT file is documented below

```
Creating your own Help Files
	============================
  Each file musth have its own title which will show up in the 
  main menu.  Each topic following the file title (see below) will 
  show up in the subtopic	menu.  Note that HelpPC will adjust the 
  menu format based on the screen height and the number of items 
  in the main menu.

	HelpPC text files are simple ASCII files that contain control codes
	in column one.   Each file must contain a menu title in the first
	line.  The remainder of the file consists of keyed lines and help
	text.  Each line must end with a CR/LF pair (standard DOS format) and
	shouldn't be longer than 79 characters.   Tabs position the text at
	8 character tab positions.  The following is a list of keys and
	special characters (keys are found in column 1, special characters
	appear in columns 1-80):

	 '@'  in column 1 indicates a file title which will appear in
	      the main topic menu.  This must be the very first line
	      in the file and has a maximum length of 40 characters
	      (excluding the '@').
	 ':'  in column 1 indicates a subtopic key.  Multiple keys separated
	      by colons ':' can be entered on the same line.  Single spaces
	      are allowed in a key, multiple spaces are compressed to single.
 
	 '%'  in column 1 indicates a highlighted title line.
	 '^'  in column 1 indicates a centered highlighted title.
	 ' '  (space) in column 1 indicates normal text.
	 '~'  Tilde is used to mark text as a subtopic link.  Use two
	      tilde characters to represent an actual tilde in the data.
	      A word or phrase enclosed between tilde's will become a
	      subtopic link for the current topic.
	 TAB  in column 1 starts text in column 9
	 any other character in column 1 is truncated

	Use the BUILD command to index/reindex the default help text files.
	To add your own files to the index use the command:

	     BUILD [fname [file2 ...]]

	This information is available in HelpPC with the topic
	"HELPPC FORMAT".

	Limits of the HelpPC program
	============================

	Max items in main topic menu:          16
	Max items in subtopic menu:           512
	Max topics in index:                 1800
	Max size of topic text:             16384 bytes
	Max lines of text per topic:          512 lines
	Max topic key length:                  20 bytes
	Max file title length:                 40 bytes
	No limit on file size


        The following list contains information on reference materials
	used to verify and supply the information found in HelpPC.

	 1. Powell, David.  "IBM PC-DOS Programmer's Quick Reference
	    Summary".  (Unpublished paper.)

	 2. Powell, David.  "IBM BIOS Programmer's Quick Reference
	    Summary".  (Unpublished paper.)
	 
	 3. Norton, Peter.  "Programmer's Guide to the IBM PC".
	    Redmond, Washington: Microsoft Press, 1985.

	 4. Duncan, Ray.  "Advanced MS-DOS".
	    Redmond, Washington: Microsoft Press, 1986.

	 5. IBM Corporation.  "Disk Operating System Version 3.10: Technical
	    Reference". Boca Raton, Florida: International Business Machines
	    Corporation, 1986.

	 6. Davies, Russ.  "COMPUTE!'s Mapping the IBM PC and PCjr".
	    Greensboro, North Carolina: COMPUTE! Publications, Inc., 1986.

	 7. Brenner, Robert C.	"IBM PC Troubleshooting & Repair Guide".
	     Indianapolis, Indiana: Howard W Sams & Company, 1985.

	 8. Borland International, Inc.  "Turbo C Reference Guide".  Scotts
	    Valley, California: Borland International, Inc., 1987.

	 9. Scanlon, Leo J.  "8086/88 Assembly Language Programming".
	    Bowie, Maryland: Robert J. Brady Co., 1984.

	10. IBM Corporation. "Technical Reference: PC/XT".  Boca Raton,
	    Florida: International Business Machines Corporation, 1983.

	11. Wilton, Richard.  "Programmer's Guide to PC & PS/2 Video
	    Systems".  Redmond, Washington: Microsoft Press, 1987.

	12. Dettemann, Terry R.  "DOS Programmers Reference".
	    Carmel, Indiana: Que Corporation, 1988.

	13. Hogan, Thom.  "The Programmer's PC Sourcebook".
	    Redmond, Washington: Microsoft Press, 1988.

	14. Intel Corporation.	"Microprocessor and Peripheral Handbook".
	    2 vols.  Mountain View, California: Intel Corporation, 1989.

	15. Wyatt, Allen L. Sr.  "Assembly Language Quick Reference".
	    Carmel, Indiana: Que Corporation, 1989.

	16. IBM Corporation. "Technical Reference: PS/2 Model 30 Technical
	    Reference".  Boca Raton, Florida: International Business
	    Machines Corporation, 1987.

	17. IBM Corporation. "Technical Reference: PS/2 Model 50 and 60
	    Technical Reference".  Boca Raton, Florida: International
	    Business Machines Corporation, 1987.

	18. Norton, Peter, and Richard Wilton.	"Programmer's Guide to the
	    IBM PC & PS/2".  Redmond, Washington: Microsoft Press, 1988.

	19. Duncan, Ray, and Susan Lammers, eds. "The MS-DOS Encyclopedia".
	    Redmond, Washington: Microsoft Press, 1988.

	20. IBM Corporation. "Technical Reference: PCjr".  Boca Raton,
	    Florida: International Business Machines Corporation, 1983.

	21. IBM Corporation, "Technical Reference: PC/AT".  Boca Raton,
	    Florida: International Business Machines Corporation, 1984.

	22. Bailey, Sharon.  "Periscope Manual".  Atlanta, Georgia:
	    The Periscope Company, 1990.

	23. Microsoft Corporation.  "Microsoft Mouse Programmer's
	    Reference".  Redmond, Washington: Microsoft Press, 1989.

	24. Schemmer, Bernd.  Letter to author.  1 July 1990.

	25. Microsoft Corporation.  "Microsoft Macro Assembler 5.0,
	    Programmer's Guide".  Redmond, Washington: Microsoft
	    Corporation, 1987.

	26. Parke, William C.  "Data Structures Used in IBM PC Compatibles
	    and the PS/2".  (Unpublished paper).
	
	27. NEC Electronics, Inc.  "Intelligent Peripheral Devices (IPD)
	    Data Book".  Mountain View, California: NEC Electronics,
	    Inc., 1989.

	28. Seiko Epson Corporation. "Epson LX-800 User's Manual".  Nagano,
	    Japan: Seiko Epson Corporation, 1987.

	29. Hewlett-Packard Company. "Hewlett-Packard LaserJet Family
	    Technical Reference Manual".  Boise, Idaho: Hewlett-Packard
	    Company, 1986.

	30. "System BIOS for IBM PC/XT/AT Computers and Compatibles".
	    Phoenix Technical Reference Series.  Reading, Massachusetts:
	    Addison-Wesley, 1990.

	31. Schulman, Andrew.  "Undocumented DOS".
	    Reading, Massachusetts: Addison-Wesley, 1990.

```
