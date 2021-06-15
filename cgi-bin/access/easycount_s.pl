#!/usr/bin/perl
#**************************************************************************
#
#    easycount_s.pl Easy Count [S] Ver1.3
#    Created on: 98/12/25 Modified 99/11/05
#   (C) Copyright 1998 by Tomey(Tomio Sato) info@web-purpose.com
#    http://www.web-purpose.com/PMC/
#
#  1.改造の有無にかかわらずこのスクリプトの再配布・レンタル・販売及び有償代行設置サ－ビスは禁止いたします。
#  2.スクリプト利用によるいかなる障害や損害なども私は一切の責任を負いません。すべて自己の責任においてご利用下さい。
#  
#**************************************************************************
#個人設定
#**************************************************************************
#
#
#カウンターを設置するファイルの場所から見たスクリプトの格納ディレクトリーの指定
$cder = '../cgi-bin/access/';
#
#カウント記録ファイル
$countdate = $cder . "count.dat";
#
#
#■総合カウンターの表示。非表示の場合「off」か空にする
$soucount = 'off';
#
#↓総合カウンターの表示の時の明細設定
$cimg = 'off';	#画像カウンター表示、テキスト表示の場合「off」か空にする
$f_kaku = 'gif';	#画像の拡張子の指定
#カウンターを設置するファイルの場所から見た画像格納ディレクトリーの指定
$imgderc = '../cgi-bin/access/img1/';
$counw = '15';	#画像の横幅
$counh = '20';	#画像の高さ
$cketa = '7';	#総合カウンターの桁数
$sotxt1 = '<b><font size=2>あなたは ';	#総合カウンターの前に付く文字列
$sotxt2 = '番目の訪問者です。</font></b><p>';	#総合カウンターの後ろに付く文字列
#

#■本日、昨日のカウンター表示、テキスト表示の場合「off」か空にする
$daycount = 'off';
#
#↓本日、昨日のカウンターの表示の時の明細設定
$dimg = 'off';	#画像カウンター表示、テキスト表示の場合「off」か空にする
$f_kakud = 'gif';	#画像の拡張子の指定
#カウンターを設置するファイルの場所から見た画像格納ディレクトリーの指定
$imgderd = '../cgi-bin/access/img2/';
$dayw = '13';	#画像の横幅
$dayh = '17';	#画像の高さ
$dketa = '3';	#DAYカウンターの桁数
$daytxt1 = '<b><font size=2>Today ';	#今日のカウンターの前に付く文字列
$daytxt2 = 'Count ';	#今日のカウンターの後ろに付く文字列
$daytxt3 = '- Yesterday ';	#昨日のカウンターの前に付く文字列
$daytxt4 = 'Count</font></b></p>';	#昨日のカウンターの後ろに付く文字列
#
#■アクセス解析を行う。解析をしない場合「off」か空にする
$acsskaiski = 'on';
#
#海外サーバー時刻設定(「1」= マイナス９時間、「2」= プラス９時間)
$timeche = '0';
#
#**********************

# 集計したくないURLを指定（この文字列を含むデータを記録しない）
#記入例「http://www.web-purpose.com/」とあれば、「http://www.web-purpose.com/」内からのアクセスでのカウント及び解析を省きます。
@refs = (
"http://xxx.xxxxx.xx.xx/",
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
$lockfile = $cder . "easycount.dat";# ロックファイル名
#
#**************************************************************************
#個人設定はここまで
#**************************************************************************
	if($timeche eq "1"){ $timec = time - 9*60*60; }
	elsif ($timeche eq "2"){ $timec = time + 9*60*60; }
	else { $timec = time; }
#**************************************************************************

$ref = $ENV{'HTTP_REFERER'};
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
	$acssdate = $cder . $acss;
	$achodate = $cder . "acsshost";

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

sub countdis{

	if($day ne ""){

	$count++;

	if($mday ne "$day"){ 
		if($mon ne "$monc"){
		$gedate = $cder . "gekan.dat";
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
 
if($soucount eq "on"){

	$count =~ s/\n//g;
	print "$sotxt1";
	@scount = split(//, $count);
	while (@scount < $cketa){ unshift(@scount,0); }
	foreach $counter (@scount) {
		if($cimg ne "on"){ print "<b>$counter</b>";
		} else {
		print "<img src=\"$imgderc$counter.$f_kaku\" width=$counw height=$counh alt=\"$counter\">";
		}
	}
	print "$sotxt2";
}
if($daycount eq "on"){
	print "$daytxt1";
	@stoday = split(//, $today);
	while (@stoday < $dketa){ unshift(@stoday,0); }
	foreach $todayc (@stoday) {
		if($dimg ne "on"){ print "<b>$todayc</b>";
		} else {
		print "<img src=\"$imgderd$todayc.$f_kakud\" width=$dayw height=$dayh alt=\"$todayc\">";
		}
	}
	print "$daytxt2$daytxt3";
	@syes = split(//, $yes);
	while (@syes < $dketa){ unshift(@syes,0); }
	foreach $yesc (@syes) {
		if($dimg ne "on"){ print "<b>$yesc</b>";
		} else {
		print "<img src=\"$imgderd$yesc.$f_kakud\" width=$dayw height=$dayh alt=\"$yesc\">";
		}
	}
	print "$daytxt4\n";
}

exit;
#**************************************************************************

sub timeget1 {
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($timec);
	$mon = $mon + 1;
	if ($mon < 10){ $monlog = "0$mon"; } else { $monlog = "$mon"; }
	if ($mday < 10){ $mdaylog = "0$mday"; } else { $mdaylog = "$mday"; }
	if ($hour < 10){ $hour = "0$hour"; }
	$acss = $monlog . $mdaylog . ".csv";
}

sub timeget2 {
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($timec - 2*24*60*60);
	$mon = $mon + 1;
	if ($mon < 10){ $monlog = "0$mon"; } else { $monlog = "$mon"; }
	if ($mday < 10){ $mdaylog = "0$mday"; } else { $mdaylog = "$mday"; }
	$acss2 = $monlog . $mdaylog . ".csv";
	$oldacssdate = $cder . $acss2;
	unlink("$oldacssdate");
}

#**************************************************************************

sub fileread {
	if (!open(NOTE,"<$countdate")) { &massehtml($no = 0); }
	@CDATE = <NOTE>;
	close(NOTE);
}

sub fileacho {
	if (!open(NOTE,"<$achodate")) { &massehtml($no = 2); }
	$AHDATE = <NOTE>;
	close(NOTE);
}

#**************************************************************************
sub massehtml{

	$masse[0] = "記事ファイルを開けません。<br>データーが無いようです。";
	$masse[1] = "アクセスファイルを開けません。<br>データーが無いようです。";
	$masse[2] = "ホストファイルを開けません。<br>データーが無いようです。";
	$masse[3] = "ビージー状態です。lock";

print <<"CANCELL";
<table width=90% cellspacing=0 cellpadding=0 align=center bgcolor=$color3>
<tr><th nowrap>
<p>　</p><font color="$fcolor2"><b>$masse[$no]</b><p>　</p>
</th></tr></table>
CANCELL


exit;
}

#**************************************************************************

sub lock {
	local($retry) = 3;
	while (!symlink(".", $lockfile)) {
		if($retry == 3){ &lockche; }
		if (--$retry <= 0) { &massehtml($no = 3); }
	}
}
sub lock2 {
	$retry = 3;
	while (-e $lockfile){
		if($retry == 3){ &lockche; }
		if(--$retry <= 0 ){ &massehtml($no = 3); }
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

