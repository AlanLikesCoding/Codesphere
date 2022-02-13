/*
CONSOLE FUNCTIONS
*/
const $ = {
  log (text) {
      console.log("%cCodesphere | " + text, "background-color: #3385ff; color: white; padding: 7px 9px");
  },
  warn (text) {
      console.log("%cCodesphere | WARNING: " + text, "background-color: #ff9633; color: white; padding: 7px 9px");
  },
  err (text) {
      console.log("%cCodesphere | ERROR: " + text, "background-color: #ff3d33; color: white; padding: 7px 9px");
  }
};

$.log("Codesphere.js Library Connected. Functions Online.")

const $redirect = (url) => {
  window.location.href = url
}

function $hashCode(str) { // java String#hashCode
    var hash = 0;
    for (var i = 0; i < str.length; i++) {
       hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    return hash;
} 

function $color(i){
    var c = (i & 0x00FFFFFF)
        .toString(16)
        .toUpperCase();

    return "00000".substring(0, 6 - c.length) + c;
}

/* 
COOKIE
*/
function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}
/*
HTTP POST FUNCTIONS
*/

/**
 * async $file(string file)
 * Simple GET request file.
 * 
 * URIString string file = File path. Input a file in the website, or use HTTP/S.
 */

async function $file(file) {
  var file = await fetch(file);
  var text = await file.text();
  return text;
}

/*
USE IN ASYNC FUNCTION 

await $data("PUT", {
  upvote: true
}, "/api/up")

*/

/**
 * async $data(string type, object data, string file, object ?more)
 * More advanced fetch features, with data, types, and configs.
 * 
 * HTTPRequestType string type = Type of request. Could be "GET"/i, "POST"/i, or "PUT"/i.
 * JSON object data = Data to send. Format in object.
 * URIString string file = File path. Input a file in the website, or use HTTP/S.
 * JSON object ?more = More fetch data if needed. Defaults to null
 */

async function $data(type, data, file, more = null) {
  var add;
  if (more !== null) {
    add = "," + JSON.stringify(more).substring(1, JSON.stringify(more).length - 1);
  } else {
    add = "";
  }
  for (var i = 0; i < Object.entries(data).length; i++) {
    if (typeof Object.entries(data)[i][1] == "object") {
      throw new TypeError("Data cannot contain an object as a value.");
    }
  }
  var thedata = ""
  if (type.match(/post/i) !== null || type.match(/put/i) !== null) {
    thedata = JSON.stringify(data).replaceAll("\"", "\\\"");
 
    var send = await fetch(file, JSON.parse(`
    {
      "method": "${type}",
      
      "headers": {
        "Content-Type": "application/javascript",
        "X-CSRFToken": "${getCookie("csrftoken")}"
      },
      "body": "${thedata}"${add}
    }
    `));
    console.log(`
    {
      "method": "${type}",
      
      "headers": {
        "Content-Type": "application/json",
        "X-CSRFToken": "${getCookie("csrftoken")}"
      },
      "body": "${thedata}"${add}
    }
    `)
    var text = await send.text();
    return text;
  } else {
    var thedata = Object.entries(data);
    for (var i = 0; i < thedata.length; i++) {
      thedata[i][0] = encodeURIComponent(thedata[i][0]);
      thedata[i][1] = encodeURIComponent(thedata[i][1]);
    }
    thedata = Object.fromEntries(thedata);
    var send = await fetch(file + "?" + (new URLSearchParams(thedata)).toString().replace("\"", "\\\""), JSON.parse(`
    {
      "method": "${type}",
      
      "headers": {
        "X-CSRFToken": "${getCookie("csrftoken")}",
        "Content-Type": "application/json"
      }${add}
    }
    `));
    console.log(`
    {
      "method": "${type}",
      
      "headers": {
        "X-CSRFToken": "${getCookie("csrftoken")}",
        "Content-Type": "application/json"
      }${add}
    }
    `)
    var text = await send.text();
    return text;
  }

}

