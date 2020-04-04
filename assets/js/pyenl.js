var i=3;

$(".plus-var").click(function(){
    addVar();
});

$(".plus-ans").click(function(){
    addAns();
});


$(".plus-eq").click(function(){
    
    $(".box-eq").append('<input type="text" placeholder="Ecuación ' + i +'"></input>');
    addVar();
    addAns();
    i++;
});

function addVar(){
    $(".tb-var").append("<tr> <td class='tg-baqh'>Z"+i+ "</td> <td class='tg-baqh'>1</td> <td class='tg-baqh'>-1000</td> <td class='tg-baqh'>1000</td> <td class='tg-baqh'>dimensionless</td> <td class='tg-baqh'>Variable</td> </tr>");
}

function addAns(){
    $(".tb-ans").append('<tr> <td class="tg-nrix">Z'+i+ '</td> <td class="tg-nrix">1</td> <td class="tg-nrix">dimensionless</td> <td class="tg-baqh">Variable</td> </tr>');
}