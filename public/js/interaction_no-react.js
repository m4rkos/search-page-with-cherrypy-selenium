$(document).ready(function() {

    $("#generate-string").click(function(e) {
        $("#generate-string").hide();
        $("#the-string").html(`
            <img src="static/img/lSUb1T4YW1td0UskwsGZ1w.gif" width="130" height="131">
            <br>
            <p class="t-center">searching ...</p>`).show();
        $.post("/generator", {"search_query": $("input[name='search_query']").val()})
        .done(function(string) {
            $("#the-string").html(`<h3>Ok <span id="search-name"></span></h3>`);
            $("span#search-name").text(string);
            $("input[name='search_query']").val('');
            
            fetch("/generator?type=1", {
                "method": "GET", "headers": {}
            })
            .then(response => { return response.text()
                .then(text => {
                    document.querySelector("#results").innerHTML = text
                    console.log(response);
                })                
            })
            .catch(err => {
                console.error(err);
            });                
            
            //$("#the-string input").val(string);
            $("#generate-string").show();
            setTimeout(function() {
                $("#the-string").hide();
            }, 10000);
            
        });
        e.preventDefault();
    });

    // $("#replace-string").click(function(e) {
    //     $.ajax({
    //         type: "PUT",
    //         url: "/generator",
    //         data: {"another_string": $("#the-string input").val()}
    //     })
    //     .done(function() {
    //         alert("Replaced!");
    //     });
    //     e.preventDefault();
    // });

    // $("#delete-string").click(function(e) {
    //     $.ajax({
    //         type: "DELETE",
    //         url: "/generator"
    //     })
    //     .done(function() {
    //         $("#the-string").hide();
    //     });
    //     e.preventDefault();
    // });

});