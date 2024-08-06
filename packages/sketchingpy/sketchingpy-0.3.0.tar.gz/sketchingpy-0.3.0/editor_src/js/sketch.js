const CORE_SRC = "/third_party/core.js?v=0.1.5";


function getSketchName() {
    const paramsStr = window.location.search;
    const params = new URLSearchParams(paramsStr);
    return params.get("filename");
}


function main() {
    const millis = Date.now();
    const sketchName = getSketchName();

    const sketchLabelText = document.createTextNode(sketchName);
    document.getElementById("sketch-label").appendChild(sketchLabelText);

    let progress = 0;
    const progressBar = document.getElementById("sketch-load-progress");
    progressBar.value = 0;
    const incrementBar = () => {
        progressBar.value += 1;

        if (progressBar.value < 19) {
            setTimeout(incrementBar, 500);
        }
    };
    incrementBar();
}


main();
