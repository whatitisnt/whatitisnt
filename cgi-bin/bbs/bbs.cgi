#!/usr/bin/perl

#<<<=============================================================================
#<<<　　『はぐれ掲示・変換派　Ver0.55』  2000.12.08
#<<<								Copyright (c) 2000.5 Tacky				     
#<<<
#<<< 設置方法構成(具体例)
#
#<<< public_html（ホームページディレクトリ）
#<<< |
#<<< |-- cgi-bin（任意のディレクトリ）
#<<<   |-- jcode.pl      (755)…(日本語ライブラリ)
#<<<   |-- hagure.cgi    (755)…(スクリプト本体)
#<<<   |-- hagure.txt    (666)…(ログファイル)
#<<<   |-- hagure.lock　　    …(ロックファイル)※スクリプト側で自動生成及び削除
#<<<   |-- xxxx.dic      (666)…(辞書ファイル)	
#<<<
#<<< ■( )内はパーミッッションの値です。
#<<< ■hagure.cgi：Perlのパス、その他の項目を修正、アスキーモードでアップロード。
#<<< ■hagure.txt：空のファイルを作成し、アスキーモードでアップロード。
#<<< ■XXXX.dic　：各自辞書ファイルを作成し、アスキーモードでアップロード。
#<<<   　※辞書の作成方法：エディタで作成してください。
#<<<          辞書のイメージは、「変換前文章」＋「半角スペース」＋「変換後文章」
#<<<        ex.
#<<<           おはよう おはぁー!
#<<<           おやすみ おにゃー!
#<<<           バイバイ （＾０＾）／～～ｓｅｅｙｏｕ！
#<<< ■hagure.lock：各自で用意する必要ありません。
#<<<
#<<< >>> Update-History...
#<<<
#<<<	2000.12.08  >>　またまたﾌｧｲﾙﾛｯｸが解除されない場合がある不具合修正
#<<<	2000.07.12  >>　スクロール処理に不具合・ﾌｧｲﾙﾛｯｸが解除されない場合がある不具合修正
#<<<	2000.06.17  >>　Apache+Netscape文字化け対応・ロック処理見直し
#<<<=============================================================================

require './jcode.pl';

$url 				= 'http://www.untitled2001.com/';			#<<<戻り先ＵＲＬ
$script 			= './bbs.cgi';									#<<<このＣＧＩの名前を指定
$logfile 			= './bbs.txt';									#<<<ログファイルの名前を指定
$lockfile			= './bbs.lock';									#<<<ロックファイルの名前を指定
$method 			= 'POST';											#<<<METHODの指定(POST又はGET)

$convert			= 0 ;												#<<<変換機能を使う？(0:no 1:yes)
#<<<辞書ファイルの名前を指定（上記の変換機能を「使う」にした場合のみ修正対象。「使わない」場合は修正不要です）
#■辞書が１つの場合の指定方法
#  @dicfile = ('./xxxx.dic');
#■辞書が複数の場合の指定方法
#  @dicfile = ('./xxxx.dic','./yyyyy.dic','./zzzzz.dic');
#  @dicname = ('Ｘ辞書','Ｙ辞書','Ｚ辞書');

@dicfile = ('./hagure.dic');
@dicname = ('テスト変換');

$titlename			= 'untitled2001 bbs';								#<<<タイトルを指定
$titlelogo	 		= '../../bbsimg/title.gif';				#<<<タイトル画像を指定
$bgcolor 			= '#000000';										#<<<背景色を指定
$backpicture	 	= '';												#<<<背景画像を指定（使用しない場合は、''で良い)

$tbgcolor 			= '#ff0000';										#<<<入力フォームの背景色を指定
$ftextcolor 		= '#ffffff';										#<<<入力フォームの文字色を指定
$stextcolor 		= '#ffffff';										#<<<削除フォームの文字色を指定

$msg_cellbgcolor 	= '#cccccc';										#<<<メッセージ部分のタイトル部セル背景色を指定
$msg_cellbgcolor2 	= '#999999';										#<<<メッセージ部分のメッセージ部セル背景色を指定

$tcolor				= "#000066";								# 文字色
$linkcolor			= "#cc6600";								# リンク色（未読リンク）
$vlinkcolor			= "#666666";								# リンク色（既読リンク）
$alinkcolor		 	= "#ff3300";								# リンク色（押した時）
$hlinkcolor			= '#ff0000';								#マウスをポイントした際のリンクアンダーラインの色（IEのみ)

$icon_hp	 		= '../../bbsimg/home.gif';				#<<<ＨＰリンク用画像を指定
$icon_back			= '../../bbsimg/back.gif';				#<<<BACK用画像を指定
$icon_center			= '../../bbsimg/center.gif';			#<<<CENTER用画像を指定
$icon_next			= '../../bbsimg/next.gif';				#<<<NEXT用画像を指定
$icon_close			= '../../bbsimg/close.gif';				#<<<CLOSE用画像を指定

$row				= 4 ;												#入力フォーム・メッセージ欄の行数
$col				= 40;												#入力フォーム・メッセージ欄の文字数

$datamax 			= 150 ;												#<<<最大データ保存件数
$pagemax 			= 10 ;												#<<<１ページ内に表示する件数
$password 			= 'pass2001';											#<<<メンテナンス用パスワード（管理者用）

$tablesz			= '50%';											#<<<ログ表示部テーブル横幅

$tag				= 'yes';											#タグ許可(yes,no)

#掲示板荒らし対策。排除したいプロバのアドレスを設定して下さい。
#　"xxx?.com"とした場合、"xxx1.com","xxx2.com"等、「？」の部分が文字列１つと判断します
#  "xxx*.com"とした場合、"xxx1.com","xxx12345.com等、「＊」の部分が０個以上の文字列と判断します。
@DANGER_LIST=("xxx.com","yyy.com","zzz*.or.jp");

#掲示板荒らし対策その２。メッセージ最大文字数を指定。特に設定しない場合は、''として下さい。
$maxword 			= '2000' ;

#投稿時のパスワードをcrypt関数を使用する（暗号化）
#crypt関数が利用出来ない場合もありますので、投稿時にエラーになる場合は、「0:使用しない」にして下さいね。
$ango				= 1 ;												#0:使用しない 1:使用する　（推奨：１：使用する）

$pt					= '9pt';									#全体のフォントサイズ（pt指定以外何があるのか、僕知らない。(^^ゞ）

#フォームＣＳＳ設定　※使用しない場合は、$css_style = "";として下さい
$css_style = <<"EOM";
 STYLE="font-size:$pt;color:#666666;border:1 dotted #000066;" onFocus="this.style.backgroundColor='#cccccc'" onBlur="this.style.backgroundColor='#FFFFFF'" onMouseOver="this.focus()"
EOM

#<<<　ここから下はいじらない方がいいです。
@errtag = ('table','meta','form','!--','embed','html','body','tr','td','th','a');		#デンジャラ～なタグ

if ( $convert == 1 && @dicfile < 1 ) { &error("辞書ファイルが設定されていません"); }

###############################################################################
#### Main Process  START  #####################################################
###############################################################################
if ($ENV{'HTTP_USER_AGENT'} !~ /MSIE/i) { $css_style = "" ; }		#Netscape-CSS対応
#<<<システム日時・時刻取得
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
$year = sprintf("%02d",$year + 1900);
$month = sprintf("%02d",$mon + 1);
$mday = sprintf("%02d",$mday);
$hour = sprintf("%02d",$hour);
$min = sprintf("%02d",$min);
if ( substr($month,0,1) == 0 )	{	$month =~ s/0/ /;	}
if ( substr($day,0,1) == 0 )	{	$day =~ s/0/ /;	}
$week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat') [$wday];
$today = "$month月$mday日($week) $hour時$min分";

&cookieget;												#<<<COOKIEの取得
&decode ;												#<<<デコード
if ( $FORM{'action'} eq "maintenance" ) {      			#<<<"処理"がメンテナンスの場合
	&update; 
}	elsif	( $FORM{'action'} eq "update" )		{		#<<<ログファイル更新（編集時）
	&update ;
}	else	{
	if	( $FORM{'action'} eq 'regist' )	{
		&regist ;
		print "Location: $script?\n\n";
	}
	&header ;											#<<<htmlヘッダー出力
	&forminput ;										#<<<入力フォーム表示
}
&view ;													#<<<ログ表示
&footer ;												#<<<htmlフッター出力
exit;
###############################################################################
#### Main Process  END  #######################################################
###############################################################################

###<--------------------------------------------------------------
###<---   デコード＆変数代入
###<--------------------------------------------------------------
sub decode{	
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	} else { $buffer = $ENV{'QUERY_STRING'}; }
	@pairs = split(/&/,$buffer);
	foreach $pair (@pairs) {
		($name, $value) = split(/=/, $pair);
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		if ($tag eq 'yes') {
	        #危険なタグは禁止!!!
			foreach ( @errtag )	{
				if ($value =~ /<$_(.|\n)*>/i) {	 &error("使用出来ないタグが入力されています");	}
			}
		}	else	{
			$value =~ s/</&lt;/g;											
			$value =~ s/>/&gt;/g;
		}
		$value =~ s/\,/，/g;
		&jcode'convert(*value,'sjis');
		$FORM{$name} = $value;
	}
	$FORM{'hp'}   =~ s/^http\:\/\///;
}
###<--------------------------------------------------------------
###<---   入力フォーム
###<--------------------------------------------------------------
sub forminput { 
	print "<table cellpadding=0 cellspacing=0 border=0 align=center><tr>\n";
	print "<td width=33% align=center>\n";
	print "<img src=\"$titlelogo\">\n";
	print "</td></tr></table><center><br>\n";
	print "<form action=$script method=$method>\n";
	print "<input type=hidden name=\"action\" value=\"regist\">\n";
	print "<table width=50% border=0 cellspacing=1 cellpadding=1 bgcolor=#000066>\n";
	print "<tr><td>\n";
	print "<table width=100% border=0 cellspacing=0 cellpadding=2>\n";
	print "<tr><td bgcolor=$tbgcolor><font  color=\"$ftextcolor\">&nbsp;Name</font></td>\n";
	print "<td bgcolor=$tbgcolor><input type=text name=\"name\" size=30 value=\"$COOKIE{'nm'}\" $css_style></td></tr>\n";
	print "<tr><td bgcolor=$tbgcolor><font  color=\"$ftextcolor\">&nbsp;Email</font></td>\n";
	print "<td bgcolor=$tbgcolor><input type=text name=\"email\" size=30 value=\"$COOKIE{'em'}\" $css_style></td></tr>\n";
	print "<tr><td bgcolor=$tbgcolor><font  color=\"$ftextcolor\">&nbsp;Homepage</font></td>\n";
	print "<td bgcolor=$tbgcolor><input type=text name=\"hp\" size=30 value=\"http://$COOKIE{'hp'}\" $css_style></td></tr>\n";
	print "<tr><td bgcolor=$tbgcolor><font  color=\"$ftextcolor\">&nbsp;Title</font></td>\n";
	print "<td bgcolor=$tbgcolor><input type=text name=\"subject\" size=30 $css_style></td></tr>\n";
	print "<tr><td bgcolor=$tbgcolor><font  color=\"$ftextcolor\">&nbsp;Message</font></td>\n";
	print "<td bgcolor=$tbgcolor><textarea name=\"comment\" cols=$col rows=$row $css_style></textarea></td></tr>\n";
	if ( $convert == 1 )	{
		print "<tr><td bgcolor=$tbgcolor><font  color=\"$ftextcolor\">&nbsp;Convert!!</font></td>\n";
		print "<td bgcolor=$tbgcolor>";
		print "<select name=henshin>\n";
		print "<option value=no selected>変換しない\n";
		print "<option value=99 selected>ランダム変換\n";
		foreach ( 0..$#dicfile )	{
			print "<option value=$_>$dicname[$_]\n";
		}	 
		print "</select>&nbsp;&nbsp;&nbsp;&nbsp;\n";
	}	else	{
		print "<tr><td bgcolor=$tbgcolor>&nbsp;</td>\n";
		print "<td bgcolor=$tbgcolor>";
	}
	print "<input type=submit value=Submit>\n";
	print "&nbsp;&nbsp;<input type=reset value=Clear>\n";
	print "&nbsp;&nbsp;<font  color=\"$ftextcolor\">Password</font><input type=password name=pass size=6 value=\"$COOKIE{'ps'}\" $css_style>\n";
	print "</td></tr>\n";
	print "</table>\n";
	print "</td></tr></table>\n";
	print "</form></center>\n";
}
###<--------------------------------------------------------------
###<---   HTMLヘッダー書き出し
###<--------------------------------------------------------------
sub header { 
	print "Content-type: text/html; charset=Shift_JIS\n\n";
	print "<html>\n<head>\n";
	print "<META HTTP-EQUIV=\"Content-type\" CONTENT=\"text/html; charset=x-sjis\">\n";
	print "<title>$titlename</title>\n";
	#<<<CSS START>>>
	print "<style type=\"text/css\">\n";
	print "<!--\n";
	print "a:link    {font-size: $pt; text-decoration:none; color:$linkcolor }\n";		
	print "a:visited {font-size: $pt; text-decoration:none; color:$vlinkcolor }\n";	
	print "a:active  {font-size: $pt; text-decoration:none; color:$alinkcolor }\n";	
	print "a:hover   {font-size: $pt; text-decoration:underline; color:$hlinkcolor; }\n";
	print "body,tr,td { font-size: $pt;}\n";
	print "-->\n";
	print "</style>\n";
	#<<<CSS END>>>
	print "</head>\n";
	if ($backpicture) { $set = "background=\"$backpicture\""; if ( $bgcolor ) { $set .= " bgcolor=\"$bgcolor\"" ; }	}
	elsif ($bgcolor )	{ $set = "bgcolor=\"$bgcolor\""; }
	print "<body $set text=$tcolor link=$linkcolor vlink=$vlinkcolor alink=$alinkcolor>\n";
}
###<--------------------------------------------------------------
###<---   HTMLフッダー書き出し
###<--------------------------------------------------------------
sub footer { 
	print "<p align=right><a href=\"javascript:window.close()\"><img src=\"$icon_close\" border=0></a></p>\n";
	print "</body></html>\n";
}
###<--------------------------------------------------------------
###<---   ログファイル読み込み
###<--------------------------------------------------------------
sub	dataread	{
	#<<<ログ読み込み
	if ( !(open(IN,"$logfile")))	{	&error("ログファイル($logfile)のオープンに失敗しました");	}
	@LOG = <IN>;
	close(IN);
}
###<--------------------------------------------------------------
###<---   ログ表示
###<--------------------------------------------------------------
sub	view	{
	&dataread ;												#<<<ログ読み込み
	print "<center><hr width=80% size=1 noshade color=#000000>\n";

	#表示対象ページの先頭データ件数を算出
	$dm = @LOG;
	if ( $dm % $pagemax == 0) {		$p = $dm / $pagemax ;
	}	else	{		$p = $dm / $pagemax + 1;	}			
	$p = sprintf("%3d",$p);
	if ( $FORM{'page'} eq "NEXT" )	{
		if ( $FORM{'disppage'} == 0 ) { $FORM{'disppage'} = 1 }	;
		$d = ($FORM{'disppage'} + 1) * $pagemax - $pagemax ; 	
		$FORM{'disppage'} = $FORM{'disppage'} + 1 ;
	}	elsif	( $FORM{'page'} eq "BACK" ) 	{
		$d = ($FORM{'disppage'} - 1) * $pagemax - $pagemax ; 	
		$FORM{'disppage'} = $FORM{'disppage'} - 1 ;
	}	else	{
		$d = 0	;
		$FORM{'disppage'} = 1 ;
	}
	$z = 1 ;
	for ( $i = $d ; ( $z <= $pagemax ) && ( $i < $dm ); $i++ )	{ 
		($no,$name,$email,$hp,$title,$comment,$regdate,$pass,$conv,$hst,$d2) = split(/,/,$LOG[$i]);
		chop $d2 ;
		print "<br>\n";
		print "<table width=$tablesz border=0 cellspacing=0 cellpadding=1 bgcolor=#000000>\n";
		print "<tr><td>\n";
			print "<table width=100% border=0 cellspacing=1 cellpadding=5>\n";
			print "<tr><td bgcolor=\"$msg_cellbgcolor\"><font  color=\"$textcolor\">\n";
			$no = sprintf("%d",$no);
			print "<font size=-1>";
			print "[$no]　";
			print "</font>\n";
			if ( $email ne '' )	{
				print "<a href=mailto:$email>$name</a>\n";
			}	else	{
				print "$name";
			}
			print "<font size=-1>&nbsp;&nbsp;";
			if ( $hp ne '' )	{
				print "<a href=http://$hp target=_blank>";
				print "[URL]" if ( !($icon_hp) ) ;
				print "<img src=$icon_hp border=0 align=absmiddle>" if ( $icon_hp );
				print "</a>";
			}
			print "&nbsp;&nbsp;&nbsp;";
			print "$regdate</font>\n";
			if ( $convert == 1 && @dicfile > 1 )	{
				print "<font size=-1>";
				print "&nbsp;&nbsp;&nbsp;&nbsp;\n";
				print "($dicname[$conv])\n"	if ( $conv ne 'no' );
				print "(変換無し)\n"	if ( $conv eq 'no' );
				print "</font>\n";
			}
			print "<br>\n";
			if ( $title ne '' )	{
				print "◆$title";
			}	else	{
				print "◆無題";
			}
			print "</td></tr>\n";
			print "<tr><td bgcolor=\"$msg_cellbgcolor2\"><font  color=\"$textcolor\">$comment</font></td></tr>\n";
			print "</table>\n";
		print "</td></tr></table>\n";
		$z++;
	}
	print "<br><table><tr><td>\n";
	if ( $FORM{'disppage'} != 0 && $FORM{'disppage'} !=1)	{	
		print "<form action=$script method=$method>\n";
		print "<input type=hidden name=\"disppage\" value=$FORM{'disppage'}>\n";
		print "<input type=submit>\n" if ( !($icon_back) ) ;	
		print "<input type=image src=$icon_back name=\"page\" value=BACK>\n" if ( $icon_back ) ;	
		print "<input type=hidden name=\"page\" value=BACK>\n";
		print "</form>\n";
	}
	print "</td><td>\n";
	print "<img src=\"$icon_center\">\n";
	print "</td><td>\n";
	if ( $FORM{'disppage'} + 1 <= $p )	{
		print "<form action=$script method=$method>\n";
		print "<input type=hidden name=\"disppage\" value=$FORM{'disppage'}>\n";
		print "<input type=submit>\n" if ( !($icon_next) ) ;	
		print "<input type=image src=$icon_next name=\"page\" value=NEXT>\n" if ( $icon_next ) ;	
		print "<input type=hidden name=\"page\" value=NEXT>\n";
		print "</form>\n";
	}
	print "</td></table><br><hr width=80% size=1 noshade color=#000000>\n";

	print "<div align=right><form action=\"$script\" method=\"$method\"><font color=\"$stextcolor\">\n";
	print "No.<input type=text name=\"no\" size=3>\n";
	print "pass.<input type=password name=\"pass\" size=8>\n";
	print "<input type=hidden name=\"action\" value=\"maintenance\">\n";
	print "<input type=submit name=proc value=\"delete\">\n";
	print "</font></form></div>\n";	

}
###<--------------------------------------------------------------
###<---   ログ出力
###<--------------------------------------------------------------
sub	regist	{
	# ホスト名を取得
	$host  = $ENV{'REMOTE_HOST'};		$adr  = $ENV{'REMOTE_ADDR'};
	if ($host eq "" || $host eq "$adr") {
		($p1,$p2,$p3,$p4) = split(/\./,$adr);
		$temp = pack("C4",$p1,$p2,$p3,$p4);			$host = gethostbyaddr("$temp", 2);
		if ($host eq "") { $host = $adr; }
	}
	#掲示板荒らし対策
	foreach $buf(@DANGER_LIST){
		if ( $buf ) {
			# パターンマッチを変換
			$buf=~ s/\./\\./g;		$buf=~ s/\?/\./g;		$buf=~ s/\*/\.\*/g;
			if($host =~ /$buf/gi){	&error("\申\し\訳ありません。<br>あなたのプロバイダーからは投稿できませんでした． ");	}
		}
	}
	if ( $maxword ne '' && (length($FORM{'comment'}) > $maxword))	{	&error("メッセージは$maxword文字までしか登録出来ません。");	}
	if ( $FORM{'name'} eq '')	{	&error("お名前を入力して下さい。");	}
	if ( $FORM{'comment'} eq '')	{	&error("メッセージは省略出来ません。");	}

	&filelock ;	#ファイルロック
	&dataread ;												#<<<ログ読み込み

	$FORM{'comment'} =~ s/\r\n/<br>/g;	$FORM{'comment'} =~ s/\r|\n/<br>/g;	
	if ( $FORM{'henshin'} ne 'no' && $convert == 1 )	{	$comment = &dicconvert($FORM{'comment'});	}
	else	{	$comment = $FORM{'comment'} ;	}

	$dcnt = @LOG;
	if ($dcnt >= $datamax) {	pop(@LOG);	}
	if ( $dcnt < 1 )	{
		$no = 1;											#１件目
	}	else	{
		($no,$dummy) = split(/,/,$LOG[0]);					#最新記事No取得
		$no++;
	}
	# パスワードの暗号化（crypt関数使用））
	if ($FORM{'pass'} ne "") { &pass_enc($FORM{'pass'}); }	else	{ $pass = '' ; }
	unshift(@LOG,"$no,$FORM{'name'},$FORM{'email'},$FORM{'hp'},$FORM{'subject'},$comment,$today,$pass,$FORM{'henshin'},$host,\n");
	if ( !(open(OUT,">$logfile")))	{	&fileunlock ;	&error("ログファイル($logfile)のオープンに失敗しました");	}
	print OUT @LOG;
	close(OUT);

	&fileunlock ;	#ファイルロック解除

	#COOKIE設定
	&cookieset ;

}
###<--------------------------------------------------------------
###<---   ログファイル更新
###<--------------------------------------------------------------
sub update {
	if ( $FORM{'pass'} eq "")	{	&error("パスワードを入力して下さい。");	}

	&filelock ;	#ファイルロック
	&dataread ;												#<<<ログ読み込み

    foreach (@LOG) {
		($no,$name,$email,$hp,$title,$comment,$regdate,$pass,$conv,$hst,$d2) = split(/,/,$_);
		if ( $FORM{'no'} eq $no)	{	
			if ($FORM{'pass'} ne $password && (&pass_dec($pass))) { &fileunlock ;	&error("パスワードが違います。"); }
		}	else	{
			push(@new,$_);	
		}
	}
	if ( !(open(OUT,">$logfile")))	{	&fileunlock ;	&error("ログファイル($logfile)のオープンに失敗しました");	}
	print OUT @new;
	close(OUT);

	&fileunlock ;	#ファイルロック解除

	print "Location: $script?\n\n";
}
###<--------------------------------------------------------------
###<---   エラー処理
###<--------------------------------------------------------------
sub error {
	&header ;
	print "<br><br>$_[0]\n";
	&footer;
	exit;
}
###<-------------------------------------------------------------
###<---   クッキー取得
###<--------------------------------------------------------------
sub cookieget	{
	$cookies = $ENV{'HTTP_COOKIE'};
	@pairs = split(/;/,$cookies);
	foreach $pair (@pairs) {
		($name, $value) = split(/=/, $pair);
		$name =~ s/ //g;
		$DUMMY{$name} = $value;
	}
	@pairs = split(/,/,$DUMMY{'hagure'});
	foreach $pair (@pairs) {
		($name, $value) = split(/:/, $pair);
		$COOKIE{$name} = $value;
	}
}
###<-------------------------------------------------------------
###<---   クッキー設定
###<--------------------------------------------------------------
sub cookieset { 
	($secg,$ming,$hourg,$mdayg,$mong,$yearg,$wdayg,$ydayg,$isdstg)
		=gmtime(time + 30*24*60*30);
	$yearg += 1900 ;
	if ($yearg < 10)  { $yearg = "0$yearg"; }
	if ($secg  < 10)  { $secg  = "0$secg";  }
	if ($ming  < 10)  { $ming  = "0$ming";  }
	if ($hourg < 10)  { $hourg = "0$hourg"; }
	if ($mdayg < 10)  { $mdayg = "0$mdayg"; }
	$mong = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')[$mong];
	$youbi = ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday')[$wdayg];
	$date_gmt = "$youbi, $mdayg\-$mong\-$yearg $hourg:$ming:$secg GMT";
	$cook="nm\:$FORM{'name'},em\:$FORM{'email'},hp\:$FORM{'hp'},ps\:$FORM{'pass'}";
	print "Set-Cookie: hagure=$cook; expires=$date_gmt\n";
}
###<-------------------------------------------------------------
###<---   辞書変換
###<--------------------------------------------------------------
sub dicconvert { 
	#<<<辞書読み込み

	if ( $FORM{'henshin'} == 99 )	{
		srand(time ^ ($$ + ($$ << 15)));
		$FORM{'henshin'}	= int(rand(@dicname)) ;
	}

	$dicf = @dicfile[$FORM{'henshin'}];
	if ( !(open(IN,"$dicf")))	{	&fileunlock ;	&error("辞書ファイルのオープンに失敗しました");	}
	@dic = <IN>;
	close(IN);
	###<-----  terra氏(http://www2q.biglobe.ne.jp/~terra/cgi/)の辞書変換ルーチンを参考にさせて頂きました-----
	local($string) = $_[0];
	$dic_count = @dic;
	if ($dic_count > 0) {
		foreach $line (@dic) {
			($a,$b) = split(/ /,$line);
			chop($b);			$stpos = 0;
			while (index($string, $a, $stpos) >= $stpos) {
				$pos = index($string, $a, $stpos);	$len = length($a);
				substr($string, $pos, $len) = $b;	$len = length($b);
				$stpos = $pos + $len;
			}
		}
	}
	$string;
}
###<--------------------------------------------------------------
###<---   ファイルロック設定
###<--------------------------------------------------------------
sub filelock {
	$sw = 0;
	foreach (1 .. 5) {
		if (-e $lockfile) { sleep(1); }
		else {		open(LOCK,">$lockfile");	close(LOCK);	$sw = 1;	return;	}
	}
	&error("只今他の方が書き込み中です。ブラウザの「戻る」で戻って再度登録を行って下さい。"); 
}
###<--------------------------------------------------------------
###<---   ファイルロック解除
###<--------------------------------------------------------------
sub fileunlock {
	if (-e $lockfile) { unlink($lockfile); }
}
###<-------------------------------------------------------------
###<---   パスワード暗号化
###<--------------------------------------------------------------
sub pass_enc {
	if ( $ango == 1 ) {		$pass = crypt($_[0], $_[0]);
	}	else	{		$pass = $_[0];	}
}
###<-------------------------------------------------------------
###<---   パスワードチェック
###<--------------------------------------------------------------
sub pass_dec {
	if ( $ango == 1 ) {
		if ($_[0] ne '' && ( crypt($FORM{'pass'}, $_[0]) eq $_[0]) )  {		return 0 ;		}
	}	else	{
		if ($FORM{'pass'} eq $_[0]) {	return 0 ;	}
	}
	return 1;
}
