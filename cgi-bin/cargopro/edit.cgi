#!/usr/bin/perl

# �V���b�s���O�o�X�P�b�g�E�v�� ���@�[�W�����R�p
# ���i�ݒ�t�@�C���ҏW�v���O���� edit.cgi
# (c)rescue.ne.jp

# 1999/9/7	�o�O�C��
# 1999/9/20	�G�N�Z��CSV�Ή�(�o�C�i������������)
# 1999/12/6	CSV�ϊ��������@�̕ύX
# 2000/1/17	CSV�ϊ��������@�̕ύX
# 2000/3/21	MD5�Ή�

#----------------------------------------------------------------------------

#�������ݒ�t�@�C��
require "./setup.pl";

#���ҏW�p�p�X���[�h
#�@���̂b�f�h�����s�����ۂɓ��͂��K�v�ȕҏW�җp�̃p�X���[�h�̐ݒ�ł��B
#�@�Y�t�̃p�X���[�h�����c�[��crypt.cgi�Ő��������u�Í������ꂽ�p�X���[�h�v�����̂܂܃R�s�[���܂��B
#�@$admin_key = '���̕����ɃR�s�[���܂�';

$admin_key = '$1$Y8$RELUvhpXQUOORsG7hwVS1.';

#���\���� (0:���� 1:�t��) .. �V�K�L�^�͂���Ɋ֌W�Ȃ��f�[�^�̌��ɒǉ������
$rev = 0;

#----------------------------------------------------------------------------

@TYPE = ('�������͎�','�`�F�b�N�{�b�N�X��','�Z���N�g��');

($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
@wday_array = ('��','��','��','��','��','��','�y');
$date_now = sprintf("%04d�N%01d��%01d��(%s)%02d��%02d��%02d�b",$year +1900,$mon +1,$mday,$wday_array[$wday],$hour,$min,$sec);

if ($ENV{'REQUEST_METHOD'} eq "POST") { read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'}); }
else { $buffer = $ENV{'QUERY_STRING'}; }

@pairs = split(/&/,$buffer);
foreach $pair (@pairs) {

	($name,$value) = split(/=/,$pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	&jcode'convert(*value,'sjis');

	$value =~ s/\n//g;
	$value =~ s/\r//g;

	if ($value =~ /^(-EDIT-|-NEW-)$/) { $edit_num = $name; $EDIT = 1; }
	if ($value =~ /^(-DEL-)$/) { $delete = $name; $DELETE = 1; }
	if ($name eq 'key') { push(@EDIT,$value); }
	else { $FORM{$name} = $value; }
}

$file = $FORM{'file'};

if ($file eq '') { &error("File Not Found","�ҏW����t�@�C�����w�肳��Ă��܂���.","Usage; http://$ENV{'SERVER_NAME'}$ENV{'SCRIPT_NAME'}\?file=���i�Ǘ��t�@�C����(�g���q�͕s�v)"); }
if (!-e "$base_dir$file\.csv") { &error('�ݒ�G���[',"���i�ݒ�t�@�C��$file��������܂���.","Usage edit.cgi?file=���i�Ǘ��t�@�C����"); }

if ($FORM{'ADMIN_KEY'} eq '') { &input; }

if ($admin_key =~ /^\$1\$/) { $salt = 5; } else { $salt = 2; }
if (crypt($FORM{'ADMIN_KEY'},substr($admin_key,0,$salt)) ne $admin_key) { &error('Authorization Required'); }

$lockfile = $tmp_dir . "$file\.lock";

&lock;

if (!open(IN,"$base_dir$file\.csv")) { &error("File Not Open","$file\.csv���J�����Ƃ��ł��܂���."); }
$head1 = <IN>; $head1 =~ s/,//g;
$head2 = <IN>; $head2 =~ s/,//g;
$head3 = <IN>; $head3 =~ s/,//g;
$head4 = <IN>;
@BASE = <IN>;
close(IN);

if ($rev) { @BASE = reverse @BASE; }

if ($EDIT) { &edit($edit_num); }
elsif ($DELETE) { &delete($delete); }
elsif ($FORM{'action'} ne '') { &regist(@EDIT); }

$start = $FORM{'start'};
if ($start eq '') { $start = 0; }

$to = $#BASE;

&html($start,$to);

if (-e $lockfile) { unlink($lockfile); }
exit;

sub html {

	local ($start,$to) = @_;
	$next = $to + 1;
	if ($next > $#BASE) { $next = ''; }

	print "Content-type: text/html\n\n";
	print <<"EOF";
	<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN">
	<HTML>
	<HEAD>
	<TITLE>$file</TITLE>
	<SCRIPT language="JavaScript">
	<!--
	function PageBack(){ history.back(); }
	function message()
	{
		f = confirm("�폜���s���Ă�낵���ł����H");
		return f
	}
	//-->
	</SCRIPT>
	</HEAD>
	<BODY>
	<h1>EDIT $file</h1>
	<h2>�^�C�g��; $head1</h2>
	<hr noshade>
	$head2
	<hr noshade>
	<form action="$ENV{'SCRIPT_NAME'}" method=POST>
	<input type=hidden name="file" value="$file">
	<input type=hidden name="ADMIN_KEY" value="$FORM{'ADMIN_KEY'}">
	<input type=hidden name="start" value="$end">
	<input type=hidden name="restart" value="$start">
	<h4>�V�K�o�^<input type=submit name="-NEW-" value="-NEW-"></h4>
	<table border>
	<tr>
	<th nowrap>�ҏW</th>
	<th nowrap>���i�R�[�h</th>
	<th nowrap>���i��</th>
	<th nowrap>�P��(�~)</th>
	<th nowrap>����ŗ�(%)</th>
	<th nowrap>���l</th>
	<th nowrap>URL</th>
	<th nowrap>�݌ɐ�</th>
	<th nowrap>���͌`��</th>
	<th nowrap>�폜</th>
	</tr>
EOF
	foreach $num ($start .. $to) {

		($code,$fname,$tanka,$tax,$rem,$url,$zaiko,$type) = &DecodeCSV($BASE[$num]);

		if ($zaiko ne '' && $zaiko == 0) { $zaiko = "�~��"; }
		elsif ($zaiko > 0) { $zaiko = "�c$zaiko"; }
		else { $zaiko = "�Z��"; }

		if ($tax == -1) { $tax = '��ې�'; }
		elsif ($tax == -2) { $tax = '�s�ې�'; }
		elsif ($tax == -3) { $tax = '�ō�'; }

		$rem =~ s/:/<br>/g;

		$num2 = $num + 1;

		$border++;
		if ($border % 2 != 0) { $bgcolor = "bgcolor=#ffeedd"; } else { $bgcolor = ""; }

		print <<"EOF";
		<tr>
		<td nowrap $bgcolor><input type=submit name="$num" value="-EDIT-"></td>
		<td nowrap $bgcolor>$code</td>
		<td nowrap $bgcolor>$fname</td>
		<td nowrap $bgcolor align=right>$tanka</td>
		<td nowrap $bgcolor align=right>$tax</td>
		<td nowrap $bgcolor>$rem</td>
		<td nowrap $bgcolor><a href="$url" target=_blankk>$url</a></td>
		<td nowrap $bgcolor align=right>$zaiko</td>
		<td nowrap $bgcolor align=center>$TYPE[$type]</td>
		<td nowrap $bgcolor><input type=submit name="$num" value="-DEL-" onClick="message(); return f"></td>
		</tr>
EOF
	}

	print <<"EOF";
	</table><p>
	<hr noshade>
	$head3
	<hr noshade>
	</form>
EOF
	if ($next ne '') {

		print <<"EOF";
		<form action="$ENV{'SCRIPT_NAME'}" method=POST>
		<input type=hidden name="start" value="$next">
		<input type=submit value="���̃y�[�W">
		</form>
EOF
	}

	print <<"EOF";
	<form action="$ENV{'SCRIPT_NAME'}" method=POST>
	<input type=hidden name="file" value="$file">
	<input type=hidden name="ADMIN_KEY" value="$FORM{'ADMIN_KEY'}">
	<input type=submit value="�ŐV�̏�ԂɍX�V">
	</form>

	������<ul>
	<li>�{�^���͂P�񂾂������ď�������������܂ő҂��Ȃ��ƃf�[�^���j�����鋰�ꂪ����܂�.
	<li>��ʂ�߂��ă{�^���������ƌ듮�삵�܂��̂Ő�΂ɔ����Ă�������.
	<li>��ʂ�߂�����K��[�ŐV�̏�ԂɍX�V]���Ă��瑀�삵�Ă�������.
	<li>�u���E�U�̍ēǍ��{�^�����ʈړ��{�^�����͎g��Ȃ��ł�������.
	<li>�w�b�h���e�[�����b�Z�[�W�̒��r�ҏW�́A�C�ӂ̃f�[�^�̕ҏW���ōs���Ă�������.
	</ul><p>
	</BODY></HTML>
EOF
}

sub edit {

	local ($target) = @_;
	if ($target eq '-NEW-' || $target > $#BASE) { $FORM{'restart'} = 0; }

	if ($target ne '-NEW-') {

		($code,$fname,$tanka,$tax,$rem,$url,$zaiko,$type) = &DecodeCSV($BASE[$target]);
	}
	else { 	$target = 'ADD'; }

	if ($type eq '') { $type = 0; }
	$selected[$type] = 'selected';

	$head1 =~ s/&/&amp;/g; $head1 =~ s/"/&quot;/g; $head1 =~ s/</&lt;/g; $head1 =~ s/>/&gt;/g;
	$head2 =~ s/&/&amp;/g; $head2 =~ s/"/&quot;/g; $head2 =~ s/</&lt;/g; $head2 =~ s/>/&gt;/g;
	$head3 =~ s/&/&amp;/g; $head3 =~ s/"/&quot;/g; $head3 =~ s/</&lt;/g; $head3 =~ s/>/&gt;/g;

	print "Content-type: text/html\n\n";
	print <<"EOF";
	<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN">
	<HTML>
	<HEAD>
	<TITLE>$file</TITLE>
	<SCRIPT language="JavaScript">
	<!--
	function PageBack(){ history.back(); }
	//-->
	</SCRIPT>
	</HEAD>
	<BODY>
	<h1>NEW/EDIT $file</h1>
	<form action="$ENV{'SCRIPT_NAME'}" method=POST>
	<input type=hidden name="file" value="$file">
	<input type=hidden name="ADMIN_KEY" value="$FORM{'ADMIN_KEY'}">
	<input type=hidden name="action" value="$target">
	<input type=hidden name="start" value="$FORM{'restart'}">

	�^�C�g�� <input type=text name="head1" value="$head1" size=60><br>
	�w�b�h���b�Z�[�W <input type=text name="head2" value="$head2" size=80><br>
	�e�[�����b�Z�[�W <input type=text name="head3" value="$head3" size=80><p>

	<table border>
	<tr>
	<th nowrap>���ږ�</th>
	<th nowrap>�ҏW�t�H�[��</th>
	</tr>

	<tr>
	<th nowrap><font size=-1>���i�R�[�h</font></th>
	<td nowrap><input type=text name="key" value="$code" size=10> (�d���ɒ���) ���p�p��������уn�C�t��</td>
	</tr>
	<tr>
	<th nowrap><font size=-1>���i��</font></th>
	<td nowrap><input type=text name="key" value="$fname" size=30></td>
	</tr>
	<tr>
	<th nowrap><font size=-1>�P��</font></th>
	<td nowrap><input type=text name="key" value="$tanka" size=10>�~ ���p����</td>
	</tr>
	<tr>
	<th nowrap><font size=-1>����ŗ�</font></th>
	<td nowrap><input type=text name="key" value="$tax" size=3>�� (��ې�:-1 �s�ې�:-2 �ō�:-3 �ې�:�ŗ�����) ���p����</td>
	</tr>
	<tr>
	<th nowrap><font size=-1>���l</font></th>
	<td nowrap><input type=text name="key" value="$rem" size=60> (�C��) :(�R����)�ŉ��s</td>
	</tr>
	<tr>
	<th nowrap><font size=-1>URL</font></th>
	<td nowrap><input type=text name="key" value="$url" size=60> (�C��)</td>
	</tr>
	<tr>
	<th nowrap><font size=-1>�݌ɐ�</font></th>
	<td nowrap><input type=text name="key" value="$zaiko" size=5> (�݂�:�� ����:0 �݌ɊǗ�:�݌ɐ�) �󗓂܂��͔��p����</td>
	</tr>
	<tr>
	<th nowrap><font size=-1>���͌`��</font></th>
	<td nowrap><select name="key" size=1>
	<option value="0" $selected[0]>�������͎�</option>
	<option value="1" $selected[1]>�`�F�b�N�{�b�N�X��</option>
	<option value="2" $selected[2]>�Z���N�g��</option></select></td>
	</tr>

	</table><p>
	<input type=submit value="�L�^����"><input type=reset value="���Z�b�g">
	</form>
	<h3>[<A HREF="JavaScript:history.back()">�ҏW����߂�</A>]</h3>
	������<ul>
	<li><b>�݌ɊǗ��@�\\���g���Ă���ꍇ�́A�ҏW����O�ɐ\\�����݉�ʂ�����Ă��������B</b>�������Ȃ��ƁA�ҏW���ɍ݌ɐ����ω�����\\��������A��������������܂���B
	<li>�{�^���͂P�񂾂������ď�������������܂ő҂��Ȃ��ƃf�[�^���j�����鋰�ꂪ����܂��B
	<li>��ʂ�߂��ă{�^���������ƌ듮�삵�܂��̂Ő�΂ɔ����Ă��������B
	<li>�u���E�U�̍Ď��s(�����[�h)�{�^�����ʈړ��{�^�����͎g��Ȃ��ł��������B
	<li><b>���̓`�F�b�N�͂���܂���B�v�Z�Ɏg�p���鐔���Ȃǂ͊ԈႦ�Ȃ��悤�ɓ��͂��A�ҏW��͕K�����쎎�������Ă��������B</b>
	</ul><p>
	</BODY></HTML>
EOF
	if (-e $lockfile) { unlink($lockfile); }
	exit;
}

sub regist {

	local (@EDIT) = @_;

	if ($FORM{'action'} eq 'ADD') {

		@NEW = @BASE;
		$write = &EncodeCSV(@EDIT);
		if ($rev) { unshift(@NEW,"$write\n"); }
		else { push(@NEW,"$write\n"); }
	}
	else {
		foreach $num (0 .. $#BASE) {

			if ($num == $FORM{'action'} && $FORM{'action'} ne 'ADD') {

				$write = &EncodeCSV(@EDIT);
				$BASE[$num] = "$write\n";
			}
			push(@NEW,$BASE[$num]);
		}
	}

	if ($rev) { @NEW = reverse @NEW; }

	if (!open(OUT,"> $base_dir$file\.csv")) { &error("File Not Open","$file\.csv���J�����Ƃ��ł��܂���."); }

	$FORM{'head1'} =~ s/&amp;/&/g; $FORM{'head1'} =~ s/&quot;/"/g; $FORM{'head1'} =~ s/&lt;/</g; $FORM{'head1'} =~ s/&gt;/>/g;
	$FORM{'head2'} =~ s/&amp;/&/g; $FORM{'head2'} =~ s/&quot;/"/g; $FORM{'head2'} =~ s/&lt;/</g; $FORM{'head2'} =~ s/&gt;/>/g;
	$FORM{'head3'} =~ s/&amp;/&/g; $FORM{'head3'} =~ s/&quot;/"/g; $FORM{'head3'} =~ s/&lt;/</g; $FORM{'head3'} =~ s/&gt;/>/g;

	print OUT "$FORM{'head1'}\n";
	print OUT "$FORM{'head2'}\n";
	print OUT "$FORM{'head3'}\n";
	print OUT "\n";

	if ($rev) { print OUT @NEW; }
	if ($FORM{'action'} eq '-NEW-') {

		$write = &EncodeCSV(@EDIT);
		print OUT "$write\n";
	}
	if (!$rev) { print OUT @NEW; }
	close(OUT);

	if (!open(IN,"$base_dir$file\.csv")) { &error("File Not Open","$file\.csv���J�����Ƃ��ł��܂���."); }
	$head1 = <IN>;
	$head2 = <IN>;
	$head3 = <IN>;
	$head4 = <IN>;
	@BASE = <IN>;
	close(IN);

	if ($rev) { @BASE = reverse @BASE; }
}

sub EncodeCSV {

	local(@fields) = @_;
	local(@CSV) = ();

	foreach $text (@fields) {

		$text =~ s/&amp;/&/g;
		$text =~ s/&quot;/"/g;
		$text =~ s/&lt;/</g;
		$text =~ s/&gt;/>/g;

		$text =~ s/"/""/g;
		if ($text =~ /,|"/) { $text = "\"$text\""; }

		push(@CSV,$text);
	}

	return join(',',@CSV);
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

sub delete {

	local ($delete) = @_;

	foreach $num (0 .. $#BASE) {

		if ($num == $delete) { next; }
		push(@NEW,$BASE[$num]);
	}

	if ($rev) { @NEW = reverse @NEW; }

	if (!open(OUT,"> $base_dir$file\.csv")) { &error("File Not Open","$file\.csv���J�����Ƃ��ł��܂���."); }
	print OUT $head1;
	print OUT $head2;
	print OUT $head3;
	print OUT $head4;

	print OUT @NEW;
	close(OUT);

	if (!open(IN,"$base_dir$file\.csv")) { &error("File Not Open","$file\.csv���J�����Ƃ��ł��܂���."); }
	$head1 = <IN>;
	$head2 = <IN>;
	$head3 = <IN>;
	$head4 = <IN>;
	@BASE = <IN>;
	close(IN);

	if ($rev) { @BASE = reverse @BASE; }
	$FORM{'start'} = $FORM{'restart'};
}

sub input {

	print "Content-type: text/html\n\n";
	print <<"EOF";
	<html><head><title></title></head>
	<body>
	<h1>�F��</h1>
	<form method=POST action="edit.cgi">
	<input type=hidden name="file" value="$file">
	�p�X���[�h <input type=password name="ADMIN_KEY" value="" size=10>
	<input type=submit value="�F��">
	</form>
	�����i�ݒ�t�@�C�������������\\�ȃp�[�~�b�V�����ɐݒ肵�Ă����K�v������܂��B
	</body>
	</html>
EOF
exit;

}

sub lock {

	# ���b�N�����̎������� symlink()�D��
	$symlink_check = (eval { symlink("",""); }, $@ eq "");
	if (!$symlink_check) {

		$c = 0;
		while(-f "$lockfile") { # file��

			$c++;
			if ($c >= 3) { &error('���g���C�G���[','�������܍��G���Ă���\��������܂�.','�߂��Ă�����x���s���Ă݂Ă�������.'); }
			sleep(2);
		}
		open(LOCK,">$lockfile");
		close(LOCK);
	}
	else {
		local($retry) = 3;
		while (!symlink(".", $lockfile)) { # symlink��

			if (--$retry <= 0) { &error('���g���C�G���[','�������܍��G���Ă���\��������܂�.','�߂��Ă�����x���s���Ă݂Ă�������.'); }
			sleep(2);
		}
	}
}

sub error {

	local (@msg) = @_;
	local ($i);

	print "Content-type: text/html\n\n";
	print <<"EOF";
	<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN">
	<HTML>
	<HEAD>
	<TITLE>ERROR</TITLE>
	<SCRIPT language="JavaScript">
	<!--
	function PageBack(){ history.back(); }
	//-->
	</SCRIPT>
	</HEAD>
	<BODY>
	<h1>$_[0]</h1>
EOF

	foreach $i (1 .. $#msg) { print "$msg[$i]<br>\n"; }

	print <<"EOF";
	<h3>[<A HREF="JavaScript:history.back()">�O�̉��</A>]</h3>
	</BODY></HTML>
EOF
	if (-e $lockfile) { unlink($lockfile); }
	exit;
}
