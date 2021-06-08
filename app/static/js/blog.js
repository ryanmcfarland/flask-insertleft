// https://www.geeksforgeeks.org/how-to-detect-shiftenter-and-generate-a-new-line-in-textarea/
// https://python-markdown.github.io/extensions/attr_list/

var easyMDE = new EasyMDE({
    element: document.getElementById('main_body'),
    spellChecker: true,
    nativeSpellcheck: true,
    lineNumbers:true,
    minHeight: "400px",
    maxHeight: "400px",
    sideBySideFullscreen: false,
    insertTexts: {
	    image: ["![](http://", "){: class=\"rounded mx-auto d-block\"}"],
	},
    toolbar: ["bold", "italic", "heading", "|", "code", "quote", "unordered-list", "ordered-list", "|", "link", "image", "|", "table", "|", "side-by-side", "|", "guide"]
    });

var easyMDECap = new EasyMDE({
        element: document.getElementById('caption'),
        spellChecker: true,
        nativeSpellcheck: true,
        lineNumbers:true,
        minHeight: "100px",
        maxHeight: "100px",
        sideBySideFullscreen: false,
        toolbar: false
        });

/*
wanted to add a newline character but no point
easyMDE.codemirror.getCursor() -> {line:3, ch:0}

easyMDE.codemirror.on("keyHandled", function(editor, event){
    if(event == "Enter") {
        console.log("Enter pressed");
        easyMDE.codemirror.replaceRange("\n", easyMDE.codemirror.getCursor());
    }
})
*/