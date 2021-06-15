#!/usr/bin/perl
#**************************************************************************
#
#    easycount_c.cgi Easy Count [C] Ver1.23
#    Created on: 99/01/03 Modified 00/11/13
#   (C) Copyright 1998- by Tomey(Tomio Sato)
#    http://www.pmcj.com/   info@pmcj.com
#    http://www.web-purpose.com/PMC/   info@web-purpose.com
#
#　○利用規約抜粋
#  1.改造の有無にかかわらずこのスクリプトの再配布・レンタル・販売及び代行設置サ－ビスは禁止いたします。
#  2.スクリプト利用によるいかなる障害や損害なども私は一切の責任を負いません。すべて自己の責任においてご利用下さい。
#  
#**************************************************************************
#個人設定
#**************************************************************************
#「count.dat」「gekan.dat」「acsshost」「解析scvファイル」「easycocg.dat(ロックファイル)」の
#　格納ディレクトリー指定です。(格納ディレクトリー[777])
$dateroot = './';
#
#
#カウント記録ファイル
$countdate = $dateroot . "count.dat";
#
#ダミー画像ファイル
$dampic = 'botan.gif';
#
#■総合カウント画像格納ディレクトリー
$imgderc = './img1/';
#総合カウント画像拡張子
$f_kaku = 'gif';
#総合カウント桁数
$cketa = '6';
#
#■アクセス解析を行う。解析をしない場合「off」か空にする
$acsskaiski = 'on';
#
#どこのページのアクセスか調査「0」リンク元調査「1」(「1」の場合、JavaScriptで記述)
$refche = '0';
#
# $refcheが「1」の時、集計したくないURLを指定（この文字列を含むデータを記録しない）
#記入例「http://www.web-purpose.com/」とあれば、「http://www.web-purpose.com/」内からのアクセスでのカウント及び解析を省きます。
@refs = (
"",
"",
"",
"",
""
);
#
#リロード防止する場合「on」
$acceche = 'off';
#
# ファイルロック (on、off) エラーの出る場合はoffに書き換えるかonを消す
$lockmode = 'off';
$lockfile = $dateroot . "easycoc.dat";	# ロックファイル名
#
#海外サーバー時刻設定(「1」= マイナス９時間、「2」= プラス９時間)
$timeche = '0';
#**************************************************************************
#個人設定はここまで
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

#スクリプト著作権表示（削除しないで下さい）
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

#スクリプト著作権表示（削除しないで下さい）
	print "Content-type: text/html\n\n";

print <<"CANCELL";
<table width=90% cellspacing=0 cellpadding=0 align=center bgcolor=$color3>
<tr><th nowrap>
<p>　</p><font color="$fcolor2"><b>これはカウンターCGIです。</b><p>　</p>
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
$erorr[0] = "一部ファイルが開けません。";
$erorr[1] = "ビージー状態です。";
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
