/*
File with random JS functions that were created and then disgarded


/*
wanted to paginate player sheets - uses these python methods:
    iter = [str(i) for i in sheets.iter_pages(left_edge=0, right_edge=0, left_current=2, right_current=3)]
    pn = dict(has_next=sheets.has_next, has_prev=sheets.has_prev, page=sheets.page, iter=iter)
    jsonify(iter=pn)
*/
function generatePaginate(iter) {
    var pagStr = '<nav aria-label="..."><ul class="pagination">';
    if (!iter['has_prev']) {
        pagStr += '<li class="page-item disabled"><span class="page-link">Previous</span></li></li>';
    } else {
        pagStr += '<li class="page-item"><a class="page-link" href="/'+home+'/playersheets?page='+iter['prev_num']+'">Previous</a></li>';
    };
    for (let i = 0; i < iter['iter'].length;i ++) {
        if (i == iter['page'] ) {
            pagStr += '<li class="page-item active"><span class="page-link">'+i+'<span class="sr-only">(current)</span></span></li>';
        } else if (!i) {
            null
        } else {
            pagStr += '<li class="page-item"><a class="page-link" href="/'+home+'/playersheets?page='+i+'">'+i+'</a></li>';
        };
    };
    if (!iter['next_num']) {
        pagStr += '<li class="page-item disabled"><span class="page-link">Next</span></li></li>';
    } else {
        pagStr += '<li class="page-item"><a class="page-link" href="/'+home+'/playersheets?page='+iter['next_num']+'">next</a></li>';
    };
    return pagStr += '</ul></nav>'
}