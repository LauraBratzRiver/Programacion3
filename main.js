window.zindex = 1;
$(document).ready(function(e){
    $("#mnxAppAcademica a").click(function(e){
        e.preventDefault();
        let modulo = $(this).data("modulo"),
            form = $(this).data("formulario");

        $.abrirVentana(modulo, form);
    });
    $.abrirVentana = (modulo,form)=>{
        let $ventana = $(`#${modulo}_${form}`);
        $ventana.load(`${modulo}/${modulo}_${form}.html`, function(){
            $ventana.click(function(){
                $(this).css("z-index", ++zindex);
            });
        }).draggable();
    };
});