async function uploadImage() {

const file =
document.getElementById("fileInput").files[0];

if (!file) {
alert("Seleccione una imagen");
return;
}

const loading =
document.getElementById("loading");

loading.innerHTML =
"Procesando imagen...";

const formData = new FormData();

formData.append("file", file);

const response = await fetch(
"/process",
{
method:"POST",
body:formData
}
);

const data = await response.json();

loading.innerHTML = "";

document.getElementById("result")
.innerHTML = `
<img src="${data.preview}">

<div class="links">
<a href="${data.png}">
Descargar PNG
</a>

<a href="${data.svg}">
Descargar SVG
</a>
</div>
`;
}

