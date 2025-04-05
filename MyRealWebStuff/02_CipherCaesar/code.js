function shiftIt(e)
{
    shift = Number(slider.value);
    shiftValOutput.innerHTML = shift;
    updateText();
}
function updateText(e)
{
    let newText = "";
    let text = textBox.value.toUpperCase();
    shift = Number(slider.value);
    for(let i = 0; i < text.length; i++)
    {
        let letter = text.charAt(i);
        if(isAlphabetic(letter))
        {
            letter = letter.charCodeAt(0)-65;
            letter += shift;
            if(letter < 0)
                letter+=26
            letter %= 26;
            letter = String.fromCharCode(letter+65);
        }
        newText += letter;
    }
    output.innerHTML = newText;
}
function isAlphabetic(str) 
{
    return str.toUpperCase() != str.toLowerCase();
}

//1. Grab HTML Elements by IDs
let textBox = document.getElementById("text")
let slider = document.getElementById("shift")
let shiftValOutput = document.getElementById("shiftVal");
let output = document.getElementById("output")

//2. Add event listeners
slider.addEventListener("input", shiftIt);
textBox.addEventListener("keyup", updateText)

updateText();