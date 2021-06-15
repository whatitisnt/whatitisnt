#!	/usr/bin/perl
#
#	mopera FTP Server System for Step3
#	happy.pl
#
#	Rev.A	01-Jul-00	Ono	Conver from Step2
#
#

if ($ENV{'REQUEST_METHOD'}  eq "POST") {
	read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	@pairs = split(/&/, $buffer);
} else {
	@pairs = split(/&/, $ENV{'QUERY_STRING'});
}

# Now digest the data, putting it into a more useful format.

foreach $pair (@pairs) {
	($key, $value) = split(/=/, $pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$value =~ tr/\cM/\n/;
	# print "$key = $value<BR>\n";
	eval("\$$key = \"$value\"");
	$FORM{$key} = $value;
}

# Now let's generate a web page to display the data we've got.

print "Content-Type: text/html\n\n\n",
	"<HTML>\n",
	"<HEAD><TITLE>CGI Data Dump</TITLE></HEAD>\n",
	"<BODY>\n",
	"<H1>CGI Data Dump</H1>\n<HR>\n",
	"Here is the data that is availabe to this CGI program:<P>\n";

print "<I><B>Command Line Arguments</B></I><P>\n\n";

if ($#ARGV < 0) {
	print "(No command-line arguments)<P>\n";
} else {
	print "<TABLE BORDER=1>\n";
	print "<TR>\n";
	foreach $var (@ARGV) {
		print "<TD>$var</TD>";
	}
	print "</TR>\n";
	print "</TABLE><P>\n\n";
}

print "<I><B>CGI values passed</B></I><P>\n\n";

print "<TABLE BORDER=1>\n";
if ($#pairs < 0) {
	print "<TR><TD>(No CGI Variables)</TD></TR>\n";
} else {
	foreach $var (keys(%FORM)) {
		print "<TR><TD>$var</TD><TD>$FORM{$var}</TD></TR>\n"
	}
}
print "</TABLE><P>\n\n";

print "<I><B>Environment variables available</B></I><P>\n\n";
print "<TABLE BORDER=1>\n";
foreach $var (sort(keys(%ENV))) {
	print "<TR><TD>$var</TD><TD>$ENV{$var}</TD></TR>\n"
}
print "</TABLE><P>\n\n";

print "<I><B>Other useful enviroment information</B></I><P>\n\n";
print "<TABLE BORDER=1>\n";

if ($OS eq "Windows_NT") {
	($user) = getpwuid($>);
	print "<TR><TD>USER</TD><TD>$user</TD></TR>\n";
	print "<TR><TD>PWD</TD><TD>",`/bin/pwd`,"</TD></TR>\n";
}
print "<TR><TD>Process ID</TD><TD>$$</TD></TR>\n";
print "</TABLE><P>\n\n";


print "</BODY>\n";
print "</HTML>\n";

exit;

