
# Zpl-Label-Print

Sublime Text plugin for printing ZPL labels to Zebra-compatible label printers 
by filling a template with selected data values.



## Examples:





## Overview:


### How it works:

1. You have a label template with variable fields.
2. You select some tabulated text containing variable values.
3. Each row is used to generate one label (ZPL format).
4. The labels are sent to the label printer together with the printer config (just static ZPL).


### Example:

* The default fields are "datestr", "sampleid", and "sampledesc".
* Select the following text:

```
datestr	sampleid	sampledesc
20191028	RS573a1	RRO core1 200uM/48
20191028	RS573a2	RRO core2 200uM/48
```

* Press `Ctrl+Shift+P` and select ""Print ZPL label(s) using SELECTED TAB-separated values (first line is header with fieldnames)."




### Installation and configuration overview:

1. Install this package/plugin.
2. Make sure your label printer is ready.
3. Configure plugin settings:
	* Specify `label_template_file` zpl file.
	* Specify `printerconfig_zpl_file` - a zpl file used to configure the ZPL label printer for each print job.
	* Specify the label printer name (`printer`), e.g. `\\localhost\usb001_generic_text_printer`.
4. Customize your label template and printerconfig ZPL files. 
	* You can use the files in the `examples` folder as a starting point. 
	  These files were created for printing on 
	  LabTags Cryogenic Barcode Labels (1.25" X 0.625" + 0.4375" #JTTA-172) labels using a 
	  Zebra ZD420 thermal transfer label printer.
	  The default fields are "datestr", "sampleid", and "sampledesc",
	  which is used to print a single barcode on the tube lid label, and three text boxes on the tube-side label.


## Installation:

OBS: Zpl-Label-Print is not 



### Installation from source:

This method requires you to be comfortable using the command line. 

1. First, you need to determine where your Sublime Text packages are stored.
	In Sublime Text, select `Preferences → Browse Packages...`.
	This should bring up Windows File Explorer.
	Copy the folder path to the clipboard.

2. Download the latest version from github. You can do this either manually or using git:

	```cmd
	cd <paste the folder path containing your Sublime Text packages>
	git clone https://github.com/scholer/sublime-zpl-label-print ZPL-Label-Print
	```
	
	In Windows File Explorer, you should now see a new folder named `ZPL-Label-Print` 
	inside the folder containing your Sublime Text package.
	If you do not see this new folder, you did something wrong 
	(e.g. didn't paste the folder path properly when using `cd` to change directory).

3. Restart Sublime Text.
	Press `~` to bring up the console inside Sublime Text.
	Look for a line saying "ZPL-Label-Print package loaded!".
	If you see this line, the package is properly installed.
	Otherwise, go back and make sure you did everything right,
	checking folder paths, etc.


OBS: There are other ways of navigating to the correct folder in the command line.

* In Windows File Explorer, just type `cmd` in the folder path bar, and this will open 
	a terminal with the correct working directory.
	
* In the terminal, you can drag-and-drop the folder from Finder into your terminal
	after typing `cd ` - this will insert the folder path without having to copy/paste.


#### Advanced: Using symbolic link

* You can also symlink the source folder from within the Sublime Text packages folder.
* On Windows:
	```cmd
	mklink /D ZPL-Label-Print <path-to-sublime-text-dev-folder>\sublime-zpl-label-print
	```
	E.g. 
	```cmd
	mklink /D ZPL-Label-Print C:\Users\au206270\Dev\sublime-text-dev\sublime-zpl-label-print
	```
* In File Explorer (or Finder/whatever), make sure you can double-click the symbolic link
	and traverse it to the source folder.
	

## Setting up your printer:

On Windows, the most reliable way to print requires the printer to be a shared network printer.

You need to note down the hostname (e.g. localhost) and the shared printer name.
The name should not contain any spaces or special characters.

The printer name should look something like this:

	\\localhost\usb001_generic_text_printer



## Configuring plugin settings:

Open the settings for this plugin/package: In Sublime Text, go 
"Preferences" → "Package Settings" → "ZPL-Label-Print" → "ZPL-Label-Print Settings".
The panel on the left shows you the default settings, while the panel to the right contains the 
user-customized settings. A user-customized setting always take precedence over a default setting.

You can use this to specify e.g. where your `label_template.zpl` and `printer_config.zpl` files are 
stored, the default columns names and order, etc.
 




## Defining your label template and printer configuration:

OBS: This *does* require a bit of "getting your hands dirty" and not being too intimidated looking 
at text files with weird-looking commands in them. Don't worry, I'll try to guide you through it.

Printing on a ZPL-compatible printer is done simply by generating a ZPL text file and 
sending this to the printer.

The ZPL text file contains the following things:

1. ZPL commands that configures the ZPL printer (e.g. darkness, print speed, etc.).
	This is not strictly required since most configuration parameters are saved 
	from one print job to the next. However, if you turn the ZPL label printer off, 
	you may find that it has forgotten the previous configuration. 
	So it is generally best to just send the exact configuration to the printer for every print job.

2. The actual label printing commands. These are generated for each label and joined together.

In order to print on a ZPL-compatible printer, you need to define the following files:

1. A ZPL file containing your desired printer configuration. 
2. A ZPL label template, defining how the printed labels should look, and where each value is printed on the label.

There are many ways to generate these two files (refer to Appendix I below for more info):

1. Use ZebraDesigner or similar GUI application to design the label, 
	then print the label to a file - this will generate a ZPL text file that you can modify as needed.

2. Use one of the label templates in the `example_files` folder for this plugin. 
	You can open this folder from Sublime Text by going 
	"Preferences" → "Package Settings" → "ZPL-Label-Print" → "Browse ZPL Example Files…".
	You can then use e.g. [Labelary Viewer](http://labelary.com/viewer.html) to further customize 
	your label template.




## Appendix I: Creating and customizing your ZPL files


#### Option I: Create a label in ZebraDesigner or other label creator GUI application.

0. Create the desired template. It can have multiple "fields" with text and/or barcodes.
	For example, you can create a label containing three text fields 
	("date", "sample_id", "sample_description") and one barcode "barcode-placeholder-text".
1. Print the label to a file, and open the file in a text editor (e.g. Sublime Text).
2. Find the first place containing `^XZ`. 
	Cut everything up to and including the first `^XZ` and paste it into a new file named `printer-config.zpl`.
3. Cut the rest and paste it in a new file named `label-template.zpl`.
4. Save both files in a suitable location.
5. Finally, edit the `label-template.zpl` contents to insert python `{placeholder}` fields 
	in the places where you would like to insert your values.
	Continuing the example above, you just need add curly-braces around the text, so it reads:
	`{date}` instead of `date`, `{sample_id}` instead of `sample_id`, 
	`{sample_description}` instead of `sample_description`, etc.
	Now, `date`, `sample_id` and `sample_description` are placeholder names.
	If you have a CSV file containing these columns, the placeholder names will be substituted 
	by the column values in your CSV data.
	
	

#### Option II: Use Labelary to create or customize your ZPL template

Go to http://labelary.com/viewer.html and paste your ZPL template code in here.

Labelary Viewer allows you to see how a certain ZPL file will look when printed.

You can also use Labelary viewer to modify existing ZPL templates without going through ZebraDesigner.

Labelary is also particularly useful if you are trying to learn how to write ZPL code yourself.



#### Option III: Learn to write ZPL commands

This is not actually as hard as it sounds.

A good way to learn is to look at the ZPL files that ZebraDesigner creates.

ZPL files consists of multiple ZPL commands; 
each command starts with either a caret, `^`, or a tilde, `~`.
For example, the `^XA` command indicates the beginning of a new label, while `^XZ` indicates the end of a label.
`^FT20,130` will insert a new text field at position (20, 130). 
`^FD<text>` will insert `<text>` in the text field.
 
You can refer to the ZPL reference book to see what each command does.


You can use [Labelary Viewer](http://labelary.com/viewer.html) to see how the label printed 
by a given set of ZPL commands will appear. Use this to play around with the different ZPL commands.





## Appendix II: Changing default label font

The default Zebra font (`ZPL-0`) is not super pretty.
The hyphens in particular have too much white-space around them, making them appear more like en- or em-dashes.
However, right now, the Zebra-0 font appears to be the only scalable font?


To change the default font, refer to the link below.
You can use the `^FL` and `^CW` commands to change the font on a label-by-label basis.

You can use ZebraDesigner to find fonts already on your printer (marked with the printer symbol).

You can use Zebra Setup Utilities to transfer fonts from your pc to your label printer.


Refs:

* https://www.zebra.com/us/en/support-downloads/knowledge-articles/ait/downloading-and-using-fonts-on-zebra-zpl-printers.html
* https://www.zebra.com/us/en/support-downloads/knowledge-articles/zebra-setup-utilities--downloading-fonts-to-a-printer.html
* https://www.zebra.com/us/en/support-downloads/knowledge-articles/printing-multiple-fonts-using-zpl-fl.html
* https://www.zebra.com/content/dam/zebra/manuals/printers/common/programming/zpl-zbi2-pm-en.pdf
* https://minisoft.com/support/index.php/zebra-font-support/
	* The "TPCL-A" and "TPCL-B" fonts in this ref look nicer than the standard Zebra "ZPL-0" font (particularly the hyphen).



## Appendix III: Reading barcodes


The following apps can be used to read datamatrix barcodes:

* "Cognex barcode reader"
* "ZXing Barcode scanner" 
* "Barcode Scanner X" from DynamSoft.



