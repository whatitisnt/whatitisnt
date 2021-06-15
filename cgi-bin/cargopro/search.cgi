#!/usr/bin/perl

require "./setup.pl";

read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
if ($ENV{'QUERY_STRING'} ne '') { $buffer .= "\&$ENV{'QUERY_STRING'}"; }

if ($center) { $center1 = '<center>'; $center2 = '</center>'; }
if ($buffer eq "") { &error('�A�N�Z�X�G���[','�g�p���鏤�i�t�@�C�����w�肳��Ă��܂���B',"Usage; http://URL/search.cgi\?file=���i�Ǘ��t�@�C����(�g���q�͕s�v)"); }

@pairs = split(/&/,$buffer);
foreach $pair (@pairs) {

	($name,$value) = split(/=/, $pair);
	$name2 = $name;
	$value2 = $value;
	$FORM2{$name} = $value;

	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	&jcode'convert(*value,'euc');

	$value =~ s/<//g;
	$value =~ s/>//g;
	$value =~ s/\n//g;
	$value =~ s/\r//g;
	$value =~ s/\t//g;

	#�t�H�[���ϐ���
	$FORM{$name} = $value;
}

$strings_sjis = $FORM{'strings'};
&jcode'convert(*strings_sjis,'sjis');

if ($FORM{'file'} eq '') { &error('�A�N�Z�X�G���[','�g�p���鏤�i�t�@�C�����w�肳��Ă��܂���B',"Usage; http://URL/search.cgi\?file=���i�Ǘ��t�@�C����(�g���q�͕s�v)"); }
if (!-e "$base_dir$FORM{'file'}\.csv") { &error('�ݒ�G���[',"���i�ݒ�t�@�C��$FORM{'file'}��������܂���B"); }

$lockfile = $tmp_dir . "$FORM{'file'}\.lock";
&lock;

#���i�ݒ�t�@�C�����J��
if (!open(FILE,"$base_dir$FORM{'file'}\.csv")) { &error('�G���[','���i�t�@�C�����ǂݏo���܂���B'); }
$item = <FILE>; $item =~ s/,//g;
$msg_top = <FILE>; $msg_top =~ s/,//g;
$msg_btm = <FILE>; $msg_btm =~ s/,//g;

while (<FILE>) { push(@BASE,$_); }
close(FILE);

if ($FORM{'FF'} eq '') { $FF = 0; } else { $FF = $FORM{'FF'}; }
$TO = $FF + $page - 1;
if ($TO > $#BASE) { $TO = $#BASE; }
$hit = 0;
$next_num = '';

foreach $num ($FF .. $#BASE) {

	$BASE[$num] =~ s/\n//g;
	$data = $data2 = $BASE[$num];
	if ($data eq '') { next; }

	&jcode'convert(*data,'euc');
	($code,$name,$tanka,$tax,$rem,$url,$zaiko,$type) = &DecodeCSV($data);
	$search_strings = "$code $name $rem";

	if ($FORM{'strings'} ne '') {

		if ($search_strings =~ /^([\x00-\x7F]|[\x8E\xA1-\xFE][\xA1-\xFE]|\x8F[\xA1-\xFE]{2})*$FORM{'strings'}/i) { ; } else { next; }
	}

	if ($FORM{'tanka'} ne '') {

		$tanka =~ s/\\//g;
		if ($tanka == 0) { next; }

		($min,$max) = split(/\,/,$FORM{'tanka'});

		if ($min eq '-') { if ($tanka >= $max) { next; }}
		elsif ($max eq '-') { if ($tanka < $min) { next; }}
		else { if ($tanka < $min || $tanka >= $max) { next; }}
	}

	if ($hit == $page) { $next_num = $num; last; }
	else { push(@NEW,$data2); $hit++; }
}

if (!@NEW) { &error('��������','���w��̏����ł͒��o����܂���ł����B'); }

if ($backreset) { $body =~ s/<body/<body onLoad="document.Items.reset();"/i; }

#��ʏo�͊J�n
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
$css
</HEAD>
$center1
$body
<h2>$item</h2>
<table><tr><td>$msg_top</td></tr></table>
<form method=POST action="cargo.cgi" name="Items">
<input type=hidden name="_file" value="$FORM{'file'}">
<table border="1" bordercolor="#FFFFFF" cellspacing="0" cellpadding="4">
<tr>
<th><font size=+1></font>�@</th>
<th align=left><font size=+1>TOP SIDE</font></th>
<th align=left><font size=+1>BOTTOM SIDE</font></th>
<th><font size=+1>�P��(�~)</font></th>
EOF

if ($viewzaiko) { print "<th><font size=+1>�݌�(�{)</font></th>\n"; }

print <<"EOF";
<th><font size=+1>������</font></th>
</tr>
EOF

#-------------------->

foreach (@NEW) {

	s/\t//g;
	s/\n//g;

	if (/^#/) { next; }
	if (/^$/) { next; }

	($code,$name,$tanka,$tax,$rem,$url,$zaiko,$type) = &DecodeCSV($_);

	if ($tax == -1) { $tax = '(��ې�)'; }
	elsif ($tax == -2) { $tax = '(�s�ې�)'; }
	elsif ($tax == -3) { $tax = '(�ō�)'; }
	else { $tax = ''; }

	$zaiko0 = 0;
	if ($zaiko =~ /\d/ && $zaiko == 0) { $zaiko = '�~��'; $zaiko0 = 1; }
	elsif ($zaiko =~ /\d/) { $zaiko = "�c$zaiko"; }
	else { $zaiko = '�Z��'; }

	#���i���Ɣ��l���̃R���������s�ɕϊ�
	$name =~ s/\:/<br>/g;
	$rem =~ s/\:/<br>/g;

	#URL���L������Ă���΃����N����
	if ($url ne '') { $name = "<a href=\"$url\">$name</a>"; }

	$tanka =~ s/\\//g; # �~�L��������
	1 while $tanka =~ s/(.*\d)(\d\d\d)/$1,$2/g; #�P���ɃJ���}�}��

	$c++;
	if ($c % 2) { $bg = "#ffeedd"; } else { $bg = "#ffffff"; } #�P�s�����ɃZ���̔w�i�F��ւ���

	print <<"EOF";
	<tr>
	<td align=left>$code</th>
	<td align=left>$rem</td>
	<td align=left><font color="#ffe600">$name</font></td>
	<td align=right><font size=-1 color="#ffe600">$tax</font> <font color="#ffe600">$tanka</font></td>
EOF
	if ($viewzaiko) { print "<td align=right><font color=\"#ffe600\">$zaiko</font></td>\n"; }

	print <<"EOF";
	<td align=right>
EOF
	#���ʓ��̓^�C�v�ɂ���ď���
	if ($zaiko0) {

		#�X�y�[�X
		print "�@";
	}
	elsif ($type == 1) {

		#���i�R�[�h�̓Z�~�R�����ŋ��ތ`���ō��ږ��Ƃ��ēn��
		print "<input type=checkbox name=\"X$code\X\" value=\"1\">�w��";
	}
	elsif ($type == 2) {

	#���i�R�[�h�̓Z�~�R�����ŋ��ތ`���ō��ږ��Ƃ��ēn��
		print "<select size=1 name=\"X$code\X\">\n";

		print <<"EOF";
		<option value="0" selected>0</option>
EOF
		foreach (1 .. $select_to) { print "<option value=\"$_\">$_</option>\n"; }
		print "</select>�{";
	}
	else {
		#���i�R�[�h�̓Z�~�R�����ŋ��ތ`���ō��ږ��Ƃ��ēn��
		print "<input type=text size=5 name=\"X$code\X\" value=\"0\">�{";
	}

	print "</td></tr>\n";
}

if (-e $lockfile) { unlink($lockfile); }
print "</table><p>\n";

if ($next_num ne '') {

	while (($key,$val) = each %FORM2) {

		if ($key ne 'FF') { $buf = "$buf&$key=$val"; }
	}

	print "<h3>�y<a href=\"search.cgi?$buf&FF=$next_num\">����$page��</a>�z</h3>\n";
}

print <<"EOF";
<input type="image" src="../../cargoimg/kago.gif" border="0">
<a href="#" onClick="JavaScript:Items.reset()"><img src="../../cargoimg/reset.gif" border="0"></a>
</form>
<p>
<table><tr><td>$msg_btm</td></tr></table><p>
<hr><p>
<a href="JavaScript:history.back()"><img src="../../cargoimg/mae.gif" border="0"></a>
<a href="cargo.cgi?_file=$FORM{'file'}"><img src="../../cargoimg/chuumonkago.gif" border="0"></a>
<a href="$top"><img src="../../cargoimg/menu.gif" border="0"></a><p>
<font size=-1>�� ��ʂ�߂��Ă��̉�ʂɗ����ꍇ��<a href="search.cgi\?file=$FORM{'file'}">�ŐV�̏�ԂɍX�V</a>���Ă��������B</font><p>
$center2</body></html>
EOF

exit;

sub lock {

	# ���b�N�����̎������� symlink()�D��
	$symlink_check = (eval { symlink("",""); }, $@ eq "");
	if (!$symlink_check) {

		$c = 0;
		while(-f "$lockfile") { # file��

			$c++;
			if ($c >= 3) { &error('���g���C�G���[','�������܍��G���Ă���\��������܂��B','�߂��Ă�����x���s���Ă݂Ă��������B'); }
			sleep(2);
		}
		open(LOCK,">$lockfile");
		close(LOCK);
	}
	else {
		local($retry) = 3;
		while (!symlink(".", $lockfile)) { # symlink��

			if (--$retry <= 0) { &error('���g���C�G���[','�������܍��G���Ă���\��������܂��B','�߂��Ă�����x���s���Ă݂Ă��������B'); }
			sleep(2);
		}
	}
}

sub DecodeCSV {

	local($text) = @_;
	local(@fields) = ();
	local($a);

	$text =~ s/\n//;
	if ($text eq '') { return (); }

	while ($text =~ m/"([^\\]*(\\.[^\\]*)*)",?|([^,]+),?|,/g) {

		$a = defined($1) ? $1 : $3;
		$a =~ s/""/"/g;

		$a =~ s/&/&amp;/g;
		$a =~ s/"/&quot;/g;
		$a =~ s/</&lt;/g;
		$a =~ s/>/&gt;/g;

		push(@fields,$a);
	}
	push(@fields, undef) if $text =~ m/,$/;

	@fields;
}

sub error {

	if (-e $lockfile) { unlink($lockfile); }

	local (@msg) = @_;
	local ($i);

	print "Content-type: text/html\n\n";

	print <<"EOF";
	<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN">
	<HTML>
	<HEAD>
	<TITLE>ERROR</TITLE>
	<meta http-equiv="Content-Type" content="text/html; charset=x-sjis">
	<SCRIPT language="JavaScript">
	<!--
	function PageBack(){ history.back(); }
	//-->
	</SCRIPT>
	$css
	</HEAD>
	$body
	$center1
	<h1>$_[0]</h1>
EOF

	print "\n";
	foreach $i (1 .. $#msg) { print "$msg[$i]<br>\n"; }
	print "\n";

	print <<"EOF";
	<h3>[<a href="JavaScript:history.back()">�߂�</a>]</h3>
	$center2</body></html>
EOF
	exit;
}
