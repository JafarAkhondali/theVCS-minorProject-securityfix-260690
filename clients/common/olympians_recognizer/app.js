//selecting all required elements
const dropArea = document.querySelector(".drag-area"),
    dragText = dropArea.querySelector("header"),
    button = dropArea.querySelector("button"),
    input = dropArea.querySelector("input");
let file; //this is a global variable and we'll use it inside multiple functions
button.onclick = () => {
    input.click(); //if user click on the button then the input also clicked
    $(".alert")[0].style.display = "none";
    $(".alert")[0].innerText = ""
    $("#matcher")[0].style.display = "none"
}
input.addEventListener("change", function () {
    //getting user select file and [0] this means if user select multiple files then we'll select only the first one
    file = this.files[0];
    dropArea.classList.add("active");
    showFile(); //calling function
});
//If user Drag File Over DropArea
dropArea.addEventListener("dragover", (event) => {
    event.preventDefault(); //preventing from default behaviour
    dropArea.classList.add("active");
    dragText.textContent = "Release to Upload File";
});
//If user leave dragged File from DropArea
dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("active");
    dragText.textContent = "Drag & Drop to Upload File";
});
//If user drop File on DropArea
dropArea.addEventListener("drop", (event) => {
    event.preventDefault(); //preventing from default behaviour
    //getting user select file and [0] this means if user select multiple files then we'll select only the first one
    file = event.dataTransfer.files[0];
    showFile(); //calling function
});

function showFile() {
    let fileType = file.type; //getting selected file type
    let validExtensions = ["image/jpeg", "image/jpg", "image/png"];
    if (validExtensions.includes(fileType)) {
        let fileReader = new FileReader();
        fileReader.onload = () => {
            // making post request
            let fileURL = fileReader.result;
            var url = "http://localhost:5000/olympians_recognizer_classify_image";

            $.post(url, {
                image_data: fileURL
            }, function (data, status) {
                if (!data || data.length == 0) {
                    return;
                }

                if (data["err"]) {
                    const ele = $(".alert")[0];
                    ele.style.display = "block"
                    ele.innerText = data["err"]
                    return;
                }

                // {class: 'neeraj_chopra', class_probability: Array(7)}
                $("#most_matched")[0].innerText = (data["class"] + " most matched athlete")
                $("#matcher")[0].style.display = "block"

                lst = ["bajrang_punia", "lovlina_borgohain", "mirabai_chanu", "neeraj_chopra", "pr_sreejesh", "pv_sindhu", "ravi_kumar_dahiya"];
                console.log(data["class_probability"])

                const sz = lst.length;

                for (let index = 0; index < sz; index++) {
                    const element = document.getElementById(lst[index]);
                    const prob = data["class_probability"][index];
                    element.innerText = prob;
                }
            })
        }
        fileReader.readAsDataURL(file);
    } else {
        alert("This is not an Image File!");
        dropArea.classList.remove("active");
        dragText.textContent = "Drag & Drop to Upload File";
    }
}