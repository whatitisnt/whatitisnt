#!/usr/bin/perl
#**************************************************************************
#
#    easycount_c.cgi Easy Count [C] Ver1.23
#    Created on: 99/01/03 Modified 00/11/13
#   (C) Copyright 1998- by Tomey(Tomio Sato)
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
#�ucount.dat�v�ugekan.dat�v�uacsshost�v�u���scv�t�@�C���v�ueasycocg.dat(���b�N�t�@�C��)�v��
#�@�i�[�f�B���N�g���[�w��ł��B(�i�[�f�B���N�g���[[777])
$dateroot = './';
#
#
#�J�E���g�L�^�t�@�C��
$countdate = $dateroot . "count.dat";
#
#�_�~�[�摜�t�@�C��
$dampic = 'botan.gif';
#
#�������J�E���g�摜�i�[�f�B���N�g���[
$imgderc = './img1/';
#�����J�E���g�摜�g���q
$f_kaku = 'gif';
#�����J�E���g����
$cketa = '6';
#
#���A�N�Z�X��͂��s���B��͂����Ȃ��ꍇ�uoff�v����ɂ���
$acsskaiski = 'on';
#
#�ǂ��̃y�[�W�̃A�N�Z�X�������u0�v�����N�������u1�v(�u1�v�̏ꍇ�AJavaScript�ŋL�q)
$refche = '0';
#
# $refche���u1�v�̎��A�W�v�������Ȃ�URL���w��i���̕�������܂ރf�[�^���L�^���Ȃ��j
#�L����uhttp://www.web-purpose.com/�v�Ƃ���΁A�uhttp://www.web-purpose.com/�v������̃A�N�Z�X�ł̃J�E���g�y�щ�͂��Ȃ��܂��B
@refs = (
"",
"",
"",
"",
""
);
#
#�����[�h�h�~����ꍇ�uon�v
$acceche = 'off';
#
# �t�@�C�����b�N (on�Aoff) �G���[�̏o��ꍇ��off�ɏ��������邩on������
$lockmode = 'off';
$lockfile = $dateroot . "easycoc.dat";	# ���b�N�t�@�C����
#
#�C�O�T�[�o�[�����ݒ�(�u1�v= �}�C�i�X�X���ԁA�u2�v= �v���X�X����)
$timeche = '0';
#**************************************************************************
#�l�ݒ�͂����܂�
#**************************************************************************

&method;

	if($timeche eq "1"){ $timec = time - 9*60*60; }
	elsif ($timeche eq "2"){ $timec = time + 9*60*60; }
	else { $timec = time; }

$f_mod = $FORMIN{'mode'};

	if($f_mod eq ""){ &massehtml; }
#**************************************************************************



if($FORMIN{'c'} eq "1" || $f_mod eq "dam"){

	if($refche ne "1"){
	$ref = $ENV{'HTTP_REFERER'};
	} else {
	$ref = $FORMIN{'url'};
	}
	$ref =~ s/\%7E/\~/ig;

	$rhost = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};
	if ($rhost eq $addr || $rhost eq "") { $rhost = gethostbyaddr(pack('C4',split(/\./,$addr)),2) || $addr; }

	if ($rhost eq $addr || $rhost eq ""){ 
	$rhost = $addr;
	@hosadd = split(/\./, $rhost);
	splice(@hosadd, 3, 1);
	} else {
	@hosadd = split(/\./, $rhost);
	$hosdel = @hosadd;$hosdel = $hosdel - 3;
	splice(@hosadd, 0, $hosdel);
	}
	$host = "@hosadd";
	$host =~ s/ /\./g;
	if ($rhost eq $addr){
	$host = $host . "\.\*";
	} else {
	$host = "\*\." . $host;
	}
	if ($host eq "*." || $host eq ".*") { $host = "Add Can't Host"; }

	$agen = $ENV{'HTTP_USER_AGENT'};
	$agen =~ s/\,//g;
	$agen =~ s/compatible\; //g;
	$agen =~ s/Windows/Win/g;
	$agen =~ s/Macintosh/Mac/g;
	$agen =~ s/\;/\//g;

	&timeget1;
	$achodate = $dateroot . "acsshost";

	if($acsskaiski eq "on"){
		if(!(-e $acssdate)){
		open(OUTA,">>$acssdate");
		close(OUTA);
		}
	if(!(-e $acssdate)){ &erorr($no = 0); }
	}

	if (!(-e $achodate)) {
		open(OUTB,">>$achodate");
		close(OUTB);
		}

	$hoskyo = 0;
	&fileacho;
	&fileread;
	($monc,$day,$today,$yes,$gekan,$count) = split(/\,/,$CDATE[0]);

	foreach $kyo (@refs) {
		if($acceche eq "on"){
		if (($rhost eq "$AHDATE" && $mday eq "$day") || ($kyo ne "" && $ref =~ /$kyo/i)) { $hoskyo = 1; }
		} else {
		if ($kyo ne "" && $ref =~ /$kyo/i) { $hoskyo = 1; }
		}
	}

	if($hoskyo eq "0"){
	if($lockmode eq "on"){ &lock; }
	&countdis;
	&unlock;
	}
	&timeget2;

} else {

	sleep(1);
	if($lockmode eq "on" && $FORMIN{'c'} ne "1" && -e $lockfile){ sleep(1); }
}

	&fileread;
	($monc,$day,$today,$yes,$gekan,$counto) = split(/\,/,$CDATE[0]);

	$counto =~ s/\n//g;
	@scount = split(//, $counto);
	@scount = reverse(@scount);
	while (@scount < $cketa){ push(@scount,0); }

	if($f_mod ne "dam"){
	$cogif = $FORMIN{'c'} - 1;
	@scount = reverse(@scount);
		if($f_mod eq "actx"){
			print "Content-type: text/plain\n\n";
			foreach $counter (@scount) {
			print "$counter";
			}
		} else {
			print "Content-type: image/gif\n\n";
			$giffile = $imgderc . $scount[$cogif] . ".$f_kaku";
			$gsize = -s $giffile;
			open(IN, $giffile);
			binmode(IN);
			binmode(STDOUT);
			read(IN, $picout, $gsize);
			print $picout;
			close(IN);
		}
	} else {

		print "Content-type: image/gif\n\n";
		$gsize = -s $dampic;
		open(IN, $dampic);
		binmode(IN);
		binmode(STDOUT);
		read(IN, $picout, $gsize);
		print $picout;
		close(IN);
	}

exit;

#**************************************************************************

sub countdis{

	if($day ne ""){

	$count++;

	if($mday ne "$day"){ 
		if($mon ne "$monc"){
		$gedate = $dateroot . "gekan.dat";
			$gekanin = $gekan + $today;
			$monin = $mon - 1;
			if($monin eq "0"){ $monin = 12; }
			if (!(-e "$gedate")) {
			open(FILE,">>$gedate");
			print FILE "$monin,$gekanin\n";
			close(FILE);
			} else {
			open(FILE,"<$gedate");
			@GDATE = <FILE>;
			close(FILE);
			$gdip = "$monin,$gekanin\n";
			unshift(@GDATE,$gdip);
			$coutg = @GDATE;
			if($coutg > 12){ splice(@GDATE, 12, 1); }

			open(FILE,">$gedate");
			eval 'flock(FILE,2);';
			print FILE @GDATE;
			eval 'flock(FILE,8);';
			close(FILE);
			}
		$gekan = 0;
		} else {
		$gekan = $gekan + $today;
		}
	$yes = $today;$today = 1;
	} else {
	$today++;
	}

	$cdisp = "$mon,$mday,$today,$yes,$gekan,$count\n";
	if($mday ne $day){
	unshift(@CDATE,$cdisp);
	} else {
	$CDATE[0] = $cdisp;
	}
	$cda = @CDATE;
	if($cda > 7){ splice(@CDATE, 7, 1); }
	open(LOGC,">$countdate");
	eval 'flock(LOGC,2);';
	print LOGC @CDATE;
	eval 'flock(LOGC,8);';
	close(LOGC);

	if($acsskaiski eq "on"){
	open(LOGA,">>$acssdate");
	eval 'flock(LOGA,2);';
	print LOGA "$hour\,$ref\,$host\,$agen\,$count\n";
	eval 'flock(LOGA,8);';
	close(LOGA);
	}

	open(LOGAC,">$achodate");
	eval 'flock(LOGAC,2);';
	print LOGAC $rhost;
	eval 'flock(LOGAC,8);';
	close(LOGAC);

	}
}




#**************************************************************************

sub end{

#�X�N���v�g���쌠�\���i�폜���Ȃ��ŉ������j
print <<"CANCELL";
<hr size=3 width=90%>
</center></p>
<p align=right><font size=2><a href="http://www.web-purpose.com/PMC/" target="top">Easy Count [C] Ver1.11 by Tomey</a></font></p>
</body></html>
CANCELL

exit;
}

#**************************************************************************

sub timeget1 {
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($timec);
	$mon = $mon + 1;
	if ($mon < 10){ $monlog = "0$mon"; } else { $monlog = "$mon"; }
	if ($mday < 10){ $mdaylog = "0$mday"; } else { $mdaylog = "$mday"; }
	if ($hour < 10){ $hour = "0$hour"; }
	$acssdate = $dateroot . $monlog . $mdaylog . ".csv";
}

sub timeget2 {
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($timec - 2*24*60*60);
	$mon = $mon + 1;
	if ($mon < 10){ $monlog = "0$mon"; } else { $monlog = "$mon"; }
	if ($mday < 10){ $mdaylog = "0$mday"; } else { $mdaylog = "$mday"; }
	$acss2 = $dateroot . $monlog . $mdaylog . ".csv";
	unlink("$acss2");
}

#**************************************************************************
sub fileread {
	if (!open(NOTE,"<$countdate")) { &erorr($no = 0); }
	@CDATE = <NOTE>;
	close(NOTE);
}

sub fileacho {
	if (!open(NOTE,"<$achodate")) { &erorr($no = 0); }
	$AHDATE = <NOTE>;
	close(NOTE);
}

#**************************************************************************
sub method {

	if ($ENV{'REQUEST_METHOD'} eq "POST") {
	read(STDIN, $inform, $ENV{'CONTENT_LENGTH'});
	} else { $inform = $ENV{'QUERY_STRING'}; }
	@preta = split(/&/,$inform);
	foreach $substi (@preta) {
	($inName, $value) = split(/=/, $substi);
	$value =~ s/\+/ /g;
	$value =~ s/%([0-9A-Fa-f]{2})/pack("C", hex($1))/eg;
	$FORMIN{$inName} = $value;
	}
}
#**************************************************************************
sub massehtml{

#�X�N���v�g���쌠�\���i�폜���Ȃ��ŉ������j
	print "Content-type: text/html\n\n";

print <<"CANCELL";
<table width=90% cellspacing=0 cellpadding=0 align=center bgcolor=$color3>
<tr><th nowrap>
<p>�@</p><font color="$fcolor2"><b>����̓J�E���^�[CGI�ł��B</b><p>�@</p>
</th></tr></table>

<hr size=3 width=90%>
</center></p>
<p align=right><font size=2><a href="http://www.pmcj.com/" target="top">Easy Count [C] Ver1.23 by Tomey</a></font></p>
</body></html>
CANCELL

exit;
}
#**************************************************************************

sub erorr{
if($f_mod !~ /tx/i){
$erorr[0] = "notfile.gif";
$erorr[1] = "busy.gif";
$erorr[2] = "$dampic";

$eropic = "$erorr[$no]";
	print "Content-type: image/gif\n\n";
	$gsize = -s $eropic;
	open(IN, $eropic);
	binmode(IN);
	binmode(STDOUT);
	read(IN, $picout, $gsize);
	print $picout;
	close(IN);
} else {
$erorr[0] = "�ꕔ�t�@�C�����J���܂���B";
$erorr[1] = "�r�[�W�[��Ԃł��B";
$erorr[2] = "";

	print "Content-type: text/plain\n\n";
	print "$erorr[$no]";
}
exit;

}
#**************************************************************************

sub lock {
	local($retry) = 3;
	while (!symlink(".", $lockfile)) {
		if($retry == 3){ &lockche; }
		if (--$retry <= 0) { &erorr($no = 1); }
	}
}
sub lock2 {
	$retry = 3;
	while (-e $lockfile){
		if($retry == 3){ &lockche; }
		if(--$retry <= 0 ){ &erorr($no = 1); }
		sleep(2);
	}
        open( LF, ">$lockfile");
        close ( LF );
}
sub lockche {
    	($mtime) = (stat($lockfile))[9];
	if ($mtime < time() - 180) { unlink($lockfile);	}
}
sub unlock {
	if (-e $lockfile) { unlink($lockfile); }
}
