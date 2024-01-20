const ddEncryptionTypes = document.getElementById("encryption-type");
ddEncryptionTypes.addEventListener("input", (e) => {
  const ctnVector = document.getElementById("ctn-vector");
  if (e.target.value === "caesar") {
    ctnVector.style.display = "block";
  } else if (e.target.value === "monoalpha") {
    ctnVector.setAttribute("style", "display: none");
  }
});
