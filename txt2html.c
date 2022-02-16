/*
 * HelpPC Reference Library to HTML converter. Ver 1.02
 *
 * Copyleft (l) Stanislav Sokolov (stanisls@gmail.com)
 * The source is published under GNU General Public Licence
 * ver. 2 of June 1991.
 *
 * Visit on-line version on:
 * http://heim.ifi.uio.no/~stanisls/helppc/
 *
 * NOTE: If you want to make HTML version using UNIX, convert first
 * all TXT files so that they have UNIX-style new-line.
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <sys/stat.h>
#include <sys/types.h>

#define BASE_PATH "helppc"

struct conv{
  char *file;
  char *orig;
  struct conv *next;
};

struct conv *c_head;

void cleanLine(char *);
char *makeFile(char *);
void rmFirst(char *);
char *makeFName(char *);
void convError(char *);
void parseLine(char *);
int buildConv(int argc, char **argv);
void strlowr(char *x);
void freeTable(struct conv *);
void idxSortWrt(struct conv [], int, FILE*);
void _qsort(struct conv c_list[], int first, int last);

int main(int argc, char **argv){
  FILE *f = NULL, *fout = NULL;

  char line[1024];
  char *tmp, *fName;
  char foutname[100];
  int i;
  char first;
  int pending = 0, files;

  fprintf(stderr, "\nHelpPC Reference Library to HTML converter. Ver 1.02\n"
	  "Copyleft (l) Stanislav Sokolov\n\n");

  if(argc == 1){
    fprintf(stderr, "Usage:\n  %s [file.txt [file2.txt [...]]]\n"
	    "or\n  %s *.txt\n\n", argv[0], argv[0]);
    return 10;
  }

  mkdir(BASE_PATH, 0777);

  /* Build conversion table */
  fprintf(stderr, "Building conversion table and index files...\n");
  i = buildConv(argc, argv);
  fprintf(stderr, "Found %d keywords corresponding to %d unique entries.\n",
	  i >> 16, i & 0xFFFF);

  /* Parse the files */
  for(files = 1; files < argc; files++){  //For all files given to function
    if((f = fopen(argv[files], "r")) == NULL){
      fprintf(stderr, "Error opening %s\n", argv[files]);
      exit(100);
    }

    fprintf(stderr, "\nParsing %s...\n", argv[files]);

    while(fgets(line, 200, f) != NULL){
      cleanLine(line);
      line[strlen(line) - 1] = '\0';
      first = line[0];

      if(first == '@'){
	/* do nothing */
      } else if(first == ':'){ /*Make new html file*/
	if(pending){
	  fprintf(fout, "</PRE>\n\n</BODY>\n</HTML>");
	  fclose(fout);
	}

	pending = 1;
	rmFirst(line);
	tmp = strtok(line, ":");
	fName = makeFName(tmp);

	sprintf(foutname, "%s/%s", BASE_PATH, fName);
	if((fout = fopen(foutname, "w+")) == NULL){
	  convError("Cannot open for writing!");
	  convError(foutname);
	  return 3;
	}
	free(fName);

	fprintf(fout,
		"<HTML>\n<HEAD>\n<TITLE>%s</TITLE>\n</HEAD>\n\n<BODY><PRE>",
		tmp);

      } else if(first == '^'){ /* Make H2 */
	rmFirst(line);
	fprintf(fout, "</PRE>\n\n<H2 ALIGN=Center>%s</H2>\n\n<PRE>\n", line);
	continue;
      } else if(first == '%'){ /* Make Bold */
	rmFirst(line);
	fprintf(fout, "<B>%s</B>\n", line);
      } else {
	if(line[0] != '\0'){
	  parseLine(line);
	}
	fprintf(fout, "%s\n", line);
      }

    }/* while */
    fclose(f);
  }/* for */

  fprintf(stderr, "\nAll done.\n");


  if(pending){
    fprintf(fout, "</PRE>\n\n</BODY>\n</HTML>");
    fclose(fout);
  }

  fclose(f);
  freeTable(c_head);

  return 0;
}


void cleanLine(char *x){
  char tgr_o[] = {
    '�', '�', '�', '�', '�', '�',  '�', '�', '�', '�', '�', '�', '\0'};
  char tgr_r[] = {
    '|', '`', '-', '�', '+', '\'', '|', '-', '-', '.', '|', '/', '\0'};

  int i = 0;

  /* Remove newline at the en of the string returned by fgets() */
  x[strlen(x) - 1] = '\0';

  while(*x != '\0'){
    for(i = 0; tgr_o[i] != '\0'; i++){
      if(*x == tgr_o[i])
	*x = tgr_r[i];
    }
    x++;
  }

  /* Remove DOS-style newline*/
  if(strrchr(x, 0x0D) != NULL){
    *strrchr(x, 0x0D) = 0x0;
  }
}


void rmFirst(char *x){
  strcpy(x, x + 1);
}

char *makeFName(char *x){
  char *tmp = malloc(strlen(x) + 6);
  char *o = tmp;

  while((*tmp = *x)){
    *tmp = tolower(*tmp);

    if(*tmp == ' ')
      *tmp = '_';
    else if(*tmp == ',')
      *tmp = '-';
    else if(*tmp == '.')
      *tmp = '_';
    else if(*tmp == '(')
      *tmp = '-';
    else if(*tmp == ')')
      *tmp = '-';
    tmp++;
    x++;
  }

  strcat(o, ".html");

  return o;
}

void convError(char *x){
  fprintf(stderr, "\n Error: %s\n", x);
}

void parseLine(char *x){
  char *tmp = malloc(1024);
  char *t_o = tmp;
  char *x_o = x;
  char link[50];
  char *l_dup;
  int i, found;
  struct conv *conv;

  tmp[0] = '\0';

  while(*x != '\0'){

    if(*x == '~' && *(x+1) != '~'){
      x++;
      i = 0;
      while(*x != '~' && *x != '\0'){
	link[i++] = *x;
	x++;
      }
      link[i] = '\0';


      /* Do an exact matching first... */
      conv = c_head;
      l_dup = strdup(link);
      strlowr(l_dup);
      found = 0;
      while(conv != NULL){
	if(strcmp(conv->orig, l_dup) == 0){
	  found = 1;
	  break;
	}
	conv = conv->next;
      }

      /* As not all keywords and link texts match exactly, do two more
	 relaxed searches in succession. */
      if(!found){
	conv = c_head;
	while(conv != NULL){
	  if(strncmp(conv->orig, l_dup, strlen(l_dup)) == 0){
	    found = 1;
	    break;
	  }
	  conv = conv->next;
	}

	if(!found){
	  conv = c_head;
	  while(conv != NULL){
	    if(strstr(conv->orig, l_dup) != NULL){
	      break;
	    }
	    conv = conv->next;
	  }
	}
      }

      if(conv == NULL){
	fprintf(stderr, " Warning: No translation for %s\n", l_dup);
	strcat(tmp, link);
      } else {
	strcat(tmp, "<A HREF=\"");
	strcat(tmp, conv->file);;
	strcat(tmp, "\">");
	strcat(tmp, link);
	strcat(tmp, "</A>");
      }

      free(l_dup);

      while(*tmp != '\0') tmp++;
      tmp--;
    }else{
      if(*x == '~')
	x++;
      *tmp = *x;
    }

    tmp++;
    x++;
  }
  *tmp = '\0';

  strcpy(x_o, t_o);
}


int buildConv(int argc, char **argv){
  int files, count = 0, i, entry = 0;
  FILE *f, *fidx, *idx;
  char index[45];
  char fidxname[100];
  char line[200];
  char *tmp, *fName = NULL, *x1, *x2;
  struct conv *conv = NULL;
  struct conv c_list[2000];
  int c_list_len;

  /* Start main index */
  sprintf(line, "%s/index.html", BASE_PATH);
  if((idx = fopen(line, "w+")) == NULL){
    convError("Error writing main index!");
    exit(100);
  }

  fprintf(idx, "<HTML>\n<HEAD>\n <TITLE>HelpPC Reference Library</TITLE>\n"
	  "</HEAD>\n\n<BODY>\n<CENTER>\n<H1>HelpPC Reference Library</H1>\n"
	  "David Jurgens<BR>\n</CENTER>\n<HR WIDTH=140>\n"
	  "<BR>\n\nTopics:<UL>\n");

  for(files = 1; files < argc; files++){  //For all files given to function
    if((f = fopen(argv[files], "r")) == NULL){
      fprintf(stderr, "Error opening %s\n", argv[files]);
      exit(100);
    }

    /* Get index title */
    fprintf(stderr, " Getting index title of %s:\n\t", argv[files]);

    fgets(index, 45, f);
    cleanLine(index);

    if(index[0] != '@'){
      convError("Not a valid help file!");
      exit(1);
    }
    rmFirst(index);

    x1 = strdup(index);
    tmp = strtok(x1, " /,");
    x2 = makeFName(tmp);
    free(x1);

    fprintf(stderr, "%s\n\n", index);
    fprintf(idx, " <LI><A HREF=\"idx_%s\">%s</A>\n", x2, index);

    sprintf(fidxname, "%s/idx_%s", BASE_PATH, x2);
    if((fidx = fopen(fidxname, "w+")) == NULL){
      convError("Error writing topic index!");
      convError(x2);
      free(x2);
      exit(100);
    }

    free(x2);

    fprintf(fidx, "<HTML>\n<HEAD>\n <TITLE>%s</TITLE>\n</HEAD>\n\n<BODY>\n", index);
    fprintf(fidx, "<H1 ALIGN=Center>%s</H1>\n\n", index);
    fprintf(fidx, "<TABLE BORDER=0>\n<TR>\n");

    c_list_len = 0;
    while(fgets(line, 200, f) != NULL){
      cleanLine(line);
      line[strlen(line) - 1] = '\0';

      if(line[0] == ':'){
	rmFirst(line);

	/* Make file name */
	tmp = strtok(line, ":");
	if(tmp != NULL){
	  fName = makeFName(tmp);
	  entry++;
	}

	while(tmp != NULL){
	  count++;

	  c_list[c_list_len].file = malloc(strlen(fName) + 1);
	  c_list[c_list_len].orig = malloc(strlen(tmp) + 1);
	  strcpy(c_list[c_list_len].file, fName);
	  strcpy(c_list[c_list_len].orig, tmp);
	  c_list_len++;

	  conv = malloc(sizeof(struct conv));
	  conv->file = malloc(strlen(fName) + 1);
	  conv->orig = malloc(strlen(tmp) + 1);

	  conv->next = c_head;
	  c_head = conv;

	  strlowr(tmp);
	  strcpy(conv->orig, tmp);
	  strcpy(conv->file, fName);

	  tmp = strtok(NULL, ":");
	}

	free(fName);
      }/* if */
    }/* while */

    idxSortWrt(c_list, c_list_len, fidx);
    for(i = 0; i < c_list_len; i++){
      free(c_list[i].file);
      free(c_list[i].orig);
    }

    fprintf(fidx, "\n</TR>\n</TABLE>\n</BODY>\n</HTML>");

    fclose(f);
    fclose(fidx);
  } /* for */

  fprintf(idx, "</UL>\n<HR>Converted to HTML with a <a href='https://github.com/numberformat/helppc_reference_library_html' target='_blank'>tool written by Stanislav Sokolov</a>.<BR>\n</BODY>\n</HTML>");

  fclose(idx);

  return (count << 16) | (entry & 0xFFFF);
}


void strlowr(char *x){
  while(*x != '\0'){
    *x = tolower(*x);
    x++;
  }
}


void freeTable(struct conv *conv){
  struct conv *x;

  while(conv != NULL){
    free(conv->file);
    free(conv->orig);
    x = conv;
    conv = conv->next;
    free(x);
  }

}


void idxSortWrt(struct conv c_list[], int len, FILE *fidx){
  int i;

  _qsort(c_list, 0, len - 1);

  for(i = 0; i < len; i++){
    fprintf(fidx, " <TD><A HREF=\"%s\">%s</A></TD><TD> </TD>", c_list[i].file, c_list[i].orig);
    if((i+1) % 5 == 0)
      fprintf(fidx, "\n</TR>\n<TR>\n");
  }

}

/* Text with leading underscore is compared from the next character */
void _qsort(struct conv c_list[], int first, int last){
  int i = first, j = last;
  char *med;
  struct conv swap;

  med = c_list[(first + last) / 2].orig;
  if(*med == '_'){
    med++;
  }

  do{
    while(strcasecmp((*c_list[i].orig == '_' ?
		      c_list[i].orig + 1 :
		      c_list[i].orig),
		     med) < 0){
      i++;
    }

    while(strcasecmp(med,
		     *c_list[j].orig == '_' ?
		     c_list[j].orig + 1 :
		     c_list[j].orig) < 0){
      j--;
    }

    if(i <= j){
      swap = c_list[i];
      c_list[i++] = c_list[j];
      c_list[j--] = swap;
    }

  }while(i <= j);

  if(first < j)
    _qsort(c_list, first, j);

  if(i < last)
    _qsort(c_list, i, last);

}
