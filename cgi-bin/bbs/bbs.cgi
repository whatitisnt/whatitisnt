#!/usr/bin/perl

#<<<=============================================================================
#<<<�@�@�w�͂���f���E�ϊ��h�@Ver0.55�x  2000.12.08
#<<<								Copyright (c) 2000.5 Tacky				     
#<<<
#<<< �ݒu���@�\��(��̗�)
#
#<<< public_html�i�z�[���y�[�W�f�B���N�g���j
#<<< |
#<<< |-- cgi-bin�i�C�ӂ̃f�B���N�g���j
#<<<   |-- jcode.pl      (755)�c(���{�ꃉ�C�u����)
#<<<   |-- hagure.cgi    (755)�c(�X�N���v�g�{��)
#<<<   |-- hagure.txt    (666)�c(���O�t�@�C��)
#<<<   |-- hagure.lock�@�@    �c(���b�N�t�@�C��)���X�N���v�g���Ŏ��������y�э폜
#<<<   |-- xxxx.dic      (666)�c(�����t�@�C��)	
#<<<
#<<< ��( )���̓p�[�~�b�b�V�����̒l�ł��B
#<<< ��hagure.cgi�FPerl�̃p�X�A���̑��̍��ڂ��C���A�A�X�L�[���[�h�ŃA�b�v���[�h�B
#<<< ��hagure.txt�F��̃t�@�C�����쐬���A�A�X�L�[���[�h�ŃA�b�v���[�h�B
#<<< ��XXXX.dic�@�F�e�������t�@�C�����쐬���A�A�X�L�[���[�h�ŃA�b�v���[�h�B
#<<<   �@�������̍쐬���@�F�G�f�B�^�ō쐬���Ă��������B
#<<<          �����̃C���[�W�́A�u�ϊ��O���́v�{�u���p�X�y�[�X�v�{�u�ϊ��㕶�́v
#<<<        ex.
#<<<           ���͂悤 ���͂��[!
#<<<           ���₷�� ���ɂ�[!
#<<<           �o�C�o�C �i�O�O�O�j�^�`�`�������������I
#<<< ��hagure.lock�F�e���ŗp�ӂ���K�v����܂���B
#<<<
#<<< >>> Update-History...
#<<<
#<<<	2000.12.08  >>�@�܂��܂�̧��ۯ�����������Ȃ��ꍇ������s��C��
#<<<	2000.07.12  >>�@�X�N���[�������ɕs��Ȩ��ۯ�����������Ȃ��ꍇ������s��C��
#<<<	2000.06.17  >>�@Apache+Netscape���������Ή��E���b�N����������
#<<<=============================================================================

require './jcode.pl';

$url 				= 'http://www.untitled2001.com/';			#<<<�߂��t�q�k
$script 			= './bbs.cgi';									#<<<���̂b�f�h�̖��O���w��
$logfile 			= './bbs.txt';									#<<<���O�t�@�C���̖��O���w��
$lockfile			= './bbs.lock';									#<<<���b�N�t�@�C���̖��O���w��
$method 			= 'POST';											#<<<METHOD�̎w��(POST����GET)

$convert			= 0 ;												#<<<�ϊ��@�\���g���H(0:no 1:yes)
#<<<�����t�@�C���̖��O���w��i��L�̕ϊ��@�\���u�g���v�ɂ����ꍇ�̂ݏC���ΏہB�u�g��Ȃ��v�ꍇ�͏C���s�v�ł��j
#���������P�̏ꍇ�̎w����@
#  @dicfile = ('./xxxx.dic');
#�������������̏ꍇ�̎w����@
#  @dicfile = ('./xxxx.dic','./yyyyy.dic','./zzzzz.dic');
#  @dicname = ('�w����','�x����','�y����');

@dicfile = ('./hagure.dic');
@dicname = ('�e�X�g�ϊ�');

$titlename			= 'untitled2001 bbs';								#<<<�^�C�g�����w��
$titlelogo	 		= '../../bbsimg/title.gif';				#<<<�^�C�g���摜���w��
$bgcolor 			= '#000000';										#<<<�w�i�F���w��
$backpicture	 	= '';												#<<<�w�i�摜���w��i�g�p���Ȃ��ꍇ�́A''�ŗǂ�)

$tbgcolor 			= '#ff0000';										#<<<���̓t�H�[���̔w�i�F���w��
$ftextcolor 		= '#ffffff';										#<<<���̓t�H�[���̕����F���w��
$stextcolor 		= '#ffffff';										#<<<�폜�t�H�[���̕����F���w��

$msg_cellbgcolor 	= '#cccccc';										#<<<���b�Z�[�W�����̃^�C�g�����Z���w�i�F���w��
$msg_cellbgcolor2 	= '#999999';										#<<<���b�Z�[�W�����̃��b�Z�[�W���Z���w�i�F���w��

$tcolor				= "#000066";								# �����F
$linkcolor			= "#cc6600";								# �����N�F�i���ǃ����N�j
$vlinkcolor			= "#666666";								# �����N�F�i���ǃ����N�j
$alinkcolor		 	= "#ff3300";								# �����N�F�i���������j
$hlinkcolor			= '#ff0000';								#�}�E�X���|�C���g�����ۂ̃����N�A���_�[���C���̐F�iIE�̂�)

$icon_hp	 		= '../../bbsimg/home.gif';				#<<<�g�o�����N�p�摜���w��
$icon_back			= '../../bbsimg/back.gif';				#<<<BACK�p�摜���w��
$icon_center			= '../../bbsimg/center.gif';			#<<<CENTER�p�摜���w��
$icon_next			= '../../bbsimg/next.gif';				#<<<NEXT�p�摜���w��
$icon_close			= '../../bbsimg/close.gif';				#<<<CLOSE�p�摜���w��

$row				= 4 ;												#���̓t�H�[���E���b�Z�[�W���̍s��
$col				= 40;												#���̓t�H�[���E���b�Z�[�W���̕�����

$datamax 			= 150 ;												#<<<�ő�f�[�^�ۑ�����
$pagemax 			= 10 ;												#<<<�P�y�[�W���ɕ\�����錏��
$password 			= 'pass2001';											#<<<�����e�i���X�p�p�X���[�h�i�Ǘ��җp�j

$tablesz			= '50%';											#<<<���O�\�����e�[�u������

$tag				= 'yes';											#�^�O����(yes,no)

#�f���r�炵�΍�B�r���������v���o�̃A�h���X��ݒ肵�ĉ������B
#�@"xxx?.com"�Ƃ����ꍇ�A"xxx1.com","xxx2.com"���A�u�H�v�̕�����������P�Ɣ��f���܂�
#  "xxx*.com"�Ƃ����ꍇ�A"xxx1.com","xxx12345.com���A�u���v�̕������O�ȏ�̕�����Ɣ��f���܂��B
@DANGER_LIST=("xxx.com","yyy.com","zzz*.or.jp");

#�f���r�炵�΍􂻂̂Q�B���b�Z�[�W�ő啶�������w��B���ɐݒ肵�Ȃ��ꍇ�́A''�Ƃ��ĉ������B
$maxword 			= '2000' ;

#���e���̃p�X���[�h��crypt�֐����g�p����i�Í����j
#crypt�֐������p�o���Ȃ��ꍇ������܂��̂ŁA���e���ɃG���[�ɂȂ�ꍇ�́A�u0:�g�p���Ȃ��v�ɂ��ĉ������ˁB
$ango				= 1 ;												#0:�g�p���Ȃ� 1:�g�p����@�i�����F�P�F�g�p����j

$pt					= '9pt';									#�S�̂̃t�H���g�T�C�Y�ipt�w��ȊO��������̂��A�l�m��Ȃ��B(^^�U�j

#�t�H�[���b�r�r�ݒ�@���g�p���Ȃ��ꍇ�́A$css_style = "";�Ƃ��ĉ�����
$css_style = <<"EOM";
 STYLE="font-size:$pt;color:#666666;border:1 dotted #000066;" onFocus="this.style.backgroundColor='#cccccc'" onBlur="this.style.backgroundColor='#FFFFFF'" onMouseOver="this.focus()"
EOM

#<<<�@�������牺�͂�����Ȃ����������ł��B
@errtag = ('table','meta','form','!--','embed','html','body','tr','td','th','a');		#�f���W�����`�ȃ^�O

if ( $convert == 1 && @dicfile < 1 ) { &error("�����t�@�C�����ݒ肳��Ă��܂���"); }

###############################################################################
#### Main Process  START  #####################################################
###############################################################################
if ($ENV{'HTTP_USER_AGENT'} !~ /MSIE/i) { $css_style = "" ; }		#Netscape-CSS�Ή�
#<<<�V�X�e�������E�����擾
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
$year = sprintf("%02d",$year + 1900);
$month = sprintf("%02d",$mon + 1);
$mday = sprintf("%02d",$mday);
$hour = sprintf("%02d",$hour);
$min = sprintf("%02d",$min);
if ( substr($month,0,1) == 0 )	{	$month =~ s/0/ /;	}
if ( substr($day,0,1) == 0 )	{	$day =~ s/0/ /;	}
$week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat') [$wday];
$today = "$month��$mday��($week) $hour��$min��";

&cookieget;												#<<<COOKIE�̎擾
&decode ;												#<<<�f�R�[�h
if ( $FORM{'action'} eq "maintenance" ) {      			#<<<"����"�������e�i���X�̏ꍇ
	&update; 
}	elsif	( $FORM{'action'} eq "update" )		{		#<<<���O�t�@�C���X�V�i�ҏW���j
	&update ;
}	else	{
	if	( $FORM{'action'} eq 'regist' )	{
		&regist ;
		print "Location: $script?\n\n";
	}
	&header ;											#<<<html�w�b�_�[�o��
	&forminput ;										#<<<���̓t�H�[���\��
}
&view ;													#<<<���O�\��
&footer ;												#<<<html�t�b�^�[�o��
exit;
###############################################################################
#### Main Process  END  #######################################################
###############################################################################

###<--------------------------------------------------------------
###<---   �f�R�[�h���ϐ����
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
	        #�댯�ȃ^�O�͋֎~!!!
			foreach ( @errtag )	{
				if ($value =~ /<$_(.|\n)*>/i) {	 &error("�g�p�o���Ȃ��^�O�����͂���Ă��܂�");	}
			}
		}	else	{
			$value =~ s/</&lt;/g;											
			$value =~ s/>/&gt;/g;
		}
		$value =~ s/\,/�C/g;
		&jcode'convert(*value,'sjis');
		$FORM{$name} = $value;
	}
	$FORM{'hp'}   =~ s/^http\:\/\///;
}
###<--------------------------------------------------------------
###<---   ���̓t�H�[��
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
		print "<option value=no selected>�ϊ����Ȃ�\n";
		print "<option value=99 selected>�����_���ϊ�\n";
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
###<---   HTML�w�b�_�[�����o��
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
###<---   HTML�t�b�_�[�����o��
###<--------------------------------------------------------------
sub footer { 
	print "<p align=right><a href=\"javascript:window.close()\"><img src=\"$icon_close\" border=0></a></p>\n";
	print "</body></html>\n";
}
###<--------------------------------------------------------------
###<---   ���O�t�@�C���ǂݍ���
###<--------------------------------------------------------------
sub	dataread	{
	#<<<���O�ǂݍ���
	if ( !(open(IN,"$logfile")))	{	&error("���O�t�@�C��($logfile)�̃I�[�v���Ɏ��s���܂���");	}
	@LOG = <IN>;
	close(IN);
}
###<--------------------------------------------------------------
###<---   ���O�\��
###<--------------------------------------------------------------
sub	view	{
	&dataread ;												#<<<���O�ǂݍ���
	print "<center><hr width=80% size=1 noshade color=#000000>\n";

	#�\���Ώۃy�[�W�̐擪�f�[�^�������Z�o
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
			print "[$no]�@";
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
				print "(�ϊ�����)\n"	if ( $conv eq 'no' );
				print "</font>\n";
			}
			print "<br>\n";
			if ( $title ne '' )	{
				print "��$title";
			}	else	{
				print "������";
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
###<---   ���O�o��
###<--------------------------------------------------------------
sub	regist	{
	# �z�X�g�����擾
	$host  = $ENV{'REMOTE_HOST'};		$adr  = $ENV{'REMOTE_ADDR'};
	if ($host eq "" || $host eq "$adr") {
		($p1,$p2,$p3,$p4) = split(/\./,$adr);
		$temp = pack("C4",$p1,$p2,$p3,$p4);			$host = gethostbyaddr("$temp", 2);
		if ($host eq "") { $host = $adr; }
	}
	#�f���r�炵�΍�
	foreach $buf(@DANGER_LIST){
		if ( $buf ) {
			# �p�^�[���}�b�`��ϊ�
			$buf=~ s/\./\\./g;		$buf=~ s/\?/\./g;		$buf=~ s/\*/\.\*/g;
			if($host =~ /$buf/gi){	&error("\�\\��\�󂠂�܂���B<br>���Ȃ��̃v���o�C�_�[����͓��e�ł��܂���ł����D ");	}
		}
	}
	if ( $maxword ne '' && (length($FORM{'comment'}) > $maxword))	{	&error("���b�Z�[�W��$maxword�����܂ł����o�^�o���܂���B");	}
	if ( $FORM{'name'} eq '')	{	&error("�����O����͂��ĉ������B");	}
	if ( $FORM{'comment'} eq '')	{	&error("���b�Z�[�W�͏ȗ��o���܂���B");	}

	&filelock ;	#�t�@�C�����b�N
	&dataread ;												#<<<���O�ǂݍ���

	$FORM{'comment'} =~ s/\r\n/<br>/g;	$FORM{'comment'} =~ s/\r|\n/<br>/g;	
	if ( $FORM{'henshin'} ne 'no' && $convert == 1 )	{	$comment = &dicconvert($FORM{'comment'});	}
	else	{	$comment = $FORM{'comment'} ;	}

	$dcnt = @LOG;
	if ($dcnt >= $datamax) {	pop(@LOG);	}
	if ( $dcnt < 1 )	{
		$no = 1;											#�P����
	}	else	{
		($no,$dummy) = split(/,/,$LOG[0]);					#�ŐV�L��No�擾
		$no++;
	}
	# �p�X���[�h�̈Í����icrypt�֐��g�p�j�j
	if ($FORM{'pass'} ne "") { &pass_enc($FORM{'pass'}); }	else	{ $pass = '' ; }
	unshift(@LOG,"$no,$FORM{'name'},$FORM{'email'},$FORM{'hp'},$FORM{'subject'},$comment,$today,$pass,$FORM{'henshin'},$host,\n");
	if ( !(open(OUT,">$logfile")))	{	&fileunlock ;	&error("���O�t�@�C��($logfile)�̃I�[�v���Ɏ��s���܂���");	}
	print OUT @LOG;
	close(OUT);

	&fileunlock ;	#�t�@�C�����b�N����

	#COOKIE�ݒ�
	&cookieset ;

}
###<--------------------------------------------------------------
###<---   ���O�t�@�C���X�V
###<--------------------------------------------------------------
sub update {
	if ( $FORM{'pass'} eq "")	{	&error("�p�X���[�h����͂��ĉ������B");	}

	&filelock ;	#�t�@�C�����b�N
	&dataread ;												#<<<���O�ǂݍ���

    foreach (@LOG) {
		($no,$name,$email,$hp,$title,$comment,$regdate,$pass,$conv,$hst,$d2) = split(/,/,$_);
		if ( $FORM{'no'} eq $no)	{	
			if ($FORM{'pass'} ne $password && (&pass_dec($pass))) { &fileunlock ;	&error("�p�X���[�h���Ⴂ�܂��B"); }
		}	else	{
			push(@new,$_);	
		}
	}
	if ( !(open(OUT,">$logfile")))	{	&fileunlock ;	&error("���O�t�@�C��($logfile)�̃I�[�v���Ɏ��s���܂���");	}
	print OUT @new;
	close(OUT);

	&fileunlock ;	#�t�@�C�����b�N����

	print "Location: $script?\n\n";
}
###<--------------------------------------------------------------
###<---   �G���[����
###<--------------------------------------------------------------
sub error {
	&header ;
	print "<br><br>$_[0]\n";
	&footer;
	exit;
}
###<-------------------------------------------------------------
###<---   �N�b�L�[�擾
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
###<---   �N�b�L�[�ݒ�
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
###<---   �����ϊ�
###<--------------------------------------------------------------
sub dicconvert { 
	#<<<�����ǂݍ���

	if ( $FORM{'henshin'} == 99 )	{
		srand(time ^ ($$ + ($$ << 15)));
		$FORM{'henshin'}	= int(rand(@dicname)) ;
	}

	$dicf = @dicfile[$FORM{'henshin'}];
	if ( !(open(IN,"$dicf")))	{	&fileunlock ;	&error("�����t�@�C���̃I�[�v���Ɏ��s���܂���");	}
	@dic = <IN>;
	close(IN);
	###<-----  terra��(http://www2q.biglobe.ne.jp/~terra/cgi/)�̎����ϊ����[�`�����Q�l�ɂ����Ē����܂���-----
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
###<---   �t�@�C�����b�N�ݒ�
###<--------------------------------------------------------------
sub filelock {
	$sw = 0;
	foreach (1 .. 5) {
		if (-e $lockfile) { sleep(1); }
		else {		open(LOCK,">$lockfile");	close(LOCK);	$sw = 1;	return;	}
	}
	&error("�������̕����������ݒ��ł��B�u���E�U�́u�߂�v�Ŗ߂��čēx�o�^���s���ĉ������B"); 
}
###<--------------------------------------------------------------
###<---   �t�@�C�����b�N����
###<--------------------------------------------------------------
sub fileunlock {
	if (-e $lockfile) { unlink($lockfile); }
}
###<-------------------------------------------------------------
###<---   �p�X���[�h�Í���
###<--------------------------------------------------------------
sub pass_enc {
	if ( $ango == 1 ) {		$pass = crypt($_[0], $_[0]);
	}	else	{		$pass = $_[0];	}
}
###<-------------------------------------------------------------
###<---   �p�X���[�h�`�F�b�N
###<--------------------------------------------------------------
sub pass_dec {
	if ( $ango == 1 ) {
		if ($_[0] ne '' && ( crypt($FORM{'pass'}, $_[0]) eq $_[0]) )  {		return 0 ;		}
	}	else	{
		if ($FORM{'pass'} eq $_[0]) {	return 0 ;	}
	}
	return 1;
}
