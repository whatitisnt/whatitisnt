#!/usr/bin/perl
#**************************************************************************
#
#    easyaccess.cgi Easy Access Ver1.13
#    Created on: 98/12/25 Modified 00/11/13
#   (C) Copyright 1998-2000 by Tomey(Tomio Sato)
#    http://www.pmcj.com/   info@pmcj.com
#    http://www.web-purpose.com/PMC/   info@web-purpose.com
#
#�@�����p�K�񔲐�
#  1.�����̗L���ɂ�����炸���̃X�N���v�g�̍Ĕz�z�E�����^���E�̔��y�ё�s�ݒu�T�|�r�X�͋֎~�������܂��B
#  2.�X�N���v�g���p�ɂ�邢���Ȃ��Q�⑹�Q�Ȃǂ����͈�؂̐ӔC�𕉂��܂���B���ׂĎ��Ȃ̐ӔC�ɂ����Ă����p�������B
#  
#**************************************************************************
#�l�ݒ�
#**************************************************************************
#
#�^�C�g�����̎w��
$title = '�����@�A�N�Z�X��́@����';
#
$refken = '0';	#�����N�������ŉ����ȉ���\�������Ȃ����w��B�ꌏ�ł��\��������ꍇ�u0�v
$hosken = '0';	#�z�X�g�����ŉ����ȉ���\�������Ȃ����w��B�ꌏ�ł��\��������ꍇ�u0�v
$ageken = '0';	#�u���E�U�����ŉ����ȉ���\�������Ȃ����w��B�ꌏ�ł��\��������ꍇ�u0�v
#
#�f�[�^�[�֘A�t�@�C�����[�g
#�ucount.dat�v�ugekan.dat�v�u���scv�t�@�C���v�̊i�[�f�B���N�g���[�w��ł��B
$dateroot = './';
#
#�J�E���g�L�^�t�@�C����
$countdate = $dateroot . "count.dat";
#���ԃJ�E���g�L�^�t�@�C����(���ӁFgekan.dat�͎����I�ɍ쐬����܂��B)
$gekandate = $dateroot . "gekan.dat";
#�O���t�摜�t�@�C��
$bar = 'bar.gif';
$bar2 = 'bar2.gif';	#�T�ԁA���ԗp�摜�t�@�C��
#
#
$maskey = 'on';	#�}�X�^�[�L�[���g���ĉ{������ꍇ�uon�v�łȂ��ꍇ�uoff�v
$mpass = '2001';	#�}�X�^�[�L�[
#
#�C�O�T�[�o�[�����ݒ�(�u1�v= �}�C�i�X�X���ԁA�u2�v= �v���X�X����)
$timeche = '0';
#
#**************************************************************************
#�l�ݒ�͂����܂�
#**************************************************************************

	print "Content-type: text/html\n\n";
	print "<html><head><meta http-equiv=Content-Typecontent=text/html; charset=x-sjis>\n";
	print "<title>$title</title>\n";
	print "</head>\n";
	print "<body bgcolor=\"#ffffff\" text=\"#000000\" link=\"#000000\" alink=\"#ff0000\" vlink=\"#777777\">\n";
	print "<p align=center><center>\n";
	print "<br><h1>$title</h1>\n";

#**************************************************************************

&method;

	if($timeche eq "1"){ $timec = time - 9*60*60; }
	elsif ($timeche eq "2"){ $timec = time + 9*60*60; }
	else { $timec = time; }

$f_mod = $FORMIN{'mode'};

if($maskey eq "on" && $FORMIN{'maspass'} ne "$mpass"){ &passche; }
else {
	if($f_mod eq "yes"){ $btim = 1;&timeget2;$acssdate = $acss2; }
	elsif($f_mod eq "today"){ &timeget1;$acssdate = $acss; }
	else{ &massehtml($no = 2); }
}
#**************************************************************************

	&fileread;
	($monc,$day,$today,$yes,$gekan,$count) = split(/\,/,$ACDATE[0]);


	print "<hr size=3 width=90%><b>$TIME</b>\n";
	print "<hr size=1 width=60%><p>\n";
	print "<table width=85%><tr><td width=50%>\n";
	print "<font color=#777744>��<b></font> <a href=#1>���ԑуA�N�Z�X����</a>\n";
	if($f_mod eq "today"){
	print "<br><font color=#777744>��<b></font> <a href=#2>�T�ԃA�N�Z�X����</a>\n";
	print "<br><font color=#777744>��<b></font> <a href=#3>���ԃA�N�Z�X����</a>\n";
	}
	print "<br><font color=#777744>��<b></font> <a href=#4>�����N������</a>\n";
	print "<br><font color=#777744>��<b></font> <a href=#5>�z�X�g����</a>\n";
	print "<br><font color=#777744>��<b></font> <a href=#6>�u���E�U����</a>\n";
	print "</td><td width=50%><b>���݂̑����J�E���g<br>�@�@<font size=4 color=#ff0000>�� $count ��</font></b><br><br>\n";
	print "<b>�������݂܂ł̖K���</b> �y<font color=#ff0000>$today</font>�z<br><b>����̖K���</b>�y<font color=ff0000>$yes</font>�z\n";
	print "</td></tr></table>\n";
	print "<a name=1></a>\n";
	print "<br><hr size=3 width=80%>\n";
	if($f_mod eq "today"){
	print "<form action=./easyaccess.cgi?mode=yes method=POST>\n";
	print "<font size=4>�� <b>�{���̒�������</b> ��</font>\n";
	print "<input type=hidden name=maspass value=\"$FORMIN{'maspass'}\">\n";
	print "<input type=hidden name=mode value=\"yes\">\n";
	print "�@<input type=submit value=\"�@����̌��ʁ@\">\n";
	} else {
	print "<form action=./easyaccess.cgi?mode=today method=POST>\n";
	print "<input type=hidden name=maspass value=\"$FORMIN{'maspass'}\">\n";
	print "<input type=hidden name=mode value=\"today\">\n";
	print "<input type=submit value=\"�@�{���̌��ʁ@\">\n";
	print "�@<font size=4>�� <b>����̒�������</b> ��</font>\n";
	}
	print "<hr size=3 width=80%></form></p><p>\n";
	&fileacss;
	$c = 0;
	foreach $line (@AADATE) {
	($hour,$ref,$host,$agen,$yobi) = split(/\,/,$line);
	$c++;
		if($ref){ push(@refdat,$ref);$res++; }
		if($host){ push(@hostdat,$host);$hss++; }
		if($agen){ push(@agendat,$agen);$ags++; }
		if($hour){ push(@hourdat,$hour); }
		}

	for (@hourdat) { $hour{$_}++; }
	for (@refdat) { $ref{$_}++; }
	for (@hostdat) { $host{$_}++; }
	for (@agendat) { $agen{$_}++; }
	$houc = @hourdat;$refc = @refdat;$hosc = @hostdat;$agec = @agendat;

	print "<font color=#555555 size=5>��������<b>�@���ԑуA�N�Z�X�����@</b>��������</font>\n";
	print "<br>�S����$c��\n";
	print "<table border=1 width=85% cellpadding=2>\n";
	print "<tr bgcolor=#eeeebb><th nowrap width=20%>����</th><th nowrap colspan=2 width=70%>����</th><th nowrap width=10%>(����)</th></tr>\n";
	@hours = sort keys(%hour);
	foreach $hourkey (@hours) {
	$pur = ($hour{$hourkey} / $c) * 100;$pur = sprintf("%.1f",$pur);
	print "<tr><th nowrap bgcolor=#cccccc>$hourkey ��</td><td nowrap bgcolor=#333333 align=center width=5%><font color=00ff00><b>$hour{$hourkey}</b></font></td><td nowrap bgcolor=#555555 width=65%><img src=\"$bar\" width=$pur\% height=10></td><td nowrap width=10% align=center bgcolor=#ffffe7>($pur\%)</th></tr>\n";
	}
	print "</table></p>\n";

if($f_mod eq "today"){

	$dc = 1;
	foreach $lines (@ACDATE) { 
	($monc,$day,$today,$yes,$gekan,$count) = split(/\,/,$lines);
		$day = $day - 1;
		if($day eq "0"){
		$btim = $dc;&timeget2;$day = $mday;
		}
		if($yes){ push(@yesdat,$yes); }
		if($day){ push(@daydat,$day); }
	$dc++;
	}

	&timeget1;


	$yesc = $yesdat[0] + $yesdat[1] + $yesdat[2] + $yesdat[3] + $yesdat[4] + $yesdat[5] + $yesdat[6];
	if($yesdat[0] ne ""){ $cpur0 = ($yesdat[0] / $yesc) * 100;$cpur0 = sprintf("%.2f",$cpur0) * 2; } else { $cpur0 = 0;$yesdat[0] = 0;$daydat[0] = "�H";}
	if($yesdat[1] ne ""){ $cpur1 = ($yesdat[1] / $yesc) * 100;$cpur1 = sprintf("%.2f",$cpur1) * 2; } else { $cpur1 = 0;$yesdat[1] = 0;$daydat[1] = "�H"; }
	if($yesdat[2] ne ""){ $cpur2 = ($yesdat[2] / $yesc) * 100;$cpur2 = sprintf("%.2f",$cpur2) * 2; } else { $cpur2 = 0;$yesdat[2] = 0;$daydat[2] = "�H"; }
	if($yesdat[3] ne ""){ $cpur3 = ($yesdat[3] / $yesc) * 100;$cpur3 = sprintf("%.2f",$cpur3) * 2; } else { $cpur3 = 0;$yesdat[3] = 0;$daydat[3] = "�H"; }
	if($yesdat[4] ne ""){ $cpur4 = ($yesdat[4] / $yesc) * 100;$cpur4 = sprintf("%.2f",$cpur4) * 2; } else { $cpur4 = 0;$yesdat[4] = 0;$daydat[4] = "�H"; }
	if($yesdat[5] ne ""){ $cpur5 = ($yesdat[5] / $yesc) * 100;$cpur5 = sprintf("%.2f",$cpur5) * 2; } else { $cpur5 = 0;$yesdat[5] = 0;$daydat[5] = "�H"; }
	if($yesdat[6] ne ""){ $cpur6 = ($yesdat[6] / $yesc) * 100;$cpur6 = sprintf("%.2f",$cpur6) * 2; } else { $cpur6 = 0;$yesdat[6] = 0;$daydat[6] = "�H"; }
	$w0 = $weday[$wday - 1];$w1 = $weday[$wday - 2];$w2 = $weday[$wday - 3];$w3 = $weday[$wday - 4];$w4 = $weday[$wday - 5];$w5 = $weday[$wday - 6];$w6 = $weday[$wday - 7];

print <<"CANCELL";
<a name=2></a>
<hr size=3 width=80%><p>

<font color=#555555 size=5>������<b>�@�T�ԃA�N�Z�X�����@</b>������</font><br>
�ߋ��P�T�Ԃ̃A�N�Z�X����
<table border=1 cellpadding=2 width=80%><tr bgcolor=#555555>
<th bgcolor=#eeeebb width=12.5%>�O<br>��<br>�t</th>
<td align=center valign=bottom width=12.5% height=200><img src=\"$bar2\" width=80% height=$cpur6></td>
<td align=center valign=bottom width=12.5% height=200><img src=\"$bar2\" width=80% height=$cpur5></td>
<td align=center valign=bottom width=12.5% height=200><img src=\"$bar2\" width=80% height=$cpur4></td>
<td align=center valign=bottom width=12.5% height=200><img src=\"$bar2\" width=80% height=$cpur3></td>
<td align=center valign=bottom width=12.5% height=200><img src=\"$bar2\" width=80% height=$cpur2></td>
<td align=center valign=bottom width=12.5% height=200><img src=\"$bar2\" width=80% height=$cpur1></td>
<td align=center valign=bottom width=12.5% height=200><img src=\"$bar2\" width=80% height=$cpur0></td>
</tr><tr bgcolor=#333333>
<th bgcolor=#eeeebb>����</th>
<td align=center><font color=00ff00><b>$yesdat[6]</b></font></td>
<td align=center><font color=00ff00><b>$yesdat[5]</b></font></td>
<td align=center><font color=00ff00><b>$yesdat[4]</b></font></td>
<td align=center><font color=00ff00><b>$yesdat[3]</b></font></td>
<td align=center><font color=00ff00><b>$yesdat[2]</b></font></td>
<td align=center><font color=00ff00><b>$yesdat[1]</b></font></td>
<td align=center><font color=00ff00><b>$yesdat[0]</b></font></td>
</tr><tr bgcolor=#cccccc>
<th bgcolor=#eeeebb nowrap>���t</th>
<th nowrap>$daydat[6]��<br>$w6</th>
<th nowrap>$daydat[5]��<br>$w5</th>
<th nowrap>$daydat[4]��<br>$w4</th>
<th nowrap>$daydat[3]��<br>$w3</th>
<th nowrap>$daydat[2]��<br>$w2</th>
<th nowrap>$daydat[1]��<br>$w1</th>
<th nowrap>$daydat[0]��<br>$w0</th>
</tr></table><font size=2>���@�u?���v�͒����f�[�^�[����</font></p>
<a name=3></a>
<hr size=3 width=80%><p>

CANCELL

	&filegakan;

	if($vno){
		foreach $lines (@AGDATE) {
		($mongc,$gakc) = split(/\,/,$lines);
			$gakc =~ s/\n//;
			if($mongc){ push(@mongcdat,$mongc); }
			if($gakc){ push(@gakdat,$gakc); }
		}
		$yesg = $gakdat[0] + $gakdat[1] + $gakdat[2] + $gakdat[3] + $gakdat[4] + $gakdat[5] + $gakdat[6]; $gakdat[7] + $gakdat[8] + $gakdat[9] + $gakdat[10] + $gakdat[11];
	}
	if($gakdat[0]){ $gpur0 = ($gakdat[0] / $yesg) * 100;$gpur0 = sprintf("%.2f",$gpur0) * 2; } else { $gpur0 = 0;$gakdat[0] = 0;$mongcdat[0] = "�H";}
	if($gakdat[1]){ $gpur1 = ($gakdat[1] / $yesg) * 100;$gpur1 = sprintf("%.2f",$gpur1) * 2; } else { $gpur1 = 0;$gakdat[1] = 0;$mongcdat[1] = "�H"; }
	if($gakdat[2]){ $gpur2 = ($gakdat[2] / $yesg) * 100;$gpur2 = sprintf("%.2f",$gpur2) * 2; } else { $gpur2 = 0;$gakdat[2] = 0;$mongcdat[2] = "�H"; }
	if($gakdat[3]){ $gpur3 = ($gakdat[3] / $yesg) * 100;$gpur3 = sprintf("%.2f",$gpur3) * 2; } else { $gpur3 = 0;$gakdat[3] = 0;$mongcdat[3] = "�H"; }
	if($gakdat[4]){ $gpur4 = ($gakdat[4] / $yesg) * 100;$gpur4 = sprintf("%.2f",$gpur4) * 2; } else { $gpur4 = 0;$gakdat[4] = 0;$mongcdat[4] = "�H"; }
	if($gakdat[5]){ $gpur5 = ($gakdat[5] / $yesg) * 100;$gpur5 = sprintf("%.2f",$gpur5) * 2; } else { $gpur5 = 0;$gakdat[5] = 0;$mongcdat[5] = "�H"; }
	if($gakdat[6]){ $gpur6 = ($gakdat[6] / $yesg) * 100;$gpur6 = sprintf("%.2f",$gpur6) * 2; } else { $gpur6 = 0;$gakdat[6] = 0;$mongcdat[6] = "�H"; }
	if($gakdat[7]){ $gpur7 = ($gakdat[7] / $yesg) * 100;$gpur7 = sprintf("%.2f",$gpur7) * 2; } else { $gpur7 = 0;$gakdat[7] = 0;$mongcdat[7] = "�H"; }
	if($gakdat[8]){ $gpur8 = ($gakdat[8] / $yesg) * 100;$gpur8 = sprintf("%.2f",$gpur8) * 2; } else { $gpur8 = 0;$gakdat[8] = 0;$mongcdat[8] = "�H"; }
	if($gakdat[9]){ $gpur9 = ($gakdat[9] / $yesg) * 100;$gpur9 = sprintf("%.2f",$gpur9) * 2; } else { $gpur9 = 0;$gakdat[9] = 0;$mongcdat[9] = "�H"; }
	if($gakdat[10]){ $gpur10 = ($gakdat[10] / $yesg) * 100;$gpur10 = sprintf("%.2f",$gpur10) * 2; } else { $gpur10 = 0;$gakdat[10] = 0;$mongcdat[10] = "�H"; }
	if($gakdat[11]){ $gpur11 = ($gakdat[11] / $yesg) * 100;$gpur11 = sprintf("%.2f",$gpur11) * 2; } else { $gpur11 = 0;$gakdat[11] = 0;$mongcdat[11] = "�H"; }

print <<"CANCELL";

<font color=#555555 size=5>��������<b>�@���ԃA�N�Z�X�����@</b>��������</font><br>
�ߋ��P�N�̌��ԃA�N�Z�X����
<table border=1 cellpadding=2 width=85%><tr bgcolor=#555555>
<th bgcolor=#eeeebb width=6%>�O<br>��<br>�t</th>
<td align=center valign=bottom width=7.8% height=200><img src=\"$bar2\" width=80% height=$gpur11></td>
<td align=center valign=bottom width=7.8% height=200><img src=\"$bar2\" width=80% height=$gpur10></td>
<td align=center valign=bottom width=7.8% height=200><img src=\"$bar2\" width=80% height=$gpur9></td>
<td align=center valign=bottom width=7.8% height=200><img src=\"$bar2\" width=80% height=$gpur8></td>
<td align=center valign=bottom width=7.8% height=200><img src=\"$bar2\" width=80% height=$gpur7></td>
<td align=center valign=bottom width=7.8% height=200><img src=\"$bar2\" width=80% height=$gpur6></td>
<td align=center valign=bottom width=7.8% height=200><img src=\"$bar2\" width=80% height=$gpur5></td>
<td align=center valign=bottom width=7.8% height=200><img src=\"$bar2\" width=80% height=$gpur4></td>
<td align=center valign=bottom width=7.8% height=200><img src=\"$bar2\" width=80% height=$gpur3></td>
<td align=center valign=bottom width=7.8% height=200><img src=\"$bar2\" width=80% height=$gpur2></td>
<td align=center valign=bottom width=7.8% height=200><img src=\"$bar2\" width=80% height=$gpur1></td>
<td align=center valign=bottom width=7.8% height=200><img src=\"$bar2\" width=80% height=$gpur0></td>
</tr><tr bgcolor=#333333>
<th bgcolor=#eeeebb nowrap>����</th>
<td align=center><font color=00ff00><b>$gakdat[11]</b></font></td>
<td align=center><font color=00ff00><b>$gakdat[10]</b></font></td>
<td align=center><font color=00ff00><b>$gakdat[9]</b></font></td>
<td align=center><font color=00ff00><b>$gakdat[8]</b></font></td>
<td align=center><font color=00ff00><b>$gakdat[7]</b></font></td>
<td align=center><font color=00ff00><b>$gakdat[6]</b></font></td>
<td align=center><font color=00ff00><b>$gakdat[5]</b></font></td>
<td align=center><font color=00ff00><b>$gakdat[4]</b></font></td>
<td align=center><font color=00ff00><b>$gakdat[3]</b></font></td>
<td align=center><font color=00ff00><b>$gakdat[2]</b></font></td>
<td align=center><font color=00ff00><b>$gakdat[1]</b></font></td>
<td align=center><font color=00ff00><b>$gakdat[0]</b></font></td>
</tr><tr bgcolor=#cccccc>
<th bgcolor=#eeeebb nowrap>����</th>
<th nowrap>$mongcdat[11]��</th>
<th nowrap>$mongcdat[10]��</th>
<th nowrap>$mongcdat[9]��</th>
<th nowrap>$mongcdat[8]��</th>
<th nowrap>$mongcdat[7]��</th>
<th nowrap>$mongcdat[6]��</th>
<th nowrap>$mongcdat[5]��</th>
<th nowrap>$mongcdat[4]��</th>
<th nowrap>$mongcdat[3]��</th>
<th nowrap>$mongcdat[2]��</th>
<th nowrap>$mongcdat[1]��</th>
<th nowrap>$mongcdat[0]��</th>
</tr></table><font size=2>���@�u?���v�͒����f�[�^�[����</font></p>

CANCELL

}


	print "<a name=4></a>\n";
	print "<hr size=3 width=80%><p>\n";
	print "<font color=#555555 size=5>����������<b>�@�����N�������@</b>����������</font>\n";
	print "<br>�S����$c�� - ��������$refc��\n";
	print "<table border=1 width=85% cellpadding=2>\n";
	print "<tr bgcolor=#eeeebb><th nowrap width=60%>�����N��</th><th nowrap width=30% colspan=2>����</th><th nowrap width=10%>(����)</th></tr>\n";
	@refs = sort { $ref{$b} <=> $ref{$a} } keys(%ref);
	foreach $refkey (@refs) {
	$pur = ($ref{$refkey} / $res) * 100;$pur = sprintf("%.1f",$pur);
	if(length($refkey) > 50){ $urlche = substr($refkey,0,45);$urlche .= "�����"; } else { $urlche = $refkey; }
		if($ref{$refkey} > $refken){
		print "<tr><td nowrap bgcolor=#cccccc><a href=\"$refkey\" target=\"_blank\">$urlche</a></td><td nowrap bgcolor=#333333 align=center width=5%><font color=00ff00><b>$ref{$refkey}</b></font></td><td nowrap bgcolor=#555555 width=25%><img src=\"$bar\" width=$pur\% height=10></td><td nowrap align=center bgcolor=#ffffe7>($pur\%)</td></tr>\n";
		}
	}
	print "</table>\n";
	if($refken ne "0"){ print "<font size=2>�� $refken���ȉ��ȗ�</font>\n"; }
	print "</p>\n";

	print "<a name=5></a>\n";
	print "<hr size=3 width=80%><p>\n";

	print "<font color=#555555 size=5>����������<b>�@�z�X�g�����@</b>����������</font>\n";
	print "<br>�S����$c�� - ��������$hosc��\n";
	print "<table border=1 width=85% cellpadding=2>\n";
	print "<tr bgcolor=#eeeebb><th nowrap width=10%>�z�X�g��</th><th nowrap width=30%>�z�X�g��</th><th nowrap colspan=2 width=50%>����</th><th nowrap width=10%>(����)</th></tr>\n";
	@hosts = sort { $host{$b} <=> $host{$a} } keys(%host);
	$h = 0;
	foreach $hostkey (@hosts) {
	$h++;
	$pur = ($host{$hostkey} / $hss) * 100;$pur = sprintf("%.1f",$pur);
		if($host{$hostkey} > $hosken){
		print "<tr><td nowrap align=center>$h</td><td nowrap bgcolor=#cccccc>$hostkey</td><td nowrap bgcolor=#333333 align=center width=5%><font color=00ff00><b>$host{$hostkey}</b></font></td><td nowrap bgcolor=#555555><img src=\"$bar\" width=$pur\% height=10></td><td nowrap align=center bgcolor=#ffffe7>($pur\%)</td></tr>\n";
		}
	}
	print "</table>\n";
	if($hosken ne "0"){ print "<font size=2>�� $hosken���ȉ��ȗ�</font>\n"; }
	print "</p>\n";

	print "<a name=6></a>\n";
	print "<hr size=3 width=80%><p>\n";

	print "<font color=#555555 size=5>����������<b>�@�u���E�U�����@</b>����������</font>\n";
	print "<br>�S����$c�� - ��������$agec��\n";
	print "<table border=1 width=85% cellpadding=2>\n";
	print "<tr bgcolor=#eeeebb><th nowrap width=60%>�u���E�U</th><th nowrap colspan=2 width=30%>����</th><th nowrap width=10%>(����)</th></tr>\n";
	@agens = sort { $agen{$b} <=> $agen{$a} } keys(%agen);
	foreach $agenkey (@agens) {
	$pur = ($agen{$agenkey} / $ags) * 100;$pur = sprintf("%.1f",$pur);
	if(length($agenkey) > 50){ $ageche = substr($agenkey,0,45);$ageche .= "����)"; } else { $ageche = $agenkey; }
		if($agen{$agenkey} > $ageken){
		print "<tr><td nowrap bgcolor=#cccccc>$ageche</td><td nowrap bgcolor=#333333 align=center width=5%><font color=00ff00><b>$agen{$agenkey}</b></font></td><td nowrap bgcolor=#555555 width=25%><img src=\"$bar\" width=$pur\% height=10></td><td nowrap align=center bgcolor=#ffffe7>($pur\%)</td></tr>\n";
		}
	}
	print "</table>\n";
	if($ageken ne "0"){ print "<font size=2>�� $ageken���ȉ��ȗ�</font>\n"; }
	print "</p>\n";

&end;

#**************************************************************************

sub passche{

print <<"CANCELL";

<form action=./easyaccess.cgi?mode method=POST>
<table width=90% border=0 cellpadding=20><tr>
<td bgcolor=#f7f7f7>
�� <b>�o�X���[�h�F</b>
<input type=password size=30 name="maspass">

<select name=mode size=1>
<option value=today>*** �{�� ***
<option value=yes>*** ��� ***
</select>
</td></tr></table><p>
<input type=submit value="�@��͉�ʂց@"></form></p>
CANCELL
&end;


}

#**************************************************************************

sub end{

#�X�N���v�g���쌠�\���i�폜���Ȃ��ŉ������j
print <<"CANCELL";
<hr size=3 width=90%>
</center></p>
<p align=right><font size=2><a href="http://www.pmcj.com/" target="top">Easy Access Ver1.13 by Tomey</a></font></p>
</body></html>
CANCELL

exit;
}

#**************************************************************************

sub timeget1 {
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($timec);
	if($year < 99){ $chri = 2000; } else { $chri = 1900; }
	$year += $chri;
	$mon = $mon + 1;
	if ($mon < 10){ $mon = "0$mon"; }
	if ($mday < 10){ $mday = "0$mday"; }
	if ($hour < 10){ $hour = "0$hour"; }
	if ($min < 10){ $min = "0$min"; }
	if ($sec < 10){ $sec = "0$sec"; }
	@weday = ('<font color=#ff0000>(��)</font>','(��)','(��)','(��)','(��)','(��)','<font color=#0000ff>(�y)</font>');
	$TIME = "$year�N$mon��$mday��$weday[$wday]$hour:$min:$sec";
	$acss = $dateroot . "$mon$mday.csv";
}

sub timeget2 {
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($timec - $btim*24*60*60);
	if($year < 99){ $chri = 2000; } else { $chri = 1900; }
	$year += $chri;
	$mon = $mon + 1;
	if ($mon < 10){ $mon = "0$mon"; }
	if ($mday < 10){ $mday = "0$mday"; }
	@weday = ('<font color=#ff0000>(��)</font>','(��)','(��)','(��)','(��)','(��)','<font color=#0000ff>(�y)</font>');
	$TIME = "$year�N$mon��$mday��$weday[$wday]";
	$acss2 = $dateroot . "$mon$mday.csv";

}

#**************************************************************************

sub fileread {
	if (!open(NOTE,"<$countdate")) { &massehtml($no = 0); }
	@ACDATE = <NOTE>;
	close(NOTE);
}
sub fileacss {
	if (!open(NOTE,"<$acssdate")) { &massehtml($no = 1); }
	@AADATE = <NOTE>;
	close(NOTE);
}
sub filegakan {
	$vno = 0;
	if (!open(NOTE,"<$gekandate")) { 
	print "���Ԃ̃f�[�^�[�͂܂�����܂���B<br>\n";
	} else { $vno = 1; }
	@AGDATE = <NOTE>;
	close(NOTE);
}
#**************************************************************************
sub method {

	if ($ENV{'REQUEST_METHOD'} eq "POST") {
	read(STDIN, $inform, $ENV{'CONTENT_LENGTH'});
	} else { $inform = $ENV{'QUERY_STRING'}; }
	@preta = split(/&/, $inform);
	foreach $substi (@preta) {
	($inName, $value) = split(/=/, $substi);
	$value =~ tr/+/ /;
	$value =~ s/%([0-9A-Fa-f]{2})/pack("C", hex($1))/eg;
	$FORMIN{$inName} = $value;
	}
}
#**************************************************************************
sub massehtml{

	$masse[0] = "�L���t�@�C�����J���܂���B<br>�f�[�^�[�������悤�ł��B";
	$masse[1] = "�A�N�Z�X�t�@�C�����J���܂���B<br>�f�[�^�[�������悤�ł��B";
	$masse[2] = "���[�h�̎w�肪����܂���B<br>�{��=...easyaccess.cgi?mode=today<br>���=...easyaccess.cgi?mode=yes";


print <<"CANCELL";
<table width=90% cellspacing=0 cellpadding=0 align=center bgcolor=$color3>
<tr><th nowrap>
<p>�@</p><font color="$fcolor2"><b>$masse[$no]</b><p>�@</p>
</th></tr></table>
CANCELL


&end;
}

