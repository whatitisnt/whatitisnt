#!/usr/bin/perl

# �V���b�s���O�o�X�P�b�g�E�v�� ���@�[�W�����Q�p
# ���i�ݒ�t�@�C���ҏW�v���O���������ݒ�p�p�X���[�h�����c�[�� crypt.cgi
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
	print "<html><head><title>�Í�������</title></head>\n";
	print "<body>\n";
	print "<h1>�Í�������</h1>\n";
	print "<form action=\"crypt.cgi\">\n";
	print "����(�p�X���[�h) <input type=text name=\"plain\" size=30> <input type=submit value=\"�Í���\"><input type=reset value=\"RESET\">\n";
	print "</form>\n";
	print "</body></html>\n";
	exit;
}

if ($FORM{'plain'} eq '' || $FORM{'plain'} =~ /\W/) { &error('�Ïؔԍ��̓��͂��������A������ɔ��p�p�����ȊO�̕������܂܂�Ă��܂�.'); }
if (length($FORM{'plain'}) < 6) { &error('�p�����U�����ȏ�Ŏw�肵�Ă�������.'); }

print "Content-type: text/html\n\n";
print "<html><head><title>�Í�������</title></head>\n";
print "<BODY>\n";
print "<h2>���s����</h2>\n";

$MD5 = &crypt_test;

print "<blockquote>\n";
print "<form>\n";
print "����(�p�X���[�h) <input size=15 value=\"$FORM{'plain'}\"><p>\n";

if ($md5) {

	($pwd) = &MakeCrypt($FORM{'plain'});
	print "�Í� <input size=60 value=\"$pwd\"> (MD5)<br>\n";
}

if ($des) {

	$MD5 = 0;
	($pwd) = &MakeCrypt($FORM{'plain'});
	print "�Í� <input size=60 value=\"$pwd\"> (DES)<p>\n";
}

print "</form></blockquote>\n";
print "</body></html>\n";
exit;

sub MakeCrypt {

	local($plain) = @_; # ����:����
	local(@char,$f,$now,@saltset,$pert1,$pert2,$nsalt,$salt);
	local($retry) = 4;

	@saltset = ('a'..'z','A'..'Z','0'..'9','.','/'); # �Í����\������镶���Q
	$now = time; # �����̕ӂ͒ʏ́u�炭���̖{�v���Q��
	srand(time|$$);
	$f = splice(@saltset,rand(@saltset),1) . splice(@saltset,rand(@saltset),1);
	($pert1,$pert2) = unpack("C2",$f);
	$week = $now / (60*60*24*7) + $pert1 + $pert2 - length($plain);
	$nsalt = $saltset[$week % 64] . $saltset[$now % 64];
	if ($MD5) { $csalt = "\$1\$"; } else { $csalt = ""; }

	while (crypt($plain,substr($result,0,$salt)) ne $result || $result eq '') {

		$result = crypt($plain,"$csalt$nsalt");
		if ($result =~ /^\$1\$/) { $salt = 5; } else { $salt = 2; }

		if (--$retry <= 0) { &error('���Í����Ɏ��s'); }
		sleep(1);
	}

	return $result; # �ߒl:�Í�
}

sub crypt_test {

	local($plain,$SALT,$MD5,$pwd,$pwd2);

	$plain = '99999999';
	$SALT = "00";

	$MD5 = 1;

	if ($MD5) { $csalt = '$1$'; } else { $csalt = ""; }

	$pwd = crypt($plain,"$csalt$SALT");
	print "MD5�Í�����=", $pwd, "<br>\n";
	if ($pwd =~ /^\$1\$/) { $salt = 5; } else { $salt = 2; }
	$pwd2 = crypt($plain,substr($pwd,0,$salt));
	print "MD5�ƍ�����=", $pwd2, "<br>\n";
	if ($pwd ne "" && $pwd eq $pwd2 && $pwd =~ /^\$1\$/) { print "��MD5���g���܂�<p>\n"; $md5 = 1; }
	else { print "��MD5�͎g���܂���<p>\n"; $md5 = 0; }

	$MD5 = 0;

	if ($MD5) { $csalt = "\$1\$"; } else { $csalt = ""; }
	$pwd = crypt($plain,"$csalt$SALT");
	print "DES�Í�����=", $pwd, "<br>\n";
	if ($pwd =~ /^\$1\$/) { $salt = 5; } else { $salt = 2; }
	$pwd2 = crypt($plain,substr($pwd,0,$salt));
	print "DES�ƍ�����=", $pwd2, "<br>\n";
	if ($pwd ne "" && $pwd eq $pwd2) { print "��DES���g���܂�<p>\n"; $des = 1; }
	else { print "��DES�͎g���܂���<p>\n"; $des = 0; }

	if ($md5) { print "��MD5���g���Ă��������B<p>\n"; $MD5 = 1; }
	elsif (!$md5 && $des) { print "��DES���g���Ă��������B<p>\n"; $MD5 = 0; }
	else { print "���ǂ�����g���܂���B<p>\n"; $MD5 = 9; }

	return $MD5;
}

sub error {

	print "Content-type: text/html\n\n";
	print "<html><head><title>�Í�������</title></head>\n";
	print "<body>\n";
        print "<h3>$_[0]</h3>\n";
        print "</body></html>\n";
        exit;
}
