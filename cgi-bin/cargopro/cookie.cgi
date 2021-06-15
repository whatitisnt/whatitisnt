#!/usr/bin/perl

require "./setup.pl";

$cgi_base_dir = "http://$ENV{'SERVER_NAME'}$ENV{'SCRIPT_NAME'}";

$buffer = $ENV{'QUERY_STRING'};
if ($buffer eq '') { &regist; }
elsif ($buffer eq 'result') { $cookies = $ENV{'HTTP_COOKIE'}; &html; }
else { &error('�����G���[',''); }
exit;

sub html {

	print "Content-type: text/html\n\n";

	print <<"EOF";
	<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN">
	<HTML>
	<HEAD>
	<TITLE></TITLE>
	<meta http-equiv="Content-Type" content="text/html; charset=x-sjis">
	<SCRIPT language="JavaScript">
	<!--
	function PageBack(){ history.back(); }
	//-->
	</SCRIPT>
	</HEAD>
	$body
	<h1>��������</h1>
EOF
	if ($cookies ne '') { print "�V���b�s���O�o�X�P�b�g�����p�\\�ł�.<p>\n"; }
	else {

		print "���Ȃ��̃u���E�U�ł́A�V���b�s���O�o�X�P�b�g�͂����p�ł��܂���.<br>\n";
		print "�l�b�g�X�P�[�v�܂��̓C���^�[�l�b�g�G�N�X�v���[���������p��������.<p>\n";
	}

	print "<hr noshade><h3><a href=\"JavaScript:history.back()\">�߂�</a></h3>\n";
	print "</body></html>\n";
	exit;

}

sub regist {

	print "Set-Cookie: cookie=$modoru;\n";
	print "Location: $cgi_base_dir\?result\n\n";
	exit;
}

sub error {

	local (@msg) = @_;
	local ($i);

	print "Content-type: text/html\n\n";

	print <<"EOF";
	<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN">
	<HTML>
	<HEAD>
	<TITLE>$title_bar</TITLE>
	<meta http-equiv="Content-Type" content="text/html; charset=x-sjis">
	<SCRIPT language="JavaScript">
	<!--
	function PageBack(){ history.back(); }
	//-->
	</SCRIPT>
	</HEAD>
	$body
	<h1>$_[0]</h1>
	<table><tr><td>
EOF
	foreach $i (1 .. $#msg) { print "$msg[$i]<br>\n"; }

	print <<"EOF";
	</td></tr></table>
	<h3>[<A HREF="JavaScript:history.back()">�߂�</A>]</h3>
	</body></html>
EOF
	exit;
}
