#!/usr/bin/perl
#**************************************************************************
#
#    easyaccess.cgi Easy Access Ver1.13
#    Created on: 98/12/25 Modified 00/11/13
#   (C) Copyright 1998-2000 by Tomey(Tomio Sato)
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
#
#タイトル名の指定
$title = '■■　アクセス解析　■■';
#
$refken = '0';	#リンク元調査で何件以下を表示させないか指定。一件でも表示させる場合「0」
$hosken = '0';	#ホスト調査で何件以下を表示させないか指定。一件でも表示させる場合「0」
$ageken = '0';	#ブラウザ調査で何件以下を表示させないか指定。一件でも表示させる場合「0」
#
#データー関連ファイルルート
#「count.dat」「gekan.dat」「解析scvファイル」の格納ディレクトリー指定です。
$dateroot = './';
#
#カウント記録ファイル名
$countdate = $dateroot . "count.dat";
#月間カウント記録ファイル名(注意：gekan.datは自動的に作成されます。)
$gekandate = $dateroot . "gekan.dat";
#グラフ画像ファイル
$bar = 'bar.gif';
$bar2 = 'bar2.gif';	#週間、月間用画像ファイル
#
#
$maskey = 'on';	#マスターキーを使って閲覧する場合「on」でない場合「off」
$mpass = '2001';	#マスターキー
#
#海外サーバー時刻設定(「1」= マイナス９時間、「2」= プラス９時間)
$timeche = '0';
#
#**************************************************************************
#個人設定はここまで
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
	print "<font color=#777744>■<b></font> <a href=#1>時間帯アクセス調査</a>\n";
	if($f_mod eq "today"){
	print "<br><font color=#777744>■<b></font> <a href=#2>週間アクセス調査</a>\n";
	print "<br><font color=#777744>■<b></font> <a href=#3>月間アクセス調査</a>\n";
	}
	print "<br><font color=#777744>■<b></font> <a href=#4>リンク元調査</a>\n";
	print "<br><font color=#777744>■<b></font> <a href=#5>ホスト調査</a>\n";
	print "<br><font color=#777744>■<b></font> <a href=#6>ブラウザ調査</a>\n";
	print "</td><td width=50%><b>現在の総合カウント<br>　　<font size=4 color=#ff0000>★ $count ★</font></b><br><br>\n";
	print "<b>今日現在までの訪問者</b> 【<font color=#ff0000>$today</font>】<br><b>昨日の訪問者</b>【<font color=ff0000>$yes</font>】\n";
	print "</td></tr></table>\n";
	print "<a name=1></a>\n";
	print "<br><hr size=3 width=80%>\n";
	if($f_mod eq "today"){
	print "<form action=./easyaccess.cgi?mode=yes method=POST>\n";
	print "<font size=4>▼ <b>本日の調査結果</b> ▼</font>\n";
	print "<input type=hidden name=maspass value=\"$FORMIN{'maspass'}\">\n";
	print "<input type=hidden name=mode value=\"yes\">\n";
	print "　<input type=submit value=\"　昨日の結果　\">\n";
	} else {
	print "<form action=./easyaccess.cgi?mode=today method=POST>\n";
	print "<input type=hidden name=maspass value=\"$FORMIN{'maspass'}\">\n";
	print "<input type=hidden name=mode value=\"today\">\n";
	print "<input type=submit value=\"　本日の結果　\">\n";
	print "　<font size=4>▼ <b>昨日の調査結果</b> ▼</font>\n";
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

	print "<font color=#555555 size=5>■■■■<b>　時間帯アクセス調査　</b>■■■■</font>\n";
	print "<br>全件数$c件\n";
	print "<table border=1 width=85% cellpadding=2>\n";
	print "<tr bgcolor=#eeeebb><th nowrap width=20%>時間</th><th nowrap colspan=2 width=70%>件数</th><th nowrap width=10%>(割合)</th></tr>\n";
	@hours = sort keys(%hour);
	foreach $hourkey (@hours) {
	$pur = ($hour{$hourkey} / $c) * 100;$pur = sprintf("%.1f",$pur);
	print "<tr><th nowrap bgcolor=#cccccc>$hourkey 時</td><td nowrap bgcolor=#333333 align=center width=5%><font color=00ff00><b>$hour{$hourkey}</b></font></td><td nowrap bgcolor=#555555 width=65%><img src=\"$bar\" width=$pur\% height=10></td><td nowrap width=10% align=center bgcolor=#ffffe7>($pur\%)</th></tr>\n";
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
	if($yesdat[0] ne ""){ $cpur0 = ($yesdat[0] / $yesc) * 100;$cpur0 = sprintf("%.2f",$cpur0) * 2; } else { $cpur0 = 0;$yesdat[0] = 0;$daydat[0] = "？";}
	if($yesdat[1] ne ""){ $cpur1 = ($yesdat[1] / $yesc) * 100;$cpur1 = sprintf("%.2f",$cpur1) * 2; } else { $cpur1 = 0;$yesdat[1] = 0;$daydat[1] = "？"; }
	if($yesdat[2] ne ""){ $cpur2 = ($yesdat[2] / $yesc) * 100;$cpur2 = sprintf("%.2f",$cpur2) * 2; } else { $cpur2 = 0;$yesdat[2] = 0;$daydat[2] = "？"; }
	if($yesdat[3] ne ""){ $cpur3 = ($yesdat[3] / $yesc) * 100;$cpur3 = sprintf("%.2f",$cpur3) * 2; } else { $cpur3 = 0;$yesdat[3] = 0;$daydat[3] = "？"; }
	if($yesdat[4] ne ""){ $cpur4 = ($yesdat[4] / $yesc) * 100;$cpur4 = sprintf("%.2f",$cpur4) * 2; } else { $cpur4 = 0;$yesdat[4] = 0;$daydat[4] = "？"; }
	if($yesdat[5] ne ""){ $cpur5 = ($yesdat[5] / $yesc) * 100;$cpur5 = sprintf("%.2f",$cpur5) * 2; } else { $cpur5 = 0;$yesdat[5] = 0;$daydat[5] = "？"; }
	if($yesdat[6] ne ""){ $cpur6 = ($yesdat[6] / $yesc) * 100;$cpur6 = sprintf("%.2f",$cpur6) * 2; } else { $cpur6 = 0;$yesdat[6] = 0;$daydat[6] = "？"; }
	$w0 = $weday[$wday - 1];$w1 = $weday[$wday - 2];$w2 = $weday[$wday - 3];$w3 = $weday[$wday - 4];$w4 = $weday[$wday - 5];$w5 = $weday[$wday - 6];$w6 = $weday[$wday - 7];

print <<"CANCELL";
<a name=2></a>
<hr size=3 width=80%><p>

<font color=#555555 size=5>■■■<b>　週間アクセス調査　</b>■■■</font><br>
過去１週間のアクセス件数
<table border=1 cellpadding=2 width=80%><tr bgcolor=#555555>
<th bgcolor=#eeeebb width=12.5%>グ<br>ラ<br>フ</th>
<td align=center valign=bottom width=12.5% height=200><img src=\"$bar2\" width=80% height=$cpur6></td>
<td align=center valign=bottom width=12.5% height=200><img src=\"$bar2\" width=80% height=$cpur5></td>
<td align=center valign=bottom width=12.5% height=200><img src=\"$bar2\" width=80% height=$cpur4></td>
<td align=center valign=bottom width=12.5% height=200><img src=\"$bar2\" width=80% height=$cpur3></td>
<td align=center valign=bottom width=12.5% height=200><img src=\"$bar2\" width=80% height=$cpur2></td>
<td align=center valign=bottom width=12.5% height=200><img src=\"$bar2\" width=80% height=$cpur1></td>
<td align=center valign=bottom width=12.5% height=200><img src=\"$bar2\" width=80% height=$cpur0></td>
</tr><tr bgcolor=#333333>
<th bgcolor=#eeeebb>件数</th>
<td align=center><font color=00ff00><b>$yesdat[6]</b></font></td>
<td align=center><font color=00ff00><b>$yesdat[5]</b></font></td>
<td align=center><font color=00ff00><b>$yesdat[4]</b></font></td>
<td align=center><font color=00ff00><b>$yesdat[3]</b></font></td>
<td align=center><font color=00ff00><b>$yesdat[2]</b></font></td>
<td align=center><font color=00ff00><b>$yesdat[1]</b></font></td>
<td align=center><font color=00ff00><b>$yesdat[0]</b></font></td>
</tr><tr bgcolor=#cccccc>
<th bgcolor=#eeeebb nowrap>日付</th>
<th nowrap>$daydat[6]日<br>$w6</th>
<th nowrap>$daydat[5]日<br>$w5</th>
<th nowrap>$daydat[4]日<br>$w4</th>
<th nowrap>$daydat[3]日<br>$w3</th>
<th nowrap>$daydat[2]日<br>$w2</th>
<th nowrap>$daydat[1]日<br>$w1</th>
<th nowrap>$daydat[0]日<br>$w0</th>
</tr></table><font size=2>※　「?日」は調査データー無し</font></p>
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
	if($gakdat[0]){ $gpur0 = ($gakdat[0] / $yesg) * 100;$gpur0 = sprintf("%.2f",$gpur0) * 2; } else { $gpur0 = 0;$gakdat[0] = 0;$mongcdat[0] = "？";}
	if($gakdat[1]){ $gpur1 = ($gakdat[1] / $yesg) * 100;$gpur1 = sprintf("%.2f",$gpur1) * 2; } else { $gpur1 = 0;$gakdat[1] = 0;$mongcdat[1] = "？"; }
	if($gakdat[2]){ $gpur2 = ($gakdat[2] / $yesg) * 100;$gpur2 = sprintf("%.2f",$gpur2) * 2; } else { $gpur2 = 0;$gakdat[2] = 0;$mongcdat[2] = "？"; }
	if($gakdat[3]){ $gpur3 = ($gakdat[3] / $yesg) * 100;$gpur3 = sprintf("%.2f",$gpur3) * 2; } else { $gpur3 = 0;$gakdat[3] = 0;$mongcdat[3] = "？"; }
	if($gakdat[4]){ $gpur4 = ($gakdat[4] / $yesg) * 100;$gpur4 = sprintf("%.2f",$gpur4) * 2; } else { $gpur4 = 0;$gakdat[4] = 0;$mongcdat[4] = "？"; }
	if($gakdat[5]){ $gpur5 = ($gakdat[5] / $yesg) * 100;$gpur5 = sprintf("%.2f",$gpur5) * 2; } else { $gpur5 = 0;$gakdat[5] = 0;$mongcdat[5] = "？"; }
	if($gakdat[6]){ $gpur6 = ($gakdat[6] / $yesg) * 100;$gpur6 = sprintf("%.2f",$gpur6) * 2; } else { $gpur6 = 0;$gakdat[6] = 0;$mongcdat[6] = "？"; }
	if($gakdat[7]){ $gpur7 = ($gakdat[7] / $yesg) * 100;$gpur7 = sprintf("%.2f",$gpur7) * 2; } else { $gpur7 = 0;$gakdat[7] = 0;$mongcdat[7] = "？"; }
	if($gakdat[8]){ $gpur8 = ($gakdat[8] / $yesg) * 100;$gpur8 = sprintf("%.2f",$gpur8) * 2; } else { $gpur8 = 0;$gakdat[8] = 0;$mongcdat[8] = "？"; }
	if($gakdat[9]){ $gpur9 = ($gakdat[9] / $yesg) * 100;$gpur9 = sprintf("%.2f",$gpur9) * 2; } else { $gpur9 = 0;$gakdat[9] = 0;$mongcdat[9] = "？"; }
	if($gakdat[10]){ $gpur10 = ($gakdat[10] / $yesg) * 100;$gpur10 = sprintf("%.2f",$gpur10) * 2; } else { $gpur10 = 0;$gakdat[10] = 0;$mongcdat[10] = "？"; }
	if($gakdat[11]){ $gpur11 = ($gakdat[11] / $yesg) * 100;$gpur11 = sprintf("%.2f",$gpur11) * 2; } else { $gpur11 = 0;$gakdat[11] = 0;$mongcdat[11] = "？"; }

print <<"CANCELL";

<font color=#555555 size=5>■■■■<b>　月間アクセス調査　</b>■■■■</font><br>
過去１年の月間アクセス件数
<table border=1 cellpadding=2 width=85%><tr bgcolor=#555555>
<th bgcolor=#eeeebb width=6%>グ<br>ラ<br>フ</th>
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
<th bgcolor=#eeeebb nowrap>件数</th>
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
<th bgcolor=#eeeebb nowrap>月間</th>
<th nowrap>$mongcdat[11]月</th>
<th nowrap>$mongcdat[10]月</th>
<th nowrap>$mongcdat[9]月</th>
<th nowrap>$mongcdat[8]月</th>
<th nowrap>$mongcdat[7]月</th>
<th nowrap>$mongcdat[6]月</th>
<th nowrap>$mongcdat[5]月</th>
<th nowrap>$mongcdat[4]月</th>
<th nowrap>$mongcdat[3]月</th>
<th nowrap>$mongcdat[2]月</th>
<th nowrap>$mongcdat[1]月</th>
<th nowrap>$mongcdat[0]月</th>
</tr></table><font size=2>※　「?月」は調査データー無し</font></p>

CANCELL

}


	print "<a name=4></a>\n";
	print "<hr size=3 width=80%><p>\n";
	print "<font color=#555555 size=5>■■■■■<b>　リンク元調査　</b>■■■■■</font>\n";
	print "<br>全件数$c件 - 調査件数$refc件\n";
	print "<table border=1 width=85% cellpadding=2>\n";
	print "<tr bgcolor=#eeeebb><th nowrap width=60%>リンク元</th><th nowrap width=30% colspan=2>件数</th><th nowrap width=10%>(割合)</th></tr>\n";
	@refs = sort { $ref{$b} <=> $ref{$a} } keys(%ref);
	foreach $refkey (@refs) {
	$pur = ($ref{$refkey} / $res) * 100;$pur = sprintf("%.1f",$pur);
	if(length($refkey) > 50){ $urlche = substr($refkey,0,45);$urlche .= "･････"; } else { $urlche = $refkey; }
		if($ref{$refkey} > $refken){
		print "<tr><td nowrap bgcolor=#cccccc><a href=\"$refkey\" target=\"_blank\">$urlche</a></td><td nowrap bgcolor=#333333 align=center width=5%><font color=00ff00><b>$ref{$refkey}</b></font></td><td nowrap bgcolor=#555555 width=25%><img src=\"$bar\" width=$pur\% height=10></td><td nowrap align=center bgcolor=#ffffe7>($pur\%)</td></tr>\n";
		}
	}
	print "</table>\n";
	if($refken ne "0"){ print "<font size=2>※ $refken件以下省略</font>\n"; }
	print "</p>\n";

	print "<a name=5></a>\n";
	print "<hr size=3 width=80%><p>\n";

	print "<font color=#555555 size=5>■■■■■<b>　ホスト調査　</b>■■■■■</font>\n";
	print "<br>全件数$c件 - 調査件数$hosc件\n";
	print "<table border=1 width=85% cellpadding=2>\n";
	print "<tr bgcolor=#eeeebb><th nowrap width=10%>ホスト数</th><th nowrap width=30%>ホスト名</th><th nowrap colspan=2 width=50%>件数</th><th nowrap width=10%>(割合)</th></tr>\n";
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
	if($hosken ne "0"){ print "<font size=2>※ $hosken件以下省略</font>\n"; }
	print "</p>\n";

	print "<a name=6></a>\n";
	print "<hr size=3 width=80%><p>\n";

	print "<font color=#555555 size=5>■■■■■<b>　ブラウザ調査　</b>■■■■■</font>\n";
	print "<br>全件数$c件 - 調査件数$agec件\n";
	print "<table border=1 width=85% cellpadding=2>\n";
	print "<tr bgcolor=#eeeebb><th nowrap width=60%>ブラウザ</th><th nowrap colspan=2 width=30%>件数</th><th nowrap width=10%>(割合)</th></tr>\n";
	@agens = sort { $agen{$b} <=> $agen{$a} } keys(%agen);
	foreach $agenkey (@agens) {
	$pur = ($agen{$agenkey} / $ags) * 100;$pur = sprintf("%.1f",$pur);
	if(length($agenkey) > 50){ $ageche = substr($agenkey,0,45);$ageche .= "････)"; } else { $ageche = $agenkey; }
		if($agen{$agenkey} > $ageken){
		print "<tr><td nowrap bgcolor=#cccccc>$ageche</td><td nowrap bgcolor=#333333 align=center width=5%><font color=00ff00><b>$agen{$agenkey}</b></font></td><td nowrap bgcolor=#555555 width=25%><img src=\"$bar\" width=$pur\% height=10></td><td nowrap align=center bgcolor=#ffffe7>($pur\%)</td></tr>\n";
		}
	}
	print "</table>\n";
	if($ageken ne "0"){ print "<font size=2>※ $ageken件以下省略</font>\n"; }
	print "</p>\n";

&end;

#**************************************************************************

sub passche{

print <<"CANCELL";

<form action=./easyaccess.cgi?mode method=POST>
<table width=90% border=0 cellpadding=20><tr>
<td bgcolor=#f7f7f7>
■ <b>バスワード：</b>
<input type=password size=30 name="maspass">

<select name=mode size=1>
<option value=today>*** 本日 ***
<option value=yes>*** 昨日 ***
</select>
</td></tr></table><p>
<input type=submit value="　解析画面へ　"></form></p>
CANCELL
&end;


}

#**************************************************************************

sub end{

#スクリプト著作権表示（削除しないで下さい）
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
	@weday = ('<font color=#ff0000>(日)</font>','(月)','(火)','(水)','(木)','(金)','<font color=#0000ff>(土)</font>');
	$TIME = "$year年$mon月$mday日$weday[$wday]$hour:$min:$sec";
	$acss = $dateroot . "$mon$mday.csv";
}

sub timeget2 {
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($timec - $btim*24*60*60);
	if($year < 99){ $chri = 2000; } else { $chri = 1900; }
	$year += $chri;
	$mon = $mon + 1;
	if ($mon < 10){ $mon = "0$mon"; }
	if ($mday < 10){ $mday = "0$mday"; }
	@weday = ('<font color=#ff0000>(日)</font>','(月)','(火)','(水)','(木)','(金)','<font color=#0000ff>(土)</font>');
	$TIME = "$year年$mon月$mday日$weday[$wday]";
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
	print "月間のデーターはまだありません。<br>\n";
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

	$masse[0] = "記事ファイルを開けません。<br>データーが無いようです。";
	$masse[1] = "アクセスファイルを開けません。<br>データーが無いようです。";
	$masse[2] = "モードの指定がありません。<br>本日=...easyaccess.cgi?mode=today<br>昨日=...easyaccess.cgi?mode=yes";


print <<"CANCELL";
<table width=90% cellspacing=0 cellpadding=0 align=center bgcolor=$color3>
<tr><th nowrap>
<p>　</p><font color="$fcolor2"><b>$masse[$no]</b><p>　</p>
</th></tr></table>
CANCELL


&end;
}

