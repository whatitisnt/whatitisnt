#!/usr/bin/perl

# ショッピングバスケット・プロ ヴァージョン２用
# 商品設定ファイル編集プログラム初期設定用パスワード生成ツール crypt.cgi
# (c)www.rescue.ne.jp

#----------------------------------------------------------------------------

$buffer = $ENV{'QUERY_STRING'};

@pairs = split(/&/,$buffer);
foreach $pair (@pairs) {

    ($name, $value) = split(/=/, $pair);
    $value =~ tr/+/ /;
    $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
    $FORM{$name} = $value;
}

if ($buffer eq '') {

	print "Content-type: text/html\n\n";
	print "<html><head><title>暗号文字化</title></head>\n";
	print "<body>\n";
	print "<h1>暗号文字化</h1>\n";
	print "<form action=\"crypt.cgi\">\n";
	print "平文(パスワード) <input type=text name=\"plain\" size=30> <input type=submit value=\"暗号化\"><input type=reset value=\"RESET\">\n";
	print "</form>\n";
	print "</body></html>\n";
	exit;
}

if ($FORM{'plain'} eq '' || $FORM{'plain'} =~ /\W/) { &error('暗証番号の入力が無いか、文字列に半角英数字以外の文字が含まれています.'); }
if (length($FORM{'plain'}) < 6) { &error('英数字６文字以上で指定してください.'); }

print "Content-type: text/html\n\n";
print "<html><head><title>暗号文字化</title></head>\n";
print "<BODY>\n";
print "<h2>実行結果</h2>\n";

$MD5 = &crypt_test;

print "<blockquote>\n";
print "<form>\n";
print "平文(パスワード) <input size=15 value=\"$FORM{'plain'}\"><p>\n";

if ($md5) {

	($pwd) = &MakeCrypt($FORM{'plain'});
	print "暗号 <input size=60 value=\"$pwd\"> (MD5)<br>\n";
}

if ($des) {

	$MD5 = 0;
	($pwd) = &MakeCrypt($FORM{'plain'});
	print "暗号 <input size=60 value=\"$pwd\"> (DES)<p>\n";
}

print "</form></blockquote>\n";
print "</body></html>\n";
exit;

sub MakeCrypt {

	local($plain) = @_; # 入力:平文
	local(@char,$f,$now,@saltset,$pert1,$pert2,$nsalt,$salt);
	local($retry) = 4;

	@saltset = ('a'..'z','A'..'Z','0'..'9','.','/'); # 暗号が構成される文字群
	$now = time; # ↓この辺は通称「らくだの本」を参照
	srand(time|$$);
	$f = splice(@saltset,rand(@saltset),1) . splice(@saltset,rand(@saltset),1);
	($pert1,$pert2) = unpack("C2",$f);
	$week = $now / (60*60*24*7) + $pert1 + $pert2 - length($plain);
	$nsalt = $saltset[$week % 64] . $saltset[$now % 64];
	if ($MD5) { $csalt = "\$1\$"; } else { $csalt = ""; }

	while (crypt($plain,substr($result,0,$salt)) ne $result || $result eq '') {

		$result = crypt($plain,"$csalt$nsalt");
		if ($result =~ /^\$1\$/) { $salt = 5; } else { $salt = 2; }

		if (--$retry <= 0) { &error('●暗号化に失敗'); }
		sleep(1);
	}

	return $result; # 戻値:暗号
}

sub crypt_test {

	local($plain,$SALT,$MD5,$pwd,$pwd2);

	$plain = '99999999';
	$SALT = "00";

	$MD5 = 1;

	if ($MD5) { $csalt = '$1$'; } else { $csalt = ""; }

	$pwd = crypt($plain,"$csalt$SALT");
	print "MD5暗号試験=", $pwd, "<br>\n";
	if ($pwd =~ /^\$1\$/) { $salt = 5; } else { $salt = 2; }
	$pwd2 = crypt($plain,substr($pwd,0,$salt));
	print "MD5照合試験=", $pwd2, "<br>\n";
	if ($pwd ne "" && $pwd eq $pwd2 && $pwd =~ /^\$1\$/) { print "○MD5が使えます<p>\n"; $md5 = 1; }
	else { print "○MD5は使えません<p>\n"; $md5 = 0; }

	$MD5 = 0;

	if ($MD5) { $csalt = "\$1\$"; } else { $csalt = ""; }
	$pwd = crypt($plain,"$csalt$SALT");
	print "DES暗号試験=", $pwd, "<br>\n";
	if ($pwd =~ /^\$1\$/) { $salt = 5; } else { $salt = 2; }
	$pwd2 = crypt($plain,substr($pwd,0,$salt));
	print "DES照合試験=", $pwd2, "<br>\n";
	if ($pwd ne "" && $pwd eq $pwd2) { print "○DESが使えます<p>\n"; $des = 1; }
	else { print "○DESは使えません<p>\n"; $des = 0; }

	if ($md5) { print "●MD5を使ってください。<p>\n"; $MD5 = 1; }
	elsif (!$md5 && $des) { print "●DESを使ってください。<p>\n"; $MD5 = 0; }
	else { print "●どちらも使えません。<p>\n"; $MD5 = 9; }

	return $MD5;
}

sub error {

	print "Content-type: text/html\n\n";
	print "<html><head><title>暗号文字化</title></head>\n";
	print "<body>\n";
        print "<h3>$_[0]</h3>\n";
        print "</body></html>\n";
        exit;
}
