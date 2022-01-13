 // HELPERS
/**
 * async $file(string file)
 * Simple GET request file.
 * 
 * URIString string file = File path. Input a file in the website, or use HTTP/S.
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
async function $file(file) {
  var file = await fetch(file);
  var text = await file.text();
  return text;
}

// await $file("/api/up") => returns if the user has upvoted, the amount of upvotes, etc 

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

/**
 * vote(integer id, pos = ("up", "down"))
 * 
 * Either upvotes or downvotes for user using /api/up REST API.
 * 
 * Uses fetch PUT request
 * 
 * id = ID of question upvoting
 * ?pos = boolean of whether it is a upvote or downvote. Default is upvote/true.
 */
const vote = async (id, pos) => {
  if(pos == "up"){
    await $data("PUT", {
      upvote: true
    }, "/api/up/q/" + id)
  } else {
    await $data("PUT", {
      upvote: false
    }, "/api/up/q/" + id)
  }
  // Refresh upvote number
  window.location.reload();
}

const avote = async (id, pos) => {
  if(pos == "up"){
    await $data("PUT", {
      upvote: true
    }, "/api/up/a/" + id)
  } else {
    await $data("PUT", {
      upvote: false
    }, "/api/up/a/" + id)
  }
  // Refresh upvote number
  window.location.reload();
}
