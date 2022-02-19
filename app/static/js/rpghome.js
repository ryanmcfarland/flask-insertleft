/*
https://stackoverflow.com/questions/1051061/convert-json-array-to-an-html-table-in-jquery

https://stackoverflow.com/questions/26079754/flask-how-to-return-a-success-status-code-for-ajax-call
https://stackoverflow.com/questions/5589420/select-tr-by-id-with-jquery
https://roytuts.com/delete-multiple-rows-from-table-using-flask-ajax-jquery-mysql/
https://stackoverflow.com/questions/22437514/how-to-keep-elements-on-same-line-with-overflow

$.getJSON('/'+home+'/sheets', function(data) {
    $.each(data['sheets'], function(index, element) {
        console.log(element)
        $('body').append($('<div>', {
            text: element.id
        }));
    });
});
*/

function createButtonGroup (name, id) {
    var btnG = '<div class="sheet-stat button"><a class="btn btn-primary btn-block" href="/'+home+'/edit/'+id+'" role="button">Edit</a></div>';
    return btnG+= '<div class="sheet-stat button last"><button class="btn btn-danger btn-block" name="delete" onclick="deleteSheet(\''+name+'\',\''+id+'\')">Delete</button></div>';
}

function formatName(name){
    if (name.length > 30) {
        name = name.substring(0,30)+"...";
    };
    return name;
};

function addSheetHitPoints(ch,mh){
    var perc = ch / mh;
    var clr = "green";
    if ( perc < 0.2 ) { clr = "red"} else if ( perc < 1.0 ) { clr = "yellow" } else { };
    var hstr = '<div class="sheet-stat hp"><div class="small-header">HP</div>';
    hstr += '<span class="'+clr+'">'+ch+'</span>';
    hstr += '<span style="font-weight:100;"> / </span>';
    hstr += '<span class="green">'+mh+'</span>';
    return hstr += '</div>'
}

function appendUserRow (data){
    $('#no-user-sheets').remove();
    var rowString = '<div id=row_'+data['id']+' class="sheet"><div class="block">';
    rowString += '<div class="wrap sheet-stats"><a class="sheet-show" href="/'+home+'/sheet/'+data['id']+'"><div class="wrap justify-content-left">';
    rowString += '<div class="sheet-stat name"><div class="small-header">Name</div>'+formatName(data['name'])+'</div>';
    rowString += '<div class="sheet-stat class"><div class="small-header">Class</div>'+data['character_class']+'</div>';
    rowString += '<div class="sheet-stat background"><div class="small-header">Background</div>'+data['background']+'</div>';
    rowString += '<div class="sheet-stat level"><div class="small-header">Level</div>'+data['level']+'</div>';
    rowString += addSheetHitPoints(data['current_hp'],data['max_hp']);
    rowString += '</div></a></div>';
    rowString += createButtonGroup(data['name'], data['id']);
    rowString += '</div></div>';
    $('.user-sheets').append(rowString);
}

function appendPlayerRow (data){
    $('#no-player-sheets').remove();
    var rowString = '<div id=row_'+data['id']+' class="sheet"><div class="block">';
    rowString += '<div class="wrap sheet-stats"><a class="sheet-show" href="/'+home+'/sheet/'+data['id']+'"><div class="wrap justify-content-left">';
    rowString += '<div class="sheet-stat name"><div class="small-header">Name</div>'+formatName(data['name'])+'</div>';
    rowString += '<div class="sheet-stat class"><div class="small-header">Class</div>'+data['character_class']+'</div>';
    rowString += '<div class="sheet-stat background"><div class="small-header">Background</div>'+data['background']+'</div>';
    rowString += '<div class="sheet-stat level"><div class="small-header">Level</div>'+data['level']+'</div>';
    rowString += addSheetHitPoints(data['current_hp'],data['max_hp']);
    rowString += '<div class="sheet-stat user"><div class="small-header">User</div>'+data['user'][0]['username']+'</div>'
    rowString += '</div></a></div>';
    rowString += '</div></div>';
    $('.player-sheets').append(rowString);
}

function removeRow (id){
    $('#row_'+id).remove();
};

function createNewSheet () {
    $.ajax({
    type: "POST",
    url: '/'+home+'/create',
    dataType: 'json',
    success: function(data) {
        appendUserRow(data['sheets']);
    }});
};

function deleteSheet(name, id) {
    if (!window.confirm("Are you sure you want to delete: "+name+" ?" )) {
        return false
    };
    $.ajax({
    type: "DELETE",
    url: '/'+home+'/delete/'+id,
    dataType: 'json',
    success: function() {
        removeRow(id);
    }});
};


function queryUserSheets () {
    $.ajax({
        type: "GET",
        url: '/'+home+'/usersheets',
        dataType: 'json',
        success: function(data) {
            console.log(data);
            if (data['sheets'].length == 0){
                $('.user-sheets').append('<div id="no-user-sheets" class="justify-content-center"><p>You have no characters saved!</p></div>')
            } else {
                $.each(data['sheets'], function(index, element) {
                    appendUserRow(element);
                });
            };
        },
        error: function() {
            $('.user-sheets').append('<div id="no-user-sheets" class="justify-content-center"><p>You have no characters saved!</p></div>')
        }
    })
}

/*
var searchParams = new URLSearchParams(window.location.search);
    searchParams.set("foo", "bar");
    window.location.search = searchParams.toString()
*/
function queryPlayerSheetsIter (page) {
    var url = '/'+home+'/home';
    var searchParams = new URLSearchParams(window.location.search);
    var query = searchParams.get("page");
    if (page !== undefined) {
        searchParams.set("page", page);
        query=searchParams.toString();
        window.history.pushState(url,'',url+'?'+query);
    } else if (query == null) {
        query = '';
    } else {
        query=searchParams.toString();
    };
    $.ajax({
        type: "GET",
        url: '/'+home+'/playersheets?'+query,
        dataType: 'json',
        success: function(data) {
            $('.player-sheets').remove();
            $('#nav-player-paginate').remove();
            $('#player-block').append('<div class="player-sheets"></div>');
            if (data['sheets'].length == 0){
                $('.player-sheets').append('<div id="no-player-sheets" class="justify-content-center"><p>There are no other player sheets!</p></div>')
            } else {
                $.each(data['sheets'], function(index, element) {
                appendPlayerRow(element);
                });
            };
            $('#player-paginate').append(generatePaginate(data['iter']))
        },
        error: function() {
            $('.player-sheets').append('<div id="no-player-sheets" class="justify-content-center"><p>There are no other player sheets!</p></div>')
        }
    })
}

/* 
*/ 
function generatePaginate(iter) {
    var pagStr = '<nav id="nav-player-paginate" aria-label="..."><ul class="pagination">';
    if (!iter['has_prev']) {
        pagStr += '<li class="page-item disabled"><span class="page-link">Previous</span></li></li>';
    } else {
        pagStr += '<li class="page-item"><button class="page-link" onclick="queryPlayerSheetsIter('+(iter['page']-1)+')">Previous</button></li>';
    };
    for (let i = 0; i < iter['iter'].length;i ++) {
        pg = iter['iter'][i];
        if (pg == iter['page'] ) {
            pagStr += '<li class="page-item active"><span class="page-link">'+pg+'<span class="sr-only">(current)</span></span></li>';
        } else if ('None' == pg) {
            null
        } else {
            pagStr += '<li class="page-item"><button class="page-link" onclick="queryPlayerSheetsIter('+pg+')">'+pg+'</button></li>';
        };
    };
    if (!iter['has_next']) {
        pagStr += '<li class="page-item disabled"><span class="page-link">Next</span></li></li>';
    } else {
        pagStr += '<li class="page-item"><button class="page-link" onclick="queryPlayerSheetsIter('+(iter['page']+1)+')">Next</button></li>';
    };
    return pagStr += '</ul></nav>'
}

/*
When the document is ready, query the backend to get all character sheets
*/
$( document ).ready(function() {
    if(document.getElementById("user-block") !== null){ queryUserSheets(); };
    queryPlayerSheetsIter();
});
