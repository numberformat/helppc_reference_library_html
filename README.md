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

```
