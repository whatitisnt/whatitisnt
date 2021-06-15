#!/usr/bin/perl

require "./setup.pl";

#�����擾
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
@wday_array = ('SUN','MON','TUE','WED','THU','FRI','SAT');
$date_now = sprintf("%01d\/%01d(%s)%02d\:%02d",$mon +1,$mday,$wday_array[$wday],$hour,$min);

#�f�[�^�̓ǂݍ���
if ($ENV{'REQUEST_METHOD'} eq "POST") { read(STDIN,$buffer,$ENV{'CONTENT_LENGTH'}); }
else { $buffer = $ENV{'QUERY_STRING'}; }

@pairs = split(/&/,$buffer);
foreach $pair (@pairs) {

	($name, $value) = split(/=/, $pair);
	$name =~ tr/+/ /;
	$name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

	&jcode'convert(*name,'sjis');
	&jcode'convert(*value,'sjis');

	$value =~ s/</&lt;/g;
	$value =~ s/>/&gt;/g;
	$value =~ s/"/&quot;/g;
	$value =~ s/\t//g;

	if ($name eq '_ZAIKO') {

		push(@ZAIKO_KANRI,$value);
		($TARGET_FILE,$CODE,$KAZU) = split(/:/,$value,3);
		$ZAIKO_TARGET{$TARGET_FILE} = 1;
	}
	else {
		$in{$name} = $value;
		push(@out,"$name\0$value");
	}
}

if ($center) { $center1 = '<center>'; $center2 = '</center>'; }

if ($in{'_order'} =~ /\D/) { exit; }

if ($in{'_file'} eq '') { &error('�ݒ�G���[','�g�p���鏤�i�t�@�C�����ݒ肳��Ă��܂���B'); }
if (!-e "$base_dir$in{'_file'}\.csv") { &error('�ݒ�G���[',"���i�ݒ�t�@�C��$in{'_file'}��������܂���B"); }

$lockfile = $tmp_dir . "$in{'_file'}\.lock";

$od_check = (eval { opendir(DIR,$base_dir); }, $@ eq "");
if (!$od_check) { &error("�G���[","�t�@�C���ꗗ���擾�ł��܂���B"); }

($cookie_name,$els) = split(/\./,$in{'_file'},2);
@newls = ();

@list = readdir(DIR); # �t�@�C�����̒��o

foreach $file (@list) {

	next if -d $file;

	if ($file =~ /^$cookie_name\./) {

		#���i�ݒ�t�@�C�����J��(�戵���i�f�[�^��ǂݍ���)
		if (!open(FILE,"$base_dir$file")) { &error('�G���[',"���i�t�@�C��$file���ǂݏo���܂���B"); }

		#�t�@�C���n���h��'FILE'����P�s���f�[�^��ǂ�
		while (<FILE>) {

			#����
			s/\t//g;
			s/\n//g;

			#�s�����V���[�v�܂��͋�s�̏ꍇ�͎���
			if (/^#/) { next; }
			if (/^$/) { next; }

			#�f�[�^���o
			($code,$name,$tanka,$tax,$rem,$url,$zaiko,$type) = &DecodeCSV($_);

			$name{$code} = $name;
			$tanka =~ s/\,//g; $tanka =~ s/\\//g; $tanka{$code} = $tanka;
			$taxrate = $tax;
			$rem{$code} = $rem;
			$url{$code} = $url;
			$zaiko{$code} = $zaiko;
			$type{$code} = $type;

			if ($taxrate == -3) { $taxm{$code} = "(�ō�)"; }
			elsif ($taxrate == -2) { $taxm{$code} = "(�s�ې�)"; }
			elsif ($taxrate == -1) { $taxm{$code} = "(��ې�)"; }
			else { $taxm{$code} = ""; }

			if ($taxrate =~ /\-/) { $taxrate = 0; } # �ł̐ݒ�l��-�������0%�ɂ���
			$tax{$code} = $taxrate;
		}
		close(FILE);
	}
}

close(DIR);

#���i�R�[�h���L�[�Ƃ���%order�ɐ��ʂ��i�[
while (($key,$val) = each %in) {

	if ($key =~ /X(.+)X/) { $code = $1; }

	#�폜���鏤�i�R�[�h���擾
	if ($in{'_action'} eq 'delete') {

		if ($key =~ /X(.+)X/) { $delete_id = $1; last; }
	}
	#���i�R�[�h������̌`���œ��͂���A���ʂ�0�ȊO�̐������w�肳��Ă���ꍇ�ɏ���
	elsif ($val =~ /\d+/ && $val != 0) {

		if ($key =~ /X(.+)X/) {

			$code = $1;
			if ($name{$code} eq '') { &error("�G���[","���i�R�[�h$code�����i�ݒ�t�@�C��$in{'_file'}�ɑ��݂��Ă��Ȃ��\\��������̂őI���ł��܂���B","�Ǘ��҂ɂ��₢���킹���������B"); }
			$w = 1; $order{$code} = $val;
		}
	}
	elsif ($key =~ /X(.+)X/ && $val =~ /\D/) { &error("�G���[","���i�R�[�h$code�̐��ʂ����p�����ȊO�Ŏw�肳��Ă��܂��B","���p�����œ��͂��Ă��������B"); }
}

#�N�b�L�[�̎擾
$cookies = $ENV{'HTTP_COOKIE'};

@pairs = split(/;/,$cookies);
foreach $pair (@pairs) {

	($key,$val) = split(/=/,$pair,2);
	$key =~ s/ //g;

	if ($key eq $cookie_name) {

		@pairs = split(/,/,$val);
		foreach $pair (@pairs) {

			($key,$val) = split(/:/,$pair,2);
			$COOKIE{$key} = $val;
		}
		last;
	}
}

#�폜����
if ($in{'_action'} eq 'delete') {

	#�o�X�P�b�g�t�@�C�����J��
	if (!open(ORDER,"$tmp_dir$in{'_order'}\.bkt")) { &error("�����I������Ă��܂���B"); }
	@base = <ORDER>;
	close(ORDER);

	@new = grep(!/^.+\t($delete_id)\t/,@base);

	if (!@new) { $delall = 1; unlink "$tmp_dir$in{'_order'}\.bkt"; }
	else {
		if (!open(FILE,"> $tmp_dir$in{'_order'}\.bkt")) { &error("�ݒ�G���[","�o�X�P�b�g�t�@�C���ɍċL�^�ł��܂���B"); }
		print FILE @new;
		close(FILE);
	}
}

#�����t�H�[��
elsif ($in{'_action'} eq 'mailform') { &mailform; }

#���M�t�H�[��
elsif ($in{'_action'} eq 'mail') { &mail; }

#�o�^����
elsif ($w) {

	if ($COOKIE{'OrderNo'} eq '') {

		$COOKIE{'OrderNo'} = sprintf("%04d%02d%02d%02d%02d%02d",$year +1900,$mon +1,$mday,$hour,$min,$sec);

		#�V�K����
		if (!open(FILE,"> $tmp_dir$COOKIE{'OrderNo'}\.bkt")) { &error("�ݒ�G���[","��ƃf�B���N�g�����������ݒ肳��Ă��܂���B"); }
	}
	else {
		#�ǉ�����
		if (!open(FILE,">> $tmp_dir$COOKIE{'OrderNo'}\.bkt")) { &error("�ݒ�G���[","��ƃf�B���N�g�����������ݒ肳��Ă��܂���B"); }
	}

	#���i�R�[�h�Ɛ��ʂ��t�@�C���ɋL�^
	while (($code,$kazu) = each %order) { print FILE "$in{'_file'}\t$code\t$kazu\n"; }

	close(FILE);
	chmod(0666,"$tmp_dir$COOKIE{'OrderNo'}\.bkt");
}

#�o�X�P�b�g�ꎞ�t�@�C���̈ꗗ
$od_check = (eval { opendir(DIR,$tmp_dir); }, $@ eq "");
if (!$od_check) { &error("�G���[","opendir()�ɒv���I�ȃG���[���������܂����B"); }
@ls = readdir(DIR);
close(DIR);

#�c�������ꎞ�t�@�C�����폜
($secg,$ming,$hourg,$mdayg,$mong,$yearg,$wdayg,$ydayg,$isdstg) = gmtime(time - 2*24*60*60);
$limit = sprintf("%04d%02d%02d%02d%02d%02d",$yearg +1900,$mong +1,$mdayg,$hourg,$ming,$secg);

foreach $file (@ls) {

	next if $file eq '.';
	next if $file eq '..';
	next if -d $file;
	if ($file =~ /(\d+)\.bkt/) { if ($1 < $limit) { unlink "$tmp_dir$file"; }}
}

#�Z�b�g����N�b�L�[�̓��e
if ($delall) { $set_cookie = ""; }
else { $set_cookie = "OrderNo\:$COOKIE{'OrderNo'}"; }

#���ʃN�b�L�[�̐ݒ�
print "Set-Cookie: $cookie_name=$set_cookie\n";

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
$body
$center1
$title
EOF

#�o�X�P�b�g�t�@�C�����J��
if (open(ORDER,"$tmp_dir$COOKIE{'OrderNo'}\.bkt")) {

	print <<"EOF";
	<table><tr><td>$msg_top</td></tr></table>
	<form method=POST action="cargo.cgi">
	<table border="1" bordercolor="#FFFFFF" cellspacing="0" cellpadding="4">
	<tr>
	<th><font size=+1></font>�@</th>
	<th align=left><font size=+1>TOP SIDE</font></th>
	<th align=left><font size=+1>BOTTOM SIDE</font></th>
	<th><font size=+1>�P��(�~)</font></th>
	<th><font size=+1>����(�{)</font></th>
EOF
	if ($taxps) { #����ł���������ꍇ

		print <<"EOF";
		<th><font size=+1>�ŕʌv(�~)</font></th>
		<th><font size=+1>�����(�~)</font></th>
		<th><font size=+1>�ō��v(�~)</font></th>
EOF
	}
	else {
		print <<"EOF";
		<th><font size=+1>���v(�~)</font></th>
EOF
	}

	print <<"EOF";
	<th><font size=+1>���</font></th>
	</tr>
EOF
	#�W�v
	&cal1;

	foreach $code (sort keys %list) { # ���i�R�[�h��
#	foreach $code (sort { $list{$b} <=> $list{$a} } keys %list) { # ���ʂ�������

		#�W�v
		&cal2;

		#���i���Ɣ��l���̃R���������s�ɕϊ�
		$name{$code} =~ s/\:/<br>/g;
		$rem{$code} =~ s/\:/<br>/g;

		$zaiko_mes = '';
		if ($zaiko{$code} ne '') {

			if ($zaiko{$code} == 0) { $zaiko_err = 1; $zaiko_mes = '<br><font size=-1>�݌ɖ����I(��U������ĉ�����)</font>'; }
			if ($list{$code} > $zaiko{$code}) { $zaiko_err = 1; $zaiko_mes = '<br><font size=-1>�݌ɕs���I(��U������ĉ�����)</font>'; }
		}

		$c++;
		if ($c % 2) { $bg = "#ffeedd"; } else { $bg = "#ffffff"; } #�P�s�����ɃZ���̔w�i�F��ւ���

		print <<"EOF";
		<tr>
		<td align=left><font color="#ffe600">$code</font></td>
		<td align=left><font color="#ffe600">$rem{$code}</font></td>
		<td align=left><font color="#ffe600">$name{$code}</font></td>
		<td align=right><font color="#ffe600">$tanka2</font></td>
		<td align=right><font color="#ffe600">$kazu2$zaiko_mes</font></td>
EOF
		if ($tax == 0) { $tax2 = ""; } # ����ŗ���0%�̏ꍇ�͕\�����Ȃ�

		if ($taxps) {

			print <<"EOF";
			<td align=right><font color="#ffe600">$kei2</font></td>
			<td align=right><font color="#ffe600" size=-1>$taxm{$code}</font> <font color="#ffe600">$tax2</font></td>
EOF
		}

		print <<"EOF";
		<td align=right><font color="#ffe600">$kei2_and_tax</font></td>
		<td><input type=submit name="X$code\X" value="���"></td>
		</tr>
EOF
	}

	close(ORDER);

	$taxs = int($taxs);
	$gokei = int($gokei);

	#���J���}�}������
	1 while $keis =~ s/(.*\d)(\d\d\d)/$1,$2/g;
	1 while $gokei =~ s/(.*\d)(\d\d\d)/$1,$2/g;
	1 while $taxs =~ s/(.*\d)(\d\d\d)/$1,$2/g;
	1 while $kazu =~ s/(.*\d)(\d\d\d)/$1,$2/g;

	print <<"EOF";
	<tr>
	<td colspan=4 align=center><font size=-1>$message1</font></td>
	<td align=right><font color="#ffe600"><strong>$kazuall</strong></font></td>
EOF
	if ($taxps) {

		print <<"EOF";
		<td align=right><font color="#ffe600"><strong>$keis</strong></font></td>
		<td align=right><strong>$taxs</strong></td>
EOF
	}

	print <<"EOF";
	<td align=right><strong><font size=+1>$gokei</font></strong></td>
	<td>$taxmes</td>
	</tr>
	</table>
	<input type=hidden name="_file" value="$in{'_file'}">
	<input type=hidden name="_order" value="$COOKIE{'OrderNo'}">
	<input type=hidden name="_action" value="delete">
	<p>
	</form>
	<p>
	<table><tr><td>$msg_btm</td></tr></table>
EOF
	if ($zaiko_err) {

		print <<"EOF";
		<h3>�݌ɕs���̏��i���I������Ă���̂Œ����ł��܂���B</h3>
EOF
	}
	else {
		print <<"EOF";
		<form method=POST action="cargo.cgi">
		<input type=hidden name="_file" value="$in{'_file'}">
		<input type=hidden name="_order" value="$COOKIE{'OrderNo'}">
		<input type=hidden name="_action" value="mailform">
		<input type="image" src="../../cargoimg/chuumon.gif" border="0">
		</form>
EOF
	}
}
else { print "<h3>�����I������Ă��܂���B</h3>\n"; }

print <<"EOF";
<hr><p>
<A HREF="javascript:window.close()"><img src="../../cargoimg/mae.gif" border="0"></A>
<A HREF="cargo.cgi?_file=$in{'_file'}"><img src="../../cargoimg/saishin.gif" border="0"></A>
<A HREF="search.cgi\?file=$in{'_file'}"><img src="../../cargoimg/ichiran.gif" border="0"></A>
$center2
</body></html>
<!-- $COOKIE{'OrderNo'} -->
EOF

exit;

sub cal1 {

	#�������i������΍��Z����
	foreach (<ORDER>) {

		s/\n//;
		($target_file,$code,$kazu) = split(/\t/,$_,3);
		$list{$code} += $kazu;
		$target_file{$code} = $target_file;
	}
}

sub cal2 {

	#�v�����ʁ~�P��
	$kei = $kei2 = $list{$code} * $tanka{$code};
	1 while $kei2 =~ s/(.*\d)(\d\d\d)/$1,$2/g;

	$kazu2 = $list{$code};
	$tanka2 = $tanka{$code};
	1 while $kazu2 =~ s/(.*\d)(\d\d\d)/$1,$2/g;
	1 while $tanka2 =~ s/(.*\d)(\d\d\d)/$1,$2/g;

	if ($taxps) {

		#�Ł��v�~�ŗ���100
		$tax = $kei * $tax{$code} / 100;
		$tax2 = int($tax);
		1 while $tax2 =~ s/(.*\d)(\d\d\d)/$1,$2/g;

		#�ō��v���v�{��
		$kei_and_tax = $kei + $tax;
		$kei2_and_tax = int($kei_and_tax);
	}
	else { $kei_and_tax = $kei2_and_tax = $kei; $taxmes = '(�ō�)'; }

	1 while $kei2_and_tax =~ s/(.*\d)(\d\d\d)/$1,$2/g;

	#���Z
	$keis += $kei;
	$gokei += $kei_and_tax;
	$taxs += $tax;
	$kazuall += $list{$code};
}

sub mailform {

	#�K��̔��@�ł̍L���\���`�������t�@�C�����J��
	if (!open(FILE,"$base_dir$hanbai")) { &error('�G���[',"�K��̔��@�ł̍L���\���`�������t�@�C�����ǂݏo���܂���B"); }
	@HANBAI = <FILE>;
	close(FILE);

	#�󒍃t�H�[���t�@�C�����J��
	if (!open(FILE,"$base_dir$juchu")) { &error('�G���[',"�󒍃t�H�[���t�@�C�����ǂݏo���܂���B"); }
	@JUCHU = <FILE>;
	close(FILE);

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
	$body
	$center1
	<h2>�������t�H�[��</h2>
EOF

	#�o�X�P�b�g�t�@�C�����J��
	if (open(ORDER,"$tmp_dir$COOKIE{'OrderNo'}\.bkt")) {

		print <<"EOF";
		<form method=POST action="cargo.cgi" name="kounyu">
		<table border="1" bordercolor="#FFFFFF" cellspacing="0" cellpadding="4">
		<tr>
		<th><font size=+1></font>�@</th>
		<th align=left><font size=+1>TOP SIDE</font></th>
		<th align=left><font size=+1>BOTTOM SIDE</font></th>
		<th><font size=+1>�P��(�~)</font></th>
		<th><font size=+1>����(�{)</font></th>
EOF
		#����ł���������ꍇ
		if ($taxps) {

			print <<"EOF";
			<th><font size=+1>�ŕʌv(�~)</font></th>
			<th><font size=+1>�����(�~)</font></th>
			<th><font size=+1>�ō��v(�~)</font></th>
EOF
		}
		else {
			print <<"EOF";
			<th><font size=+1>���v(�~)</font></th>
EOF
		}

		print <<"EOF";
		</tr>
EOF
		#�W�v
		&cal1;

		foreach $code (sort keys %list) { # ���i�R�[�h��
#		foreach $code (sort { $list{$b} <=> $list{$a} } keys %list) { # ���ʂ�������

			#�W�v
			&cal2;

			#���i���Ɣ��l���̃R�������X�y�[�X�ɕϊ�
			$name{$code} =~ s/\:/ /g;
			$rem{$code} =~ s/\:/ /g;

			#�݌ɊǗ��Ώۃf�[�^
			if ($zaiko{$code} =~ /\d/ && $zaiko{$code} > 0) { print "<input type=hidden name=\"_ZAIKO\" value=\"$target_file{$code}:$code:$list{$code}\">\n"; }

			$c++;
			if ($c % 2) { $bg = "#ffeedd"; } else { $bg = "#ffffff"; } #�P�s�����ɃZ���̔w�i�F��ւ���

			print <<"EOF";
			<tr>
			<td align=left>$code</td>
			<td align=left>$rem{$code}</td>
			<td align=left>$name{$code}</td>
			<td align=right>$tanka2</td>
			<td align=right>$kazu2</td>
			<input type=hidden name="ORDER" value="��$code $name{$code}">
EOF
			if ($mailrem) { print "<input type=hidden name=\"ORDER\" value=\"$rem{$code}\">\n"; }

			if ($taxps) {

				if ($tax == 0) { $tax2 = ""; } # ����ŗ���0%�̏ꍇ�͕\�����Ȃ�

				print <<"EOF";
				<td align=right>$kei2</td>
				<td align=right><font size=-1>$taxm{$code}</font> $tax2</td>
				<input type=hidden name="ORDER" value="\@$tanka2�~�~$kazu2��$kei2�~.">
EOF
			}
			else {

				print <<"EOF";
				<input type=hidden name="ORDER" value="\@$tanka2�~$kazu2��$kei2_and_tax\.">
EOF
			}

			print <<"EOF";
			<td align=right>$kei2_and_tax</td>
			</tr>
EOF
		}

		close(ORDER);

		$taxs = int($taxs);
		$gokei = int($gokei);

		#�J���}�}������
		1 while $keis =~ s/(.*\d)(\d\d\d)/$1,$2/g;
		1 while $gokei =~ s/(.*\d)(\d\d\d)/$1,$2/g;
		1 while $taxs =~ s/(.*\d)(\d\d\d)/$1,$2/g;
		1 while $kazu =~ s/(.*\d)(\d\d\d)/$1,$2/g;

		print <<"EOF";
		<tr>
		<th colspan=4><font size=-1 align=center>���������v ��</font></th>
		<td align=right><font color="#ffe600"><strong>$kazuall</strong></font></td>
EOF
		if ($taxps) {

			print <<"EOF";
			<input type=hidden name="�����" value="$taxs�~">
			<td align=right><strong>$keis</strong></td>
			<td align=right><strong>$taxs</strong></td>
EOF
		}

		print <<"EOF";
		<td align=right><font color="#ffe600">$taxmes</font> <strong><font color="#ffe600" size=+1>$gokei</font></strong></td>
		</tr>
		</table>
		<input type=hidden name="_file" value="$in{'_file'}">
		<input type=hidden name="_order" value="$COOKIE{'OrderNo'}">
		<input type=hidden name="_action" value="mail">
		<p>
		<input type=hidden name="���v" value="$gokei�~ $taxmes">
		<table><tr><td>
EOF
		foreach (@JUCHU) { print; }

		print <<"EOF";
		</td></tr></table>
		</form>
EOF
	}
	else { print "<h3>�����I������Ă��܂���B</h3>\n"; }

	print <<'EOF';
	<br><h3>�s�K��̔��@�ł̍L���\���`���������t</h3>
EOF
	print "<form><textarea cols=80 rows=10>";
	foreach (@HANBAI) { print; }

	#if ($reg_name eq '' || $reg_code eq '') { $reg = "���o�^"; }
	#else { $reg = "$reg_name �o�^�R�[�h�F$reg_code"; }

	#print "\n"; #���폜���Ȃ����ƁB
	#print '�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q�Q' . "\n";
	#print "�V���b�s���O�o�X�P�b�g�V�X�e���E�v�� (c)www.rescue.ne.jp\n";
	#print "�V�F�A�E�G�A�o�^�F$reg\n";
	print "</textarea></form><p>\n";

	print <<"EOF";
	<hr><p>
	<A HREF="JavaScript:history.back()"><img src="../../cargoimg/mae.gif" border="0"></A>
	<A HREF="$top"><img src="../../cargoimg/menu.gif" border="0"></A>
	$center2
	</body></html>
EOF
	exit;
}

#���[�����M����
sub mail {

	unless ($in{'_EMAIL'} =~ /\b[-\w.]+@[-\w.]+\.[-\w]+\b/) { &error('���L��������܂��B','�d���[���͔��p�Ő��������L�����������B'); }

	#�݌ɊǗ�

	&lock;

	foreach $zaiko_file (keys %ZAIKO_TARGET) {

		@NEW = ();

		if (!open(IN,"$base_dir$zaiko_file\.csv")) { &error('�G���[',"$zaiko_file���I�[�v���ł��܂���B"); }
		@lines = <IN>;
		close(IN);

		foreach $line (@lines) {

			$line =~ s/\n//g;
			$zaiko = '';

			#�f�[�^���o
			($code,$name,$tanka,$tax,$rem,$url,$zaiko,$type) = &DecodeCSV($line);

			if ($zaiko =~ /\d+/ && $zaiko ne '') {

				foreach $target (@ZAIKO_KANRI) {

					($TARGET_FILE,$CODE,$KAZU) = split(/:/,$target,3);

					$old = $zaiko;
					if ($CODE eq $code && $zaiko == 0) { &error("�݌ɃG���[","���i�R�[�h$code�̏��i�͍݌ɂ������Ȃ�܂����B",'��ʂ�߂��ē��Y���i���폜���Ă��������B'); }
					if ($CODE eq $code) { $zaiko = $zaiko - $KAZU; }
					if ($zaiko < 0) { &error("�݌ɃG���[","���i�R�[�h$code�̏��i���݌ɐ�($old)�����鐔($KAZU)�����I������Ă��܂��B",'��ʂ�߂��ē��Y���i���폜���Ă���A���߂ď��i�����I�����������B'); }
				}

				push(@EDIT,$code);
				push(@EDIT,$name);
				push(@EDIT,$tanka);
				push(@EDIT,$tax);
				push(@EDIT,$rem);
				push(@EDIT,$url);
				push(@EDIT,$zaiko);
				push(@EDIT,$type);
				$write = &EncodeCSV(@EDIT);
				@EDIT = ();
			}
			else { $write = $line; }

			push(@NEW,"$write\n")
		}

		if ($viewzaiko) {

			if (!open(OUT,"> $base_dir$zaiko_file\.csv")) { &error('�G���[',"$zaiko_file���I�[�v���ł��܂���B"); }
			print OUT @NEW;
			close(OUT);
		}

		if (-e $lockfile) { unlink($lockfile); }
	}

	$| = 1;

	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};
	if ($host eq '') { $host = $addr; }
	if ($host eq $addr) { $host = gethostbyaddr(pack('C4',split(/\./,$host)),2) || $addr; }

	if ($hiho) {

		$in{'_SUBJECT'} = "\[$in{'_order'}\] Mail Order";
		if (!open(OUT,"| $sendmail -s \"$in{'_SUBJECT'}\" -f \"$in{'_EMAIL'}\" $mailto")) { &error('Error'); }
	}
	else {
		if (!open(OUT,"| $sendmail -t")) { &error('Error'); }

		print OUT "X-Processed: $date_now\n";
		print OUT "X-Mailer: SHPPING CARGO PRO by www.rescue.ne.jp $reg_code\n";
		print OUT "X-HTTP-REFERER: $ENV{'HTTP_REFERER'}\n";
		print OUT "To: $mailto\n";
		print OUT "From: $in{'_EMAIL'}\n";
		print OUT &jis("Subject: \[$in{'_order'}\] $in{'_SUBJECT'}\n");
		print OUT "\n";
	}

	foreach (@out) {

		($name,$value) = split("\0");

		#���[���p�Ƀ^�O�ϊ�
		$value =~ s/&amp;/&/g;
		$value =~ s/&quot;/"/g;
		$value =~ s/&lt;/</g;
		$value =~ s/&gt;/>/g;
		if ($value =~ /(\.)$/) { $value =~ s/\./\n/; }

		if ($name eq 'ORDER' && $value ne '') { print OUT &jis("$value\n"); }
		elsif ($name eq 'ORDER' && $value eq '') { next; }
		elsif ($name eq '_EMAIL') { print OUT &jis("[�d���[��]\n$value\n\n"); }
		elsif ($name =~ /^\_/) { next; }
		else { print OUT &jis("[$name]\n$value\n\n"); }
	}

	print OUT "\n";
	print OUT "Sender Information >>\n";
	print OUT "X-HTTP-User-Agent: $ENV{'HTTP_USER_AGENT'}\n";
	print OUT "X-Remote-host: $host\n";
	print OUT "X-Remote-Addr: $ENV{'REMOTE_ADDR'}\n";
	close(OUT);

	#�ꎞ�t�@�C���̍폜
	unlink "$tmp_dir$in{'_order'}\.bkt";

	#-------------------->

	#���ʃN�b�L�[�̐ݒ�(�󏑍�)
	print "Set-Cookie: $cookie_name=\n";

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
	$body
	$center1
	<table><tr><td>$msg_sended</td></tr></table>
	<p>
EOF
	print "<form>\n";
	print "<textarea cols=70 rows=20>";

	print "������ $date_now\n";
	print "��t�ԍ� $in{'_order'}\n";
	print "�₢���킹�� $mailto\n\n";

	foreach (@out) {

		($name,$value) = split("\0");
		if ($value =~ /(\.)$/) { $value =~ s/\./\n/; }

		if ($name eq 'ORDER' && $value ne '') { print "$value\n"; }
		elsif ($name eq 'ORDER' && $value eq '') { next; }
		elsif ($name eq '_EMAIL') { print "[�d���[��]\n$value\n\n"; }
		elsif ($name =~ /^\_/) { next; }
		else { print "[$name]\n$value\n\n"; }
	}

	print "</textarea></form><p>\n";

	if ($resp) {

		sleep(1);

		if ($hiho) {

			$in{'_SUBJECT'} = "\[$in{'_order'}\] Mail Order (COPY)";
			open(OUT,"| $sendmail -s \"$in{'_SUBJECT'}\" -f \"$mailto\" $in{'_EMAIL'}");
		}
		else {
			open(OUT,"| $sendmail -t");

			print OUT "X-Processed: $date_now\n";
			print OUT "X-Mailer: SHPPING CARGO PRO by www.rescue.ne.jp $reg_code\n";
			print OUT "X-HTTP-REFERER: $ENV{'HTTP_REFERER'}\n";
			print OUT "To: $in{'_EMAIL'}\n";
			print OUT "From: $mailto\n";
			print OUT &jis("Subject: \[$in{'_order'}\] $in{'_SUBJECT'} (�ʂ�)\n");
			print OUT "\n";
		}

		print OUT &jis("$head\n");

		foreach (@out) {

			($name,$value) = split("\0");

			#���[���p�Ƀ^�O�ϊ�
			$value =~ s/&amp;/&/g;
			$value =~ s/&quot;/"/g;
			$value =~ s/&lt;/</g;
			$value =~ s/&gt;/>/g;
			if ($value =~ /(\.)$/) { $value =~ s/\./\n/; }

			if ($name eq 'ORDER' && $value ne '') { print OUT &jis("$value\n"); }
			elsif ($name eq 'ORDER' && $value eq '') { next; }
			elsif ($name eq '_EMAIL') { print OUT &jis("[�d���[��]\n$value\n\n"); }
			elsif ($name =~ /^\_/) { next; }
			else { print OUT &jis("[$name]\n$value\n\n"); }
		}

		print OUT &jis("$sign\n");

		close(OUT);
	}

	print <<"EOF";
	<p>
	<table><tr><td>$msg_sended2</td></tr></table><p>
	<hr><p>
	<A HREF="JavaScript:history.back()"><img src="../../cargoimg/mae.gif" border="0"></A>
	<A HREF="$end"><img src="../../cargoimg/menu.gif" border="0"></A>
	$center2
	</body></html>
EOF

exit;

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

sub error {

	local (@msg) = @_;
	local ($i);

	if (-e $lockfile) { unlink($lockfile); }

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
	$body
	$center1
	<h1>$_[0]</h1>
	<table><tr><td>
EOF
	foreach $i (1 .. $#msg) { print "$msg[$i]<br>\n"; }

	print <<"EOF";
	</td></tr></table>
	<h3>[<A HREF="JavaScript:history.back()">�߂�</A>]</h3>
	$center2
	</body></html>
EOF
	exit;
}

sub jis {

	local($msg) = @_;
	&jcode'convert(*msg,'jis');
	return $msg;
}
