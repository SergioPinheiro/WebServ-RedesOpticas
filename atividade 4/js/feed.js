function setData() {
        var nodes = [];
        var edges = [];
        //fazer - pacific bell
        // randomly create some nodes and edges
        for (var i = 1; i <= 8; i++) {
                nodes.push({
                        id: i,
                        label: String(i)
                });
        }
        
        edges.push({
                from: '1',
                to: '2',
                label: '50'
        });
        edges.push({
                from: '1',
                to: '4',
                label: '80'
        });
        edges.push({
                from: '1',
                to: '6',
                label: '150'
        });
        edges.push({
                from: '2',
                to: '3',
                label: '60'
        });
        edges.push({
                from: '2',
                to: '4',
                label: '40'
        });
        edges.push({
                from: '2',
                to: '5',
                label: '90'
        });
        edges.push({
                from: '3',
                to: '5',
                label: '110'
        });
        edges.push({
                from: '3',
                to: '8',
                label: '150'
        });
        edges.push({
                from: '4',
                to: '6',
                label: '150'
        });
        edges.push({
                from: '4',
                to: '7',
                label: '130'
        });
        edges.push({
                from: '5',
                to: '7',
                label: '120'
        });
        edges.push({
                from: '5',
                to: '8',
                label: '130'
        });
        edges.push({
                from: '6',
                to: '7',
                label: '120'
        });
        edges.push({
                from: '7',
                to: '8',
                label: '120'
        });

        // let send = JSON.stringify({"edges": edges, "connections": [
        //         {"begin":"1", "end": "8"},
		// 		{"begin":"2", "end": "5"}]});
				
		let vezes = prompt("Quantidade de vezes", "5");

		con = [];
		
		for (let index = 0; index < parseInt(vezes); index++) {

			do {
				var rand1 = Math.floor(Math.random() * 8 ) + 1;
				var rand2 = Math.floor(Math.random() * 8 ) + 1;
				console.log("re - random")
			} while (rand1 == rand2);

			con.push({"begin":rand1.toString(), "end": rand2.toString()})
		}
		
		let send = JSON.stringify({"edges": edges, 
			"connections": con
		});
		// console.log(con.lenght)
		loadDoc(send);	
		// if (vezes == null || vezes == "") {
		// 	txt = 1000;
		// }

		// console.log(edges)

        
        
        // console.log();
        return {
                nodes: nodes,
                edges: edges
        };
}



function loadDoc(send) {
        var xhttp = new XMLHttpRequest();
        var message = send;
        xhttp.onreadystatechange = function() {
			if (this.readyState == 4 && this.status == 200) {
	    		// document.getElementById("message").innerHTML = this.responseText;
				console.log(this.responseText)
				let json = JSON.parse(this.responseText);
				console.log(json)
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

	con = [];
	
	for (let index = 0; index < parseInt(vezes); index++) {

		do {
			var rand1 = Math.floor(Math.random() * 8 ) + 1;
			var rand2 = Math.floor(Math.random() * 8 ) + 1;
			console.log("re - random")
		} while (rand1 == rand2);

		con.push({"begin":rand1.toString(), "end": rand2.toString()})
	}
	
	// console.log(data.edges)
	let send = JSON.stringify({"edges": data.edges, 
		"connections": con
	});

	loadDoc(send);
}