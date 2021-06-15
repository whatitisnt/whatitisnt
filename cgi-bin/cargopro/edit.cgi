#!/usr/bin/perl

# ショッピングバスケット・プロ ヴァージョン３用
# 商品設定ファイル編集プログラム edit.cgi
# (c)rescue.ne.jp

# 1999/9/7	バグ修正
# 1999/9/20	エクセルCSV対応(バイナリ処理を除く)
# 1999/12/6	CSV変換処理方法の変更
# 2000/1/17	CSV変換処理方法の変更
# 2000/3/21	MD5対応

#----------------------------------------------------------------------------

#●初期設定ファイル
require "./setup.pl";

#●編集用パスワード
#　このＣＧＩを実行した際に入力が必要な編集者用のパスワードの設定です。
#　添付のパスワード生成ツールcrypt.cgiで生成した「暗号化されたパスワード」をそのままコピーします。
#　$admin_key = 'この部分にコピーします';

$admin_key = '$1$Y8$RELUvhpXQUOORsG7hwVS1.';

#●表示順 (0:正順 1:逆順) .. 新規記録はこれに関係なくデータの後ろに追加される
$rev = 0;

#----------------------------------------------------------------------------

@TYPE = ('数字入力式','チェックボックス式','セレクト式');

($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
@wday_array = ('日','月','火','水','木','金','土');
$date_now = sprintf("%04d年%01d月%01d日(%s)%02d時%02d分%02d秒",$year +1900,$mon +1,$mday,$wday_array[$wday],$hour,$min,$sec);

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

if ($file eq '') { &error("File Not Found","編集するファイルが指定されていません.","Usage; http://$ENV{'SERVER_NAME'}$ENV{'SCRIPT_NAME'}\?file=商品管理ファイル名(拡張子は不要)"); }
if (!-e "$base_dir$file\.csv") { &error('設定エラー',"商品設定ファイル$fileが見つかりません.","Usage edit.cgi?file=商品管理ファイル名"); }

if ($FORM{'ADMIN_KEY'} eq '') { &input; }

if ($admin_key =~ /^\$1\$/) { $salt = 5; } else { $salt = 2; }
if (crypt($FORM{'ADMIN_KEY'},substr($admin_key,0,$salt)) ne $admin_key) { &error('Authorization Required'); }

$lockfile = $tmp_dir . "$file\.lock";

&lock;

if (!open(IN,"$base_dir$file\.csv")) { &error("File Not Open","$file\.csvを開くことができません."); }
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
		f = confirm("削除実行してよろしいですか？");
		return f
	}
	//-->
	</SCRIPT>
	</HEAD>
	<BODY>
	<h1>EDIT $file</h1>
	<h2>タイトル; $head1</h2>
	<hr noshade>
	$head2
	<hr noshade>
	<form action="$ENV{'SCRIPT_NAME'}" method=POST>
	<input type=hidden name="file" value="$file">
	<input type=hidden name="ADMIN_KEY" value="$FORM{'ADMIN_KEY'}">
	<input type=hidden name="start" value="$end">
	<input type=hidden name="restart" value="$start">
	<h4>新規登録<input type=submit name="-NEW-" value="-NEW-"></h4>
	<table border>
	<tr>
	<th nowrap>編集</th>
	<th nowrap>商品コード</th>
	<th nowrap>商品名</th>
	<th nowrap>単価(円)</th>
	<th nowrap>消費税率(%)</th>
	<th nowrap>備考</th>
	<th nowrap>URL</th>
	<th nowrap>在庫数</th>
	<th nowrap>入力形式</th>
	<th nowrap>削除</th>
	</tr>
EOF
	foreach $num ($start .. $to) {

		($code,$fname,$tanka,$tax,$rem,$url,$zaiko,$type) = &DecodeCSV($BASE[$num]);

		if ($zaiko ne '' && $zaiko == 0) { $zaiko = "×無"; }
		elsif ($zaiko > 0) { $zaiko = "残$zaiko"; }
		else { $zaiko = "〇在"; }

		if ($tax == -1) { $tax = '非課税'; }
		elsif ($tax == -2) { $tax = '不課税'; }
		elsif ($tax == -3) { $tax = '税込'; }

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
		<input type=submit value="次のページ">
		</form>
EOF
	}

	print <<"EOF";
	<form action="$ENV{'SCRIPT_NAME'}" method=POST>
	<input type=hidden name="file" value="$file">
	<input type=hidden name="ADMIN_KEY" value="$FORM{'ADMIN_KEY'}">
	<input type=submit value="最新の状態に更新">
	</form>

	※注意<ul>
	<li>ボタンは１回だけ押して処理が完了するまで待たないとデータが破損する恐れがあります.
	<li>画面を戻してボタンを押すと誤動作しますので絶対に避けてください.
	<li>画面を戻したら必ず[最新の状態に更新]してから操作してください.
	<li>ブラウザの再読込ボタンや画面移動ボタン等は使わないでください.
	<li>ヘッド＆テールメッセージの中途編集は、任意のデータの編集内で行ってください.
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

	タイトル <input type=text name="head1" value="$head1" size=60><br>
	ヘッドメッセージ <input type=text name="head2" value="$head2" size=80><br>
	テールメッセージ <input type=text name="head3" value="$head3" size=80><p>

	<table border>
	<tr>
	<th nowrap>項目名</th>
	<th nowrap>編集フォーム</th>
	</tr>

	<tr>
	<th nowrap><font size=-1>商品コード</font></th>
	<td nowrap><input type=text name="key" value="$code" size=10> (重複に注意) 半角英数字およびハイフン</td>
	</tr>
	<tr>
	<th nowrap><font size=-1>商品名</font></th>
	<td nowrap><input type=text name="key" value="$fname" size=30></td>
	</tr>
	<tr>
	<th nowrap><font size=-1>単価</font></th>
	<td nowrap><input type=text name="key" value="$tanka" size=10>円 半角数字</td>
	</tr>
	<tr>
	<th nowrap><font size=-1>消費税率</font></th>
	<td nowrap><input type=text name="key" value="$tax" size=3>％ (非課税:-1 不課税:-2 税込:-3 課税:税率入力) 半角数字</td>
	</tr>
	<tr>
	<th nowrap><font size=-1>備考</font></th>
	<td nowrap><input type=text name="key" value="$rem" size=60> (任意) :(コロン)で改行</td>
	</tr>
	<tr>
	<th nowrap><font size=-1>URL</font></th>
	<td nowrap><input type=text name="key" value="$url" size=60> (任意)</td>
	</tr>
	<tr>
	<th nowrap><font size=-1>在庫数</font></th>
	<td nowrap><input type=text name="key" value="$zaiko" size=5> (在り:空欄 無し:0 在庫管理:在庫数) 空欄または半角数字</td>
	</tr>
	<tr>
	<th nowrap><font size=-1>入力形式</font></th>
	<td nowrap><select name="key" size=1>
	<option value="0" $selected[0]>数字入力式</option>
	<option value="1" $selected[1]>チェックボックス式</option>
	<option value="2" $selected[2]>セレクト式</option></select></td>
	</tr>

	</table><p>
	<input type=submit value="記録する"><input type=reset value="リセット">
	</form>
	<h3>[<A HREF="JavaScript:history.back()">編集をやめる</A>]</h3>
	※注意<ul>
	<li><b>在庫管理機能\を使っている場合は、編集する前に申\し込み画面を閉鎖してください。</b>そうしないと、編集中に在庫数が変化する可能\性があり、正しく処理されません。
	<li>ボタンは１回だけ押して処理が完了するまで待たないとデータが破損する恐れがあります。
	<li>画面を戻してボタンを押すと誤動作しますので絶対に避けてください。
	<li>ブラウザの再実行(リロード)ボタンや画面移動ボタン等は使わないでください。
	<li><b>入力チェックはありません。計算に使用する数字などは間違えないように入力し、編集後は必ず動作試験をしてください。</b>
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

	if (!open(OUT,"> $base_dir$file\.csv")) { &error("File Not Open","$file\.csvを開くことができません."); }

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

	if (!open(IN,"$base_dir$file\.csv")) { &error("File Not Open","$file\.csvを開くことができません."); }
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

	if (!open(OUT,"> $base_dir$file\.csv")) { &error("File Not Open","$file\.csvを開くことができません."); }
	print OUT $head1;
	print OUT $head2;
	print OUT $head3;
	print OUT $head4;

	print OUT @NEW;
	close(OUT);

	if (!open(IN,"$base_dir$file\.csv")) { &error("File Not Open","$file\.csvを開くことができません."); }
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
	<h1>認証</h1>
	<form method=POST action="edit.cgi">
	<input type=hidden name="file" value="$file">
	パスワード <input type=password name="ADMIN_KEY" value="" size=10>
	<input type=submit value="認証">
	</form>
	※商品設定ファイルを書き換え可能\なパーミッションに設定しておく必要があります。
	</body>
	</html>
EOF
exit;

}

sub lock {

	# ロック方式の自動判定 symlink()優先
	$symlink_check = (eval { symlink("",""); }, $@ eq "");
	if (!$symlink_check) {

		$c = 0;
		while(-f "$lockfile") { # file式

			$c++;
			if ($c >= 3) { &error('リトライエラー','ただいま混雑している可能性があります.','戻ってもう一度実行してみてください.'); }
			sleep(2);
		}
		open(LOCK,">$lockfile");
		close(LOCK);
	}
	else {
		local($retry) = 3;
		while (!symlink(".", $lockfile)) { # symlink式

			if (--$retry <= 0) { &error('リトライエラー','ただいま混雑している可能性があります.','戻ってもう一度実行してみてください.'); }
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
	<h3>[<A HREF="JavaScript:history.back()">前の画面</A>]</h3>
	</BODY></HTML>
EOF
	if (-e $lockfile) { unlink($lockfile); }
	exit;
}
