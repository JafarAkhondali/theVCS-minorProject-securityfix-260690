ml = false;
tool = false;

function all_ml_projects() {
    const ele = $('#ml_box');
    if(ml)return;

    var url = "http://localhost:5000/all_ml_projects";

    $.post(url, {},
        function (data, status) {
            for (const opt in data) {
                const page = data[opt];
                var li = document.createElement("LI");
                var a = document.createElement("A");
                a.innerText = opt;
                a.href = "./" + page + ".html";
                li.append(a);
                ele.append(li);
            }

            ml = true;
        })
}


function all_tool_projects() {
    const ele = $('#tool_box');
    if(tool)return;

    var url = "http://localhost:5000/all_tool_projects";

    $.post(url, {},
        function (data, status) {
            for (const opt in data) {
                const page = data[opt];
                var li = document.createElement("LI");
                var a = document.createElement("A");
                a.innerText = opt;
                a.href = "./" + page + ".html";
                li.append(a);
                ele.append(li);
            }

            tool = true;
        })
}