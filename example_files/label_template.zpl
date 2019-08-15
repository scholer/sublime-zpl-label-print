
^FX[ Label Format ]^FS
^FX[ PrintWidth is 395 dots = 49.375 mm = 1.944 in ]^FS
^FX[ LabelLength is 152 dots = 19.125 mm = 0.753 in ]^FS

^XA
^MMT
^PW395
^LL0153
^LS0


^FX[ SampleID - top left ]^FS

^FO20,25
^A0N,26,26
^FB140,2,0,L,0
^FD{sampleid}
^FS


^FX[ Date string - top right ]^FS

^FO150,25
^A0N,26,26
^FB110,2,0,R,0
^FD{datestr}
^FS


^FX[ Sample description - multi-line text box ]^FS

^FT20,130
^A0N,28,28
^FB240,3,0,C,0
^FD{sampledesc}
^FS


^FX[ Lid datamatrix 2D barcode ]^FS
^FX[ For Quality 200, datamatrix size should be 2 if content is more than 33 chars]^FS
^FX[ (You can use size 4 for content less than 10 chars.) ]^FS
^FX[ (The length depends on which characters are actually used.) ]^FS
^FX[ Use ~ as escape character (default is underscore - yikes) ]^FS

^BY48,48
^FT311,100
^BXN,2,200,0,0,1,~,1
^FH\^FD{datestr} {sampleid} {sampledesc}
^FS


^PQ1,0,1,Y

^XZ

