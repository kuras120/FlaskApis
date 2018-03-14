function FlipCard() {
    var d = document.getElementById("card");
    if(!d.classList.contains("flipped")){
        d.classList.add("flipped");
    }
    else{
        d.classList.remove("flipped");
    }
}
