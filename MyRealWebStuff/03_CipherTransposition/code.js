function updateText(e)
{
    let text = textBox.value.toUpperCase();
    let key = keyInput.value.toUpperCase();
    let newText = "";
    for(let i = 0; i < key.length; i++)
    
    output.innerHTML = newText;
}
function nextMin(text, index)
{
    let minIndex = -1;
    for(let i = 0; i < text.length; i++)
    {
        if (i == index)
            continue;
        if(text.charAt(i)<text.charAt(index))
            continue;
        if( text.charAt(i) == text.charAt(index) && i < index)
            continue;
        if(minIndex == -1 || text.charAt(i) < text.charAt(minIndex))
            minIndex = i;
    }
    return minIndex;
}
//1. Grab HTML Elements by IDs
let textBox = document.getElementById("text")
let keyInput = document.getElementById("key")
let output = document.getElementById("output")

//2. Add event listeners
textBox.addEventListener("keyup", updateText)

updateText();