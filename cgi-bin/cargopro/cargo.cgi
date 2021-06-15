#!/usr/bin/perl

require "./setup.pl";

#時刻取得
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
@wday_array = ('SUN','MON','TUE','WED','THU','FRI','SAT');
$date_now = sprintf("%01d\/%01d(%s)%02d\:%02d",$mon +1,$mday,$wday_array[$wday],$hour,$min);

#データの読み込み
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

if ($in{'_file'} eq '') { &error('設定エラー','使用する商品ファイルが設定されていません。'); }
if (!-e "$base_dir$in{'_file'}\.csv") { &error('設定エラー',"商品設定ファイル$in{'_file'}が見つかりません。"); }

$lockfile = $tmp_dir . "$in{'_file'}\.lock";

$od_check = (eval { opendir(DIR,$base_dir); }, $@ eq "");
if (!$od_check) { &error("エラー","ファイル一覧が取得できません。"); }

($cookie_name,$els) = split(/\./,$in{'_file'},2);
@newls = ();

@list = readdir(DIR); # ファイル名の抽出

foreach $file (@list) {

	next if -d $file;

	if ($file =~ /^$cookie_name\./) {

		#商品設定ファイルを開く(取扱商品データを読み込む)
		if (!open(FILE,"$base_dir$file")) { &error('エラー',"商品ファイル$fileが読み出せません。"); }

		#ファイルハンドル'FILE'から１行ずつデータを読む
		while (<FILE>) {

			#無視
			s/\t//g;
			s/\n//g;

			#行頭がシャープまたは空行の場合は次へ
			if (/^#/) { next; }
			if (/^$/) { next; }

			#データ抽出
			($code,$name,$tanka,$tax,$rem,$url,$zaiko,$type) = &DecodeCSV($_);

			$name{$code} = $name;
			$tanka =~ s/\,//g; $tanka =~ s/\\//g; $tanka{$code} = $tanka;
			$taxrate = $tax;
			$rem{$code} = $rem;
			$url{$code} = $url;
			$zaiko{$code} = $zaiko;
			$type{$code} = $type;

			if ($taxrate == -3) { $taxm{$code} = "(税込)"; }
			elsif ($taxrate == -2) { $taxm{$code} = "(不課税)"; }
			elsif ($taxrate == -1) { $taxm{$code} = "(非課税)"; }
			else { $taxm{$code} = ""; }

			if ($taxrate =~ /\-/) { $taxrate = 0; } # 税の設定値に-があれば0%にする
			$tax{$code} = $taxrate;
		}
		close(FILE);
	}
}

close(DIR);

#商品コードをキーとした%orderに数量を格納
while (($key,$val) = each %in) {

	if ($key =~ /X(.+)X/) { $code = $1; }

	#削除する商品コードを取得
	if ($in{'_action'} eq 'delete') {

		if ($key =~ /X(.+)X/) { $delete_id = $1; last; }
	}
	#商品コードが所定の形式で入力され、数量に0以外の数字が指定されている場合に処理
	elsif ($val =~ /\d+/ && $val != 0) {

		if ($key =~ /X(.+)X/) {

			$code = $1;
			if ($name{$code} eq '') { &error("エラー","商品コード$codeが商品設定ファイル$in{'_file'}に存在していない可能\性があるので選択できません。","管理者にお問い合わせください。"); }
			$w = 1; $order{$code} = $val;
		}
	}
	elsif ($key =~ /X(.+)X/ && $val =~ /\D/) { &error("エラー","商品コード$codeの数量が半角数字以外で指定されています。","半角数字で入力してください。"); }
}

#クッキーの取得
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

#削除処理
if ($in{'_action'} eq 'delete') {

	#バスケットファイルを開く
	if (!open(ORDER,"$tmp_dir$in{'_order'}\.bkt")) { &error("何も選択されていません。"); }
	@base = <ORDER>;
	close(ORDER);

	@new = grep(!/^.+\t($delete_id)\t/,@base);

	if (!@new) { $delall = 1; unlink "$tmp_dir$in{'_order'}\.bkt"; }
	else {
		if (!open(FILE,"> $tmp_dir$in{'_order'}\.bkt")) { &error("設定エラー","バスケットファイルに再記録できません。"); }
		print FILE @new;
		close(FILE);
	}
}

#注文フォーム
elsif ($in{'_action'} eq 'mailform') { &mailform; }

#送信フォーム
elsif ($in{'_action'} eq 'mail') { &mail; }

#登録処理
elsif ($w) {

	if ($COOKIE{'OrderNo'} eq '') {

		$COOKIE{'OrderNo'} = sprintf("%04d%02d%02d%02d%02d%02d",$year +1900,$mon +1,$mday,$hour,$min,$sec);

		#新規処理
		if (!open(FILE,"> $tmp_dir$COOKIE{'OrderNo'}\.bkt")) { &error("設定エラー","作業ディレクトリが正しく設定されていません。"); }
	}
	else {
		#追加処理
		if (!open(FILE,">> $tmp_dir$COOKIE{'OrderNo'}\.bkt")) { &error("設定エラー","作業ディレクトリが正しく設定されていません。"); }
	}

	#商品コードと数量をファイルに記録
	while (($code,$kazu) = each %order) { print FILE "$in{'_file'}\t$code\t$kazu\n"; }

	close(FILE);
	chmod(0666,"$tmp_dir$COOKIE{'OrderNo'}\.bkt");
}

#バスケット一時ファイルの一覧
$od_check = (eval { opendir(DIR,$tmp_dir); }, $@ eq "");
if (!$od_check) { &error("エラー","opendir()に致命的なエラーが発生しました。"); }
@ls = readdir(DIR);
close(DIR);

#残存した一時ファイルを削除
($secg,$ming,$hourg,$mdayg,$mong,$yearg,$wdayg,$ydayg,$isdstg) = gmtime(time - 2*24*60*60);
$limit = sprintf("%04d%02d%02d%02d%02d%02d",$yearg +1900,$mong +1,$mdayg,$hourg,$ming,$secg);

foreach $file (@ls) {

	next if $file eq '.';
	next if $file eq '..';
	next if -d $file;
	if ($file =~ /(\d+)\.bkt/) { if ($1 < $limit) { unlink "$tmp_dir$file"; }}
}

#セットするクッキーの内容
if ($delall) { $set_cookie = ""; }
else { $set_cookie = "OrderNo\:$COOKIE{'OrderNo'}"; }

#識別クッキーの設定
print "Set-Cookie: $cookie_name=$set_cookie\n";

#画面出力開始
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

#バスケットファイルを開く
if (open(ORDER,"$tmp_dir$COOKIE{'OrderNo'}\.bkt")) {

	print <<"EOF";
	<table><tr><td>$msg_top</td></tr></table>
	<form method=POST action="cargo.cgi">
	<table border="1" bordercolor="#FFFFFF" cellspacing="0" cellpadding="4">
	<tr>
	<th><font size=+1></font>　</th>
	<th align=left><font size=+1>TOP SIDE</font></th>
	<th align=left><font size=+1>BOTTOM SIDE</font></th>
	<th><font size=+1>単価(円)</font></th>
	<th><font size=+1>数量(本)</font></th>
EOF
	if ($taxps) { #消費税を処理する場合

		print <<"EOF";
		<th><font size=+1>税別計(円)</font></th>
		<th><font size=+1>消費税(円)</font></th>
		<th><font size=+1>税込計(円)</font></th>
EOF
	}
	else {
		print <<"EOF";
		<th><font size=+1>小計(円)</font></th>
EOF
	}

	print <<"EOF";
	<th><font size=+1>取消</font></th>
	</tr>
EOF
	#集計
	&cal1;

	foreach $code (sort keys %list) { # 商品コード順
#	foreach $code (sort { $list{$b} <=> $list{$a} } keys %list) { # 数量が多い順

		#集計
		&cal2;

		#商品名と備考中のコロンを改行に変換
		$name{$code} =~ s/\:/<br>/g;
		$rem{$code} =~ s/\:/<br>/g;

		$zaiko_mes = '';
		if ($zaiko{$code} ne '') {

			if ($zaiko{$code} == 0) { $zaiko_err = 1; $zaiko_mes = '<br><font size=-1>在庫無し！(一旦取消して下さい)</font>'; }
			if ($list{$code} > $zaiko{$code}) { $zaiko_err = 1; $zaiko_mes = '<br><font size=-1>在庫不足！(一旦取消して下さい)</font>'; }
		}

		$c++;
		if ($c % 2) { $bg = "#ffeedd"; } else { $bg = "#ffffff"; } #１行おきにセルの背景色を替える

		print <<"EOF";
		<tr>
		<td align=left><font color="#ffe600">$code</font></td>
		<td align=left><font color="#ffe600">$rem{$code}</font></td>
		<td align=left><font color="#ffe600">$name{$code}</font></td>
		<td align=right><font color="#ffe600">$tanka2</font></td>
		<td align=right><font color="#ffe600">$kazu2$zaiko_mes</font></td>
EOF
		if ($tax == 0) { $tax2 = ""; } # 消費税率が0%の場合は表示しない

		if ($taxps) {

			print <<"EOF";
			<td align=right><font color="#ffe600">$kei2</font></td>
			<td align=right><font color="#ffe600" size=-1>$taxm{$code}</font> <font color="#ffe600">$tax2</font></td>
EOF
		}

		print <<"EOF";
		<td align=right><font color="#ffe600">$kei2_and_tax</font></td>
		<td><input type=submit name="X$code\X" value="取消"></td>
		</tr>
EOF
	}

	close(ORDER);

	$taxs = int($taxs);
	$gokei = int($gokei);

	#桁カンマ挿入処理
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
		<h3>在庫不足の商品が選択されているので注文できません。</h3>
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
else { print "<h3>何も選択されていません。</h3>\n"; }

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

	#同じ商品があれば合算する
	foreach (<ORDER>) {

		s/\n//;
		($target_file,$code,$kazu) = split(/\t/,$_,3);
		$list{$code} += $kazu;
		$target_file{$code} = $target_file;
	}
}

sub cal2 {

	#計＝数量×単価
	$kei = $kei2 = $list{$code} * $tanka{$code};
	1 while $kei2 =~ s/(.*\d)(\d\d\d)/$1,$2/g;

	$kazu2 = $list{$code};
	$tanka2 = $tanka{$code};
	1 while $kazu2 =~ s/(.*\d)(\d\d\d)/$1,$2/g;
	1 while $tanka2 =~ s/(.*\d)(\d\d\d)/$1,$2/g;

	if ($taxps) {

		#税＝計×税率÷100
		$tax = $kei * $tax{$code} / 100;
		$tax2 = int($tax);
		1 while $tax2 =~ s/(.*\d)(\d\d\d)/$1,$2/g;

		#税込計＝計＋税
		$kei_and_tax = $kei + $tax;
		$kei2_and_tax = int($kei_and_tax);
	}
	else { $kei_and_tax = $kei2_and_tax = $kei; $taxmes = '(税込)'; }

	1 while $kei2_and_tax =~ s/(.*\d)(\d\d\d)/$1,$2/g;

	#合算
	$keis += $kei;
	$gokei += $kei_and_tax;
	$taxs += $tax;
	$kazuall += $list{$code};
}

sub mailform {

	#訪問販売法での広告表示義務事項ファイルを開く
	if (!open(FILE,"$base_dir$hanbai")) { &error('エラー',"訪問販売法での広告表示義務事項ファイルが読み出せません。"); }
	@HANBAI = <FILE>;
	close(FILE);

	#受注フォームファイルを開く
	if (!open(FILE,"$base_dir$juchu")) { &error('エラー',"受注フォームファイルが読み出せません。"); }
	@JUCHU = <FILE>;
	close(FILE);

	#画面出力開始
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
	<h2>ご注文フォーム</h2>
EOF

	#バスケットファイルを開く
	if (open(ORDER,"$tmp_dir$COOKIE{'OrderNo'}\.bkt")) {

		print <<"EOF";
		<form method=POST action="cargo.cgi" name="kounyu">
		<table border="1" bordercolor="#FFFFFF" cellspacing="0" cellpadding="4">
		<tr>
		<th><font size=+1></font>　</th>
		<th align=left><font size=+1>TOP SIDE</font></th>
		<th align=left><font size=+1>BOTTOM SIDE</font></th>
		<th><font size=+1>単価(円)</font></th>
		<th><font size=+1>数量(本)</font></th>
EOF
		#消費税を処理する場合
		if ($taxps) {

			print <<"EOF";
			<th><font size=+1>税別計(円)</font></th>
			<th><font size=+1>消費税(円)</font></th>
			<th><font size=+1>税込計(円)</font></th>
EOF
		}
		else {
			print <<"EOF";
			<th><font size=+1>小計(円)</font></th>
EOF
		}

		print <<"EOF";
		</tr>
EOF
		#集計
		&cal1;

		foreach $code (sort keys %list) { # 商品コード順
#		foreach $code (sort { $list{$b} <=> $list{$a} } keys %list) { # 数量が多い順

			#集計
			&cal2;

			#商品名と備考中のコロンをスペースに変換
			$name{$code} =~ s/\:/ /g;
			$rem{$code} =~ s/\:/ /g;

			#在庫管理対象データ
			if ($zaiko{$code} =~ /\d/ && $zaiko{$code} > 0) { print "<input type=hidden name=\"_ZAIKO\" value=\"$target_file{$code}:$code:$list{$code}\">\n"; }

			$c++;
			if ($c % 2) { $bg = "#ffeedd"; } else { $bg = "#ffffff"; } #１行おきにセルの背景色を替える

			print <<"EOF";
			<tr>
			<td align=left>$code</td>
			<td align=left>$rem{$code}</td>
			<td align=left>$name{$code}</td>
			<td align=right>$tanka2</td>
			<td align=right>$kazu2</td>
			<input type=hidden name="ORDER" value="●$code $name{$code}">
EOF
			if ($mailrem) { print "<input type=hidden name=\"ORDER\" value=\"$rem{$code}\">\n"; }

			if ($taxps) {

				if ($tax == 0) { $tax2 = ""; } # 消費税率が0%の場合は表示しない

				print <<"EOF";
				<td align=right>$kei2</td>
				<td align=right><font size=-1>$taxm{$code}</font> $tax2</td>
				<input type=hidden name="ORDER" value="\@$tanka2円×$kazu2＝$kei2円.">
EOF
			}
			else {

				print <<"EOF";
				<input type=hidden name="ORDER" value="\@$tanka2×$kazu2＝$kei2_and_tax\.">
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

		#カンマ挿入処理
		1 while $keis =~ s/(.*\d)(\d\d\d)/$1,$2/g;
		1 while $gokei =~ s/(.*\d)(\d\d\d)/$1,$2/g;
		1 while $taxs =~ s/(.*\d)(\d\d\d)/$1,$2/g;
		1 while $kazu =~ s/(.*\d)(\d\d\d)/$1,$2/g;

		print <<"EOF";
		<tr>
		<th colspan=4><font size=-1 align=center>送料込合計 →</font></th>
		<td align=right><font color="#ffe600"><strong>$kazuall</strong></font></td>
EOF
		if ($taxps) {

			print <<"EOF";
			<input type=hidden name="消費税" value="$taxs円">
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
		<input type=hidden name="合計" value="$gokei円 $taxmes">
		<table><tr><td>
EOF
		foreach (@JUCHU) { print; }

		print <<"EOF";
		</td></tr></table>
		</form>
EOF
	}
	else { print "<h3>何も選択されていません。</h3>\n"; }

	print <<'EOF';
	<br><h3>《訪問販売法での広告表示義務事項等》</h3>
EOF
	print "<form><textarea cols=80 rows=10>";
	foreach (@HANBAI) { print; }

	#if ($reg_name eq '' || $reg_code eq '') { $reg = "未登録"; }
	#else { $reg = "$reg_name 登録コード：$reg_code"; }

	#print "\n"; #↓削除しないこと。
	#print '＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿' . "\n";
	#print "ショッピングバスケットシステム・プロ (c)www.rescue.ne.jp\n";
	#print "シェアウエア登録：$reg\n";
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

#メール送信処理
sub mail {

	unless ($in{'_EMAIL'} =~ /\b[-\w.]+@[-\w.]+\.[-\w]+\b/) { &error('未記入があります。','Ｅメールは半角で正しくご記入ください。'); }

	#在庫管理

	&lock;

	foreach $zaiko_file (keys %ZAIKO_TARGET) {

		@NEW = ();

		if (!open(IN,"$base_dir$zaiko_file\.csv")) { &error('エラー',"$zaiko_fileがオープンできません。"); }
		@lines = <IN>;
		close(IN);

		foreach $line (@lines) {

			$line =~ s/\n//g;
			$zaiko = '';

			#データ抽出
			($code,$name,$tanka,$tax,$rem,$url,$zaiko,$type) = &DecodeCSV($line);

			if ($zaiko =~ /\d+/ && $zaiko ne '') {

				foreach $target (@ZAIKO_KANRI) {

					($TARGET_FILE,$CODE,$KAZU) = split(/:/,$target,3);

					$old = $zaiko;
					if ($CODE eq $code && $zaiko == 0) { &error("在庫エラー","商品コード$codeの商品は在庫が無くなりました。",'画面を戻して当該商品を削除してください。'); }
					if ($CODE eq $code) { $zaiko = $zaiko - $KAZU; }
					if ($zaiko < 0) { &error("在庫エラー","商品コード$codeの商品が在庫数($old)を上回る数($KAZU)をご選択されています。",'画面を戻して当該商品を削除してから、改めて商品をご選択ください。'); }
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

			if (!open(OUT,"> $base_dir$zaiko_file\.csv")) { &error('エラー',"$zaiko_fileがオープンできません。"); }
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

		#メール用にタグ変換
		$value =~ s/&amp;/&/g;
		$value =~ s/&quot;/"/g;
		$value =~ s/&lt;/</g;
		$value =~ s/&gt;/>/g;
		if ($value =~ /(\.)$/) { $value =~ s/\./\n/; }

		if ($name eq 'ORDER' && $value ne '') { print OUT &jis("$value\n"); }
		elsif ($name eq 'ORDER' && $value eq '') { next; }
		elsif ($name eq '_EMAIL') { print OUT &jis("[Ｅメール]\n$value\n\n"); }
		elsif ($name =~ /^\_/) { next; }
		else { print OUT &jis("[$name]\n$value\n\n"); }
	}

	print OUT "\n";
	print OUT "Sender Information >>\n";
	print OUT "X-HTTP-User-Agent: $ENV{'HTTP_USER_AGENT'}\n";
	print OUT "X-Remote-host: $host\n";
	print OUT "X-Remote-Addr: $ENV{'REMOTE_ADDR'}\n";
	close(OUT);

	#一時ファイルの削除
	unlink "$tmp_dir$in{'_order'}\.bkt";

	#-------------------->

	#識別クッキーの設定(空書込)
	print "Set-Cookie: $cookie_name=\n";

	#画面出力開始
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

	print "発注日 $date_now\n";
	print "受付番号 $in{'_order'}\n";
	print "問い合わせ先 $mailto\n\n";

	foreach (@out) {

		($name,$value) = split("\0");
		if ($value =~ /(\.)$/) { $value =~ s/\./\n/; }

		if ($name eq 'ORDER' && $value ne '') { print "$value\n"; }
		elsif ($name eq 'ORDER' && $value eq '') { next; }
		elsif ($name eq '_EMAIL') { print "[Ｅメール]\n$value\n\n"; }
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
			print OUT &jis("Subject: \[$in{'_order'}\] $in{'_SUBJECT'} (写し)\n");
			print OUT "\n";
		}

		print OUT &jis("$head\n");

		foreach (@out) {

			($name,$value) = split("\0");

			#メール用にタグ変換
			$value =~ s/&amp;/&/g;
			$value =~ s/&quot;/"/g;
			$value =~ s/&lt;/</g;
			$value =~ s/&gt;/>/g;
			if ($value =~ /(\.)$/) { $value =~ s/\./\n/; }

			if ($name eq 'ORDER' && $value ne '') { print OUT &jis("$value\n"); }
			elsif ($name eq 'ORDER' && $value eq '') { next; }
			elsif ($name eq '_EMAIL') { print OUT &jis("[Ｅメール]\n$value\n\n"); }
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

	# ロック方式の自動判定 symlink()優先
	$symlink_check = (eval { symlink("",""); }, $@ eq "");
	if (!$symlink_check) {

		$c = 0;
		while(-f "$lockfile") { # file式

			$c++;
			if ($c >= 3) { &error('リトライエラー','ただいま混雑している可能性があります。','戻ってもう一度実行してみてください。'); }
			sleep(2);
		}
		open(LOCK,">$lockfile");
		close(LOCK);
	}
	else {
		local($retry) = 3;
		while (!symlink(".", $lockfile)) { # symlink式

			if (--$retry <= 0) { &error('リトライエラー','ただいま混雑している可能性があります。','戻ってもう一度実行してみてください。'); }
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
	<h3>[<A HREF="JavaScript:history.back()">戻る</A>]</h3>
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
