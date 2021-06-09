// MSIE 4 +

function launch(newURL, newName, newFeatures, orgName) {
  var remote = open(newURL, newName, newFeatures);
  if (remote.opener == null)
    remote.opener = window;
  remote.opener.name = orgName;
  return remote;
}

function launchRemote(frameset) {
  myRemote = launch(frameset, "frameset", "channelmode=0,dependent=0,directories=0,fullscreen=1,location=0,menubar=0,resizable=1,scrollbars=0,status=1,toolbar=0", "myWindow");
}

// Netscape 4 +

function essential(url)
 {
  essentialPop(url);
 };

function essentialPop(url)
 {
  var menuVar = 'no';
  var popX = 0;
  var popY = 0;
  if ( parseFloat(navigator.appVersion.substring(0,navigator.appVersion.indexOf(' '))) >= 4 )
   {
    var popWidth = screen.width;
    var popHeight = screen.height;
    if ( navigator.appVersion.indexOf("Mac") != -1 )
    { popHeight = screen.height - 20; menuVar = 'yes'; }
    if ( navigator.appName == "Microsoft Internet Explorer" && parseFloat(navigator.appVersion.substring(0,navigator.appVersion.indexOf(' '))) >= 4)
    { popHeight = screen.height - 50;popWidth = screen.width - 10; }
   };
  var theParameters = 'LEFT=' + popX + ',TOP=' + popY + ',screenX=' + popX + ',screenY=' + popY + ',' + 'OUTERWIDTH=' + popWidth + ',OUTERHEIGHT=' + popHeight + ',WIDTH=' + popWidth + ',HEIGHT=' + popHeight + ',TOOLBAR=no,LOCATION=no,DIRECTORIES=no,STATUS=no,MENUBAR=' + menuVar + ',SCROLLBARS=no,RESIZABLE=no';
  hellPop = window.open(url,"main",theParameters);
 };


// browser re-direct

version = navigator.appVersion
name = navigator.appName
var nn2, nn3, nn4, ie3, ie4

//4.x Browsers
if (version.charAt(0) == "4")
  {
    if (name == "Netscape")
      {
        nn4 = true
      }else
      if (name == "Microsoft Internet Explorer")
      {
        ie4 = true
      }
  }

if ((version.charAt(0) == "3") || (version.charAt(0) == "2"))
  {
    if (name == "Microsoft Internet Explorer")
      {
        ie3 = true
      }else if (version.charAt(0) == "2")
      {
        nn2 = true
      } else
      {
        nn3 = true
      }
  }

function poppa(url, frameset)
  {
    if (nn2)
      {
        // Netscape 2 browser
        window.location = url;
      }

    if (nn3)
      {
        // Netscape 3 browser
        window.location = url;
      }

    if (nn4)
      {
        // Netscape 4 browser
        essential(url)
      }

    if (ie3)
      {
        // Explorer 3 browser
        window.location = url;
      }

    if (ie4)
      {
        // Explorer 4 browser
        launchRemote(frameset)
      }
  }