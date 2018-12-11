var network, networkData, seed;
network= null;
// randomly create some nodes and edges
networkData = setData();
seed = 4;
//4

// console.log(JSON.stringify(data))
function destroy() {
    if (network !== null) {
        network.destroy();
        network = null;
    }
}

function draw() {
    destroy();
    // create a network
    var container = document.getElementById('mynetwork');
    var options = {
        autoResize: true,
         physics: {
            enabled: false
        },
        height: '100%',
        width: '100%',
        clickToUse : true,
        layout: {
            randomSeed: seed
        }, // just to make sure the layout is the same when the locale is changed
        locale: "en",
        manipulation: {
            addNode: function (data, callback) {
                // filling in the popup DOM elements
                document.getElementById('node-operation').innerHTML = "Add Node";
                editNode(data, clearNodePopUp, callback);
            },
            editNode: function (data, callback) {
                // filling in the popup DOM elements
                document.getElementById('node-operation').innerHTML = "Edit Node";
                editNode(data, cancelNodeEdit, callback);
            },
            addEdge: function (data, callback) {
                if (data.from == data.to) {
                    var r = confirm("Do you want to connect the node to itself?");
                    if (r != true) {
                        callback(null);
                        return;
                    }
                }
                document.getElementById('edge-operation').innerHTML = "Add Edge";
                editEdgeWithoutDrag(data, callback);
            },
            editEdge: {
                editWithoutDrag: function (data, callback) {
                    document.getElementById('edge-operation').innerHTML = "Edit Edge";
                    editEdgeWithoutDrag(data, callback);
                }
            }
        }
    };
    network = new vis.Network(container, networkData, options);
}

function editNode(data, cancelAction, callback) {
    document.getElementById('node-label').value = data.label;
    document.getElementById('node-saveButton').onclick = saveNodeData.bind(this, data, callback);
    document.getElementById('node-cancelButton').onclick = cancelAction.bind(this, callback);
    document.getElementById('node-popUp').style.display = 'block';
}

// Callback passed as parameter is ignored
function clearNodePopUp() {
    document.getElementById('node-saveButton').onclick = null;
    document.getElementById('node-cancelButton').onclick = null;
    document.getElementById('node-popUp').style.display = 'none';
}

function cancelNodeEdit(callback) {
    clearNodePopUp();
    callback(null);
}

function saveNodeData(data, callback) {
    data.label = document.getElementById('node-label').value;
    networkData.nodes.update({id:data.id, label:data.label});
    // console.log(data)
    clearNodePopUp();
    callback(data);
    
}

function editEdgeWithoutDrag(data, callback) {
    // filling in the popup DOM elements
    document.getElementById('edge-label').value = data.label;
    document.getElementById('edge-saveButton').onclick = saveEdgeData.bind(this, data, callback);
    document.getElementById('edge-cancelButton').onclick = cancelEdgeEdit.bind(this, callback);
    document.getElementById('edge-popUp').style.display = 'block';
}

function clearEdgePopUp() {
    document.getElementById('edge-saveButton').onclick = null;
    document.getElementById('edge-cancelButton').onclick = null;
    document.getElementById('edge-popUp').style.display = 'none';
}

function cancelEdgeEdit(callback) {
    clearEdgePopUp();
    callback(null);
}

function saveEdgeData(data, callback) {
    // callback(data);
    if (typeof data.to === 'object'){
        data.to = data.to.id;
        networkData.edges.update({id:data.id, to: data.to});
    }

    if (typeof data.from === 'object'){
        data.from = data.from.id;
        networkData.edges.update({id:data.id, from: data.from});
    }
    data.label = document.getElementById('edge-label').value;
    // networkData.edges.update({id:data.id, label:data.label});
    clearEdgePopUp();
    
    callback(data);
}



function init() {
    // setDefaultLocale();
    // addNodeMode();
    draw();
}