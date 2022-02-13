$.log("Parser.js Library Connected. Functions Online.")

/*
CODESPHERE MARKDOWN EDITOR
This is the markdown editor used for CodeSphere, the command keys are:
*placeholder* for bold
_placeholder_ for italics
<placeholder> for underline
-placeholder- for strikethrough

To use this function, you first give it a unparsed plaintext markdown file through its paramters.
markdown(params:[text: type==string])
This function will return an html string after parsing through the markdown string.
*/
const markdown = (text) => {
  let map = text.split("");
  var tree = [];
  let res = [];
  for (let i = 0; i < map.length; i++) {
    let type, count, start, end;
    switch (map[i]) {
      case '\\':
        i ++;
        break;
      case '*':
        type = "bold"
        count = i;
        count++;
        start = i;
        end;
        for (var j = count; j < map.length; j++) {
          if (map[j] == "*") {
            end = j;
            i = j;
            break;
          } else {
            let _type = "normal"
            let _start = j;
            let _end = j;
            let _text = map[j]
            tree.push({ start: _start, end: _end, type: _type, text: _text })
          }
        }
        tree.push({ start: start, end: end, type: type, text: "font-weight: bold;" })
        break;
      case '_':
        type = "italics"
        count = i;
        count++;
        start = i;
        end;
        for (var j = count; j < map.length; j++) {
          if (map[j] == "_") {
            end = j;
            i = j;
            break;
          } else {
            let _type = "normal"
            let _start = j;
            let _end = j;
            let _text = map[j]
            tree.push({ start: _start, end: _end, type: _type, text: _text })
          }
        }
        tree.push({ start: start, end: end, type: type, text: "font-style: italic;" })
        break;
      case '<':
        type = "underline"
        count = i;
        count++;
        start = i;
        end;
        for (var j = count; j < map.length; j++) {
          if (map[j] == ">") {
            end = j;
            i = j;
            break;
          } else {
            let _type = "normal"
            let _start = j;
            let _end = j;
            let _text = map[j]
            tree.push({ start: _start, end: _end, type: _type, text: _text })
          }
        }
        tree.push({ start: start, end: end, type: type, text: "text-decoration: underline;" })
        break;
      case '-':
        type = "strikethrough"
        count = i;
        count++;
        start = i;
        end;
        for (var j = count; j < map.length; j++) {
          if (map[j] == "-") {
            end = j;
            i = j;
            break;
          } else {
            let _type = "normal"
            let _start = j;
            let _end = j;
            let _text = map[j]
            tree.push({ start: _start, end: _end, type: _type, text: _text })
          }
        }
        tree.push({ start: start, end: end, type: type, text: "text-decoration: line-through;" })
        break;
      default:
        type = "normal"
        start = i;
        end = i;
        let text = map[i]
        tree.push({ start: start, end: end, type: type, text: text })
        break;
    }
  }
  for (var i = 0; i < tree.length; i++) {
    let start = tree[i].start;
    let end = tree[i].end;
    let type = tree[i].type;
    let text = tree[i].text
    console.log(start, end, type)
    if (type == "normal") {
      res[start] = text
    } else {
      res[start] = "<span style=\"" + text + "\">"
      res[end] = "</span>"
    }
  }
  res = res.join('')
  return res
}

/*
CODESPHERE PROFANITY FILTER
This is the profanity filter used in Codesphere, the swear words are stored in list.js

To use this function, you first give it a plaintext file through its paramters.
profanity(params:[txt: type==string])
This function will return an string after parsing the text.
*/

const profanity = (text) => {
	list.forEach(item => {
		let regex = item;
		regex = regex.replace(/\+/g, "\\+")
			         .replace(/\*/g, "\\*")
					 .replace(/\-/g, "\\-")
					 .replace(/\$/g, "\\$")
					 .replace(/\./g, "\\.")
					 .replace(/\^/g, "\\^")
					 .replace(/\[/g, "\\[")
					 .replace(/\]/g, "\\]")
					 .replace(/\{/g, "\\{")
					 .replace(/\}/g, "\\}");
		regex = regex.split("");
		regex = regex.map(char => char === "\\" ? char : char + "\\W*?");
		regex = regex.join("");
		regex = regex.replace(/a/gi, "[a|@|4]")
						.replace(/e/gi, "[e|3]")
						.replace(/i/gi, "[i|1]")
						.replace(/o/gi, "[o|0]")
						.replace(/t/gi, "[t|7]")
						.replace(/s/gi, "[s|5]")
						.replace(/b/gi, "[b|ß|6]")
						.replace(/g/gi, "[g|9]");
		regex = "\\b" + regex + "\\b"
		while (text.match(new RegExp(regex, "im"))) {
			const swear = text.match(new RegExp(regex, "im"));
			text = text.substring(0, swear.index) + "*".repeat(swear[0].length) + text.substring(swear.index + swear[0].length)
		}
	});
	return text
};
