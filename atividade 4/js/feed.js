var dijkstra;
function setData() {
        var nodesArray, edgesArray, nodes, edges;
        nodesArray = [];
        //fazer - pacific bell
        // randomly create some nodes and edges
        for (var i = 1; i <= 17; i++) {
                nodesArray.push({id: i, label: String(i)});
        }
        edgesArray = [
            {from: 1, to: 3, label: '100'},
            {from: 1, to: 4, label: '90'},
            {from: 1, to: 5, label: '100'},
            {from: 1, to: 6, label: '120'},
            {from: 1, to: 7, label: '150'},
            {from: 2, to: 4, label: '80'},
            {from: 2, to: 5, label: '90'},
            {from: 3, to: 8, label: '60'},
            {from: 4, to: 9, label: '140'},
            {from: 4, to: 10, label: '100'},
            {from: 4, to: 13, label: '100'},
            {from: 4, to: 16, label: '100'},
            {from: 5, to: 9, label: '120'},
            {from: 5, to: 14, label: '90'},
            {from: 5, to: 16, label: '100'},
            {from: 6, to: 15, label: '150'},
            {from: 7, to: 8, label: '110'},
            {from: 7, to: 10, label: '100'},
            {from: 7, to: 11, label: '100'},
            {from: 11, to: 12, label: '100'},
            {from: 12, to: 13, label: '90'},
            {from: 14, to: 17, label: '90'},
            {from: 15, to: 17, label: '90'},

        ];
        // edgesArray = [
        //     {from: 1, to: 2, label: '50'},
        //     {from: 1, to: 4, label: '80'},
        //     {from: 1, to: 6, label: '150'},
        //     {from: 2, to: 3, label: '60'},
        //     {from: 2, to: 4, label: '40'},
        //     {from: 2, to: 5, label: '90'},
        //     {from: 3, to: 5, label: '110'},
        //     {from: 3, to: 8, label: '150'},
        //     {from: 4, to: 6, label: '150'},
        //     {from: 4, to: 7, label: '130'},
        //     {from: 5, to: 7, label: '120'},
        //     {from: 5, to: 8, label: '130'},
        //     {from: 6, to: 7, label: '120'},
        //     {from: 7, to: 8, label: '120'}];

        nodes = new vis.DataSet(nodesArray);
        edges = new vis.DataSet(edgesArray);

        //edges.update({id:"1acf0638-7138-48ad-907e-e7a1bb9dc896", from:7, to:8, label: 150});
        //sintaxe para dar update, não precisa todos os campos;

		/*let vezes = prompt("Quantidade de vezes", "5");

		con = [];

		for (let index = 0; index < parseInt(vezes); index++) {

			do {
				var rand1 = Math.floor(Math.random() * nodes.length ) + 1;
				var rand2 = Math.floor(Math.random() * nodes.length ) + 1;
				console.log("re - random")
			} while (rand1 == rand2);

			con.push({"begin":rand1, "end": rand2})
		}

		let send = JSON.stringify({"edges": edges.get(),"connections": con});
		loadDoc(send);*/
        return {nodes: nodes, edges: edges};
}

function loadDoc(send) {
        var xhttp = new XMLHttpRequest();
        var message = send;
        xhttp.onreadystatechange = function() {
			if (this.readyState == 4 && this.status == 200) {
				let json = JSON.parse(this.responseText);
				dijkstra = json;
				console.log(json);
				// for (const key in json) {
				// 	if (json.hasOwnProperty(key)) {
				// 		// const element = object[key];
				// 		var ul = document.getElementById("respostas");
				// 		var li = document.createElement("li");
				// 		li.appendChild(document.createTextNode(JSON.stringify(json[key])));
				// 		ul.appendChild(li);
						
				// 		// console.log(json[key].toString())
				// 	}
				// }
			}
        };
        xhttp.open("POST", "http://localhost:8080", true);
        xhttp.send(message);
}


function checktopo(){
	let vezes = prompt("Quantidade de vezes", "5");
	let nCompOnda = prompt("Numero de comprimentos de onda", 1);
	let tempo = prompt("total de tempo de simulação em segundos", 300);

	con = [];

	for (let index = 0; index < parseInt(vezes); index++) {

		do {
			var rand1 = Math.floor(Math.random() * 8 ) + 1;
			var rand2 = Math.floor(Math.random() * 8 ) + 1;
			console.log("re - random")
		} while (rand1 == rand2);

		con.push({"begin":rand1, "end": rand2})
	}
	let arestas = networkData.edges.get();
	// console.log(data.edges)
	let send = JSON.stringify({"edges": arestas,
		"connections": con,
        "nwavelenghts" : nCompOnda,
        "tempo" : tempo
	});

	loadDoc(send);
}

function debugData(){
    console.log(networkData.nodes);
}



