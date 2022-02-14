$.log("Main.js Library Connected. Functions Online.")

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

const filter = () => {
  let filter = document.getElementById("filter").value;
  let tags = document.getElementById("tags_input").value;
  if(tags == null) {
    $redirect("https://codesphere.repl.co/forum/" + filter)
  }
  $redirect("https://codesphere.repl.co/forum/" + filter + "/" + tags)
}

const addTag = () => {
  let input = document.getElementById("tags")
  if(input == null) return
  document.getElementById("display").innerHTML += "<span class='badge bg-secondary me-1'>" + input.value + "<button type='button' class='btn-close' aria-label='Close' onclick='closeTag(this.parentElement)'></button></span>"
  document.getElementById("tags_input").value += input.value + "|"
  input.value = ""
}

const closeTag = (object) => {
  let value = object.innerText;
  object.style.display = "none"
  let tags = document.getElementById("tags_input").value
  let replaceValue = value + "|"
  console.log(replaceValue)
  tags = tags.replace(replaceValue, "")
  console.log(tags)
  document.getElementById("tags_input").value = tags
}

/* DOCUMENT ONLOAD FUNCTIONS */
const load = () => {
  // Markdown Everything
  $.log("Onload Proccess Started.")
  let parse = document.getElementsByClassName("parse");
  for(let i = 0; i < parse.length; i++){
    let text = parse[i].innerText;
    text = markdown(text);
    text = profanity(text);
    parse[i].innerHTML = text
  }
  let tags = document.getElementsByClassName("badge")
  // for(let i = 0; i < tags.length; i++){
  //   let text = tags[i].innerText;
  //   let colour = colorTags(text);
  //   tags[i].style = "background-color: " + colour + " !important;"
  // }
}

window.onload = load