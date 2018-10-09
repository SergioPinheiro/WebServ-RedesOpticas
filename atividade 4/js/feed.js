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
        return {
                nodes: nodes,
                edges: edges
        };
}