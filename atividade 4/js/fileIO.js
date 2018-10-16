function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

document.getElementById("dwn-btn").addEventListener("click", function(){
    // Generate download of hello.txt file with some content
    var text = prepareData(networkData.nodes.get(),networkData.edges.get(), dijkstra);
    var filename = document.getElementById('file-name').value + '.txt';
    download(filename, text);
}, false);

var fileData, reader;

reader = new FileReader();

function loadFile() {
    var file = document.getElementById("myFile").files[0];
    reader.onload = function(e) {
        var text = reader.result;
        fileData = JSON.parse(text);
        console.log(fileData);
        networkData.nodes = new vis.DataSet(fileData.nodes);
        networkData.edges = new vis.DataSet(fileData.edges);
        network.setData(networkData);
        network.redraw();
    }
    reader.readAsText(file);
}



function prepareData(nodes,edges,dijkstra){
    let dataToSave, textData;
    dataToSave = {
				    nodes: nodes,
                    edges: edges,
                    dijkstra: dijkstra
                };
    textData = JSON.stringify(dataToSave);
    return textData;
}

