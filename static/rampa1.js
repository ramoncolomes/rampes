

function entrades(i) {
    alt=document.getElementById("h").value;
    long = document.getElementById("l").value
    planta=document.getElementById("x").value
    console.log(planta)
    // evitar que enter validi form i el punt decimal
    window.addEventListener("keypress", function(event){

        if (event.keyCode < 48 || event.keyCode > 57){
            event.preventDefault();
        }
    }, false);
// si es modifica l'alçada
      if (i==1) {
        if(long >0 & planta==0){
            document.getElementById("x").value =Number.parseInt( (long**2-alt**2)**0.5);
        }
        else if (planta>0 & long==0){
            document.getElementById("l").value =Number.parseInt( (alt**2+planta**2)**0.5);
        }else if (planta>0 & long>0){
            document.getElementById("x").value =Number.parseInt( (long**2-alt**2)**0.5);
        }

      }
  // si es modifica L llargada rampa
      if(i==2){
        if(alt>0 & planta==0){
            document.getElementById("x").value =Number.parseInt( (long**2-alt**2)**0.5);
        }else if(planta > 0 & alt==0){
            document.getElementById("h").value =Number.parseInt( (long**2-planta**2)**0.5);
        }
        else if (planta>0 & alt>0){
            document.getElementById("x").value =Number.parseInt( (long**2-alt**2)**0.5);
        }

      }
      if(i==3){
        if(alt>0 & long==0){
            document.getElementById("l").value =Number.parseInt( (alt**2+planta**2)**0.5);
        }
        else if(long>0 & alt==0){
            document.getElementById("h").value =Number.parseInt( (long**2-planta**2)**0.5);
        }
        else if(long>0 & alt>0 ){
            document.getElementById("l").value =Number.parseInt( (alt**2+planta**2)**0.5);
        }
      }
  return
}


function cotxe(){
    window.addEventListener("keypress", function(event){
        document.getElementById("resultats").setAttribute('disabled', "true");
        if (event.keyCode < 48 || event.keyCode > 57){
            event.preventDefault();
        }
    }, false);
}
//document.getElementById('calcular').onclick = function(){
//document.getElementById("1").value="true";
//document.getElementById("1").data_canviat="true";

//function validar(){
    //document.getElementById("1").value="true";
//  a=document.getElementById("1");
//}
